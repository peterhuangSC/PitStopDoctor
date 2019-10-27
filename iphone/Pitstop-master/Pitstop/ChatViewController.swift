//
//  ViewController.swift
//  PitStop
//
//  Created by Peter Huang on 26/10/2019.
//

import UIKit
import Firebase
//import PythonKit

class ChatViewController: UIViewController {

    @IBOutlet var heightConstraint: NSLayoutConstraint!
    
    @IBOutlet weak var BeginPitstop: UIButton!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        BeginPitstop.layer.cornerRadius = 10
        
        let pkA = PythonTesterA.init()
        pkA.loadSimpleFn()
        //pkA.numpyTest()
        
        //TODO: Set yourself as the delegate and datasource here:
        //TODO: Set yourself as the delegate of the text field here:
        //TODO: Set the tapGesture here:
        //TODO: Register your MessageCell.xib file here:

    }
    
    @IBAction func beginPressed(_ sender: UIButton) {
        
        print("Executing python file!")
        
        //let file = Python.open("filename")
    }
    
    
    @IBAction func logOutPressed(_ sender: AnyObject) {
        do {
            try Auth.auth().signOut()
            navigationController?.popToRootViewController(animated: true)
        } catch {
            print("Error, there was a problem signing out")
        }
    }
    
}
