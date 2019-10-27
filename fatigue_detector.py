from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear

def lip_droop(mouth):
	# compute the euclidean distances between the  upper lip
	# and the outermost points of the lips
	W = dist.euclidean(mouth[0], mouth[2])
	X = dist.euclidean(mouth[6], mouth[4])

	# compute the euclidean distances between the right edges of the upper and lower
	# lips and the outermost right point of the lips
	Y = dist.euclidean(mouth[0], mouth[10])
	Z = dist.euclidean(mouth[6], mouth[8])

	# compute the lip hang
	ldroop = (W + X) / (Y + Z)

	return ldroop

def face_map(face):
	# grab the indexes of the facial landmarks for the left and
	# right eye, respectively
	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

	# grab the indexes of the facial landmarks for the mouth
	(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

	# determine the facial landmarks for the face region, then
	# convert the facial landmark (x, y)-coordinates to a NumPy array
	shape = predictor(gray, face)
	shape = face_utils.shape_to_np(shape)

	# extract the left and right eye coordinates, then use the
	# coordinates to compute the eye aspect ratio for both eyes
	leftEye = shape[lStart:lEnd]
	rightEye = shape[rStart:rEnd]
	leftEAR = eye_aspect_ratio(leftEye)
	rightEAR = eye_aspect_ratio(rightEye)

	# extract the mouth coordinates, then use the coordinates
	# to compute the lip droop
	mouth = shape[mStart:mEnd]
	ldroop = lip_droop(mouth)

	# average the eye aspect ratio together for both eyes
	ear = (leftEAR + rightEAR) / 2.0

	return ear, ldroop, leftEye, rightEye, mouth

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="",
	help="path alarm .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
ap.add_argument("-i", "--image", type=str,
	help="path to original picture of physician")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# Load in the original image, resize it, and convert it to grayscale
orig_image = cv2.imread(args["image"])
orig_image = imutils.resize(orig_image, width=450)
gray = cv2.cvtColor(orig_image, cv2.COLOR_BGR2GRAY)

# Detect faces in the grayscale image
faces = detector(gray, 1)

for face in faces:
	eyelid_hang, lip_d, _, _, _ = face_map(face)

# Threshold for the eyelid hang
EYE_AR_THRESH = eyelid_hang

# Threshold for the lip droop
LIP_DROOP_THRESH = lip_d

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

# create an array to hold all the eye aspect ratios throughout the recording
ear_array = []
ldroop_array = []
frames_below_thres = 0
num_frames = 0

# loop over frames from the video stream
while True:
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale channels)
	frame = vs.read()
	num_frames += 1
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	faces = detector(gray, 0)

	# loop over the face detections
	for face in faces:
		ear, ldroop, leye, reye, mouth = face_map(face)
		ldroop_array.append(ldroop)
		# add the average eye aspect ratio to the array of eye aspect ratios
		ear_array.append(ear)

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leye)
		rightEyeHull = cv2.convexHull(reye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		# compute the convex hull for the mouth, then visualize it
		mouthHull = cv2.convexHull(mouth)
		cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
			frames_below_thres += 1

		# draw the computed eye aspect ratio on the frame to help
		# with debugging and setting the correct eye aspect ratio
		# thresholds and frame counters
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		# draw the computed lip hang on the frame to help
		# with debugging and setting the correct lip hang
		# thresholds and frame counters
		cv2.putText(frame, "Lip Hang: {:.2f}".format(ldroop), (300, 60),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

baseline_ear = round(EYE_AR_THRESH, 2)
print(f"Baseline EAR: {baseline_ear}")
baseline_ldroop = round(LIP_DROOP_THRESH, 2)
print(f"Baseline Lip Droop: {baseline_ldroop}")

average_ear = np.mean(ear_array)
print(f"Average Eye Aspect Ratio: {average_ear.round(2)}")
average_ldroop = np.mean(ldroop_array)
print(f"Average Lip Droop: {average_ldroop.round(2)}")
drowsiness_score = round(frames_below_thres/num_frames, 2)
print(f"Drowsiness Score: {drowsiness_score}")

# Assess whether the physician is fit to work
elhang_score = 0
ldroop_score = 0
drows_score = 0

# Score the recorded eyelid hang
if average_ear >= baseline_ear:
	elhang_score = 1
elif average_ear > baseline_ear-0.05:
	elhang_score = 2
else:
	elhang_score = 3

# Score the recorded lip droop
if average_ldroop <= baseline_ldroop:
	ldroop_score = 1
elif average_ldroop < baseline_ldroop+0.05:
	ldroop_score = 2
else:
	ldroop_score = 3

# Score the recorded drowsiness
if drowsiness_score >= 0.7:
	drows_score = 3
elif drowsiness_score > 0.45:
	drows_score = 2
else:
	drows_score = 1

# Calculate the composite score
comp_score = elhang_score + ldroop_score + drows_score

# Provide a recommendation based on the fatigue detected in the physician
if comp_score < 5:
	print("Physician is fully cleared to practice")
elif comp_score < 7:
	print("Physician is fit to practice but should be reassessed in 1 hour")
else:
	print("Physician is too fatigued to practice")

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
