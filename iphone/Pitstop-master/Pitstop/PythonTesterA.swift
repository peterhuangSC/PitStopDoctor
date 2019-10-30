//
//  PythonTesterA.swift
//  Pitstop
//
//  Created by Peter Huang on 2019-10-27.
//


import Foundation
import PythonKit
//import Python

class PythonTesterA {
    func loadSimpleFn() {
        print("abcde")
    }
    
    func numpyTest() {
        let np = Python.import("numpy") //import numpy as np
        let arrA = np.array([4, 3, 7])
        let arrB = np.array([9, 3, 5])
        let result = arrA * arrB
        print(result)
        //[36 9 35]
    }
    
    
//    func tester2() {
//        let sys = try Python.import("sys")
//
//        print("Python \(sys.version_info.major).\(sys.version_info.minor)")
//        print("Python Version: \(sys.version)")
//        print("Python Encoding: \(sys.getdefaultencoding().upper())")
//    }
    
    
//    func fatigueChecker() {
//        let sys : PythonObject = Python.import("sys")
//        sys.path.append("/Users/peterhuang/")
//    }
}
