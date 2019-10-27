//
//  PythonTesterA.swift
//  Pitstop
//
//  Created by Peter Huang on 2019-10-27.
//

//import Cocoa
import Foundation

class PythonTesterA {
    func loadSimpleFn() {
        print("abcde")
    }
    
    func numpyTest() {
        let np = Python.import("numpy")
        let arrA = np.array([4, 3, 7])
        let arrB = np.array([9, 3, 5])
        let result = arrA * arrB
        print(result)
        //[36 9 35]
    }
    
    func fatigueChecker() {
        let sys : PythonObject = Python.import("sys")
        sys.path.append("/Users/peterhuang/")
    }
}
