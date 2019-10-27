//
//  ViewController.swift
//  PitStop
//
//  Created by Peter Huang on 26/10/2019.
//

import UIKit
import Firebase
//import PythonKit

class PrePitstopViewController: UIViewController {

    @IBOutlet var heightConstraint: NSLayoutConstraint!
    
    @IBOutlet weak var BeginPitstop: UIButton!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        BeginPitstop.layer.cornerRadius = 10
        
        let pkA = PythonTesterA.init()
        pkA.loadSimpleFn()
        //pkA.numpyTest()
        //pkA.tester2()
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
