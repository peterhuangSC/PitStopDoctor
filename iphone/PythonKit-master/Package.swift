// swift-tools-version:5.0

import PackageDescription

let package = Package(
    name: "PythonTool",
    products: [
        .executable(
            name: "PythonTool",
            targets: ["PythonTool"]
        ),
        .library(
            name: "PythonKit",
            targets: ["PythonKit"]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/pvieito/CommandLineKit.git", .branch("master")),
        .package(url: "https://github.com/pvieito/LoggerKit.git", .branch("master")),
        .package(url: "https://github.com/pvieito/PythonKit.git", .branch("master"))
    ],
    targets: [
        .target(
            name: "PythonTool",
            dependencies: ["LoggerKit", "CommandLineKit", "PythonKit"],
            path: "PythonTool"
        ),
        .target(
            name: "PythonKit",
            path: "PythonKit"
        ),
        .testTarget(
            name: "PythonKitTests",
            dependencies: ["PythonKit"]
        ),
    ]
)
