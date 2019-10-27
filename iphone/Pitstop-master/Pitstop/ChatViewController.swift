//
//  ViewController.swift
//  PitStop
//
//  Created by Angela Yu on 29/08/2015.
//  Copyright (c) 2015 London App Brewery. All rights reserved.
//

import UIKit
import Firebase

class ChatViewController: UIViewController {
    
    // Declare instance variables here

    
    // We've pre-linked the IBOutlets
    @IBOutlet var heightConstraint: NSLayoutConstraint!
    
    @IBOutlet weak var BeginPitstop: UIButton!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        BeginPitstop.layer.cornerRadius = 10
        
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
        
        //TODO: Log out the user and send them back to WelcomeViewController
        do {
            try Auth.auth().signOut()
            navigationController?.popToRootViewController(animated: true)
        } catch {
            print("Error, there was a problem signing out")
        }
        
    }
    


}
