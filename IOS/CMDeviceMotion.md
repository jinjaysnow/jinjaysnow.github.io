```Swift 
import CoreMotion
```

# CMDeviceMotion
CMDeviceMotion产生的是经过处理的数据。
```Swift
// 初始化资源管理者
var manager = CMMotionManager()
// 查询设备是否可用
if manager.deviceMotionAvailable {
    // 设置设备数据更新间隔
    manager.deviceMotionUpdateInterval = updateInterval
    // 开始获取数据
    manager.startDeviceMotionUpdatesToQueue(NSOperationQueue.mainQueue(), withHandler: {data, error in
        if !error {
            print("设备姿态: \(manager.deviceMotion.attitude)")
            print("旋转率: \(manager.deviceMotion.rotationRate)")
            print("加速度数据(重力+用户施加的加速度): \(manager.deviceMotion.gravity)")
            print("用户施加的加速度: \(manager.deviceMotion.userAcceleration)")
            print("归一化的磁场数据(地磁+周围环境磁场-设备自身偏差):\(manager.deviceMotion.magneticField)")
        }
        // 停止获取数据
        manager.stopDeviceMotionUpdates()
    })
}
```

# CMAltimeter
产生与高度相关的原始数据。产生的相对高度，而不是绝对高度值。
```Swift 
if CMAltimeter.isRelativeAltitudeAvailable() {
    var altimeter = CMAltimeter()
    // 开始获取相对的高度数据data: CMAltimeterData
    altimeter.startRelativeAltitudeUpdatesToQueue(NSOperationQueue.mainQueue(),{data, error in
        if !error {
            print("相对高度:\(data.relativeAltitude)")
            print("气压:\(data.pressure)")
        }
    })
}
// 结束获取数据
altimeter.stopRelativeAltitudeUpdates()
```

# CMAttitude
产生于设备姿态相关的原始数据。通过CMDeviceMotion来获取数据。
```Swift 
var attitude = manager.deviceMotion.attitude
print("欧拉角表示: \(attitude.roll), \(attitude.pitch), \(attitude.yaw)")
print("四元数表示: \(attitude.quaternion)")
```

# CMPedometer
产生计步数据。
```Swift 
CMPedometer.isStepCountingAvailable() // 计步器
CMPedometer.isDistanceAvailable()     // 距离
CMPedometer.isFloorCountingAvailable()// 楼层计数
var pedometer = CMPedometer()
pedometer.startPedometerUpdatesFromDate(start: Date, handler: CMPedometerHandler) // 从某一个日期开始的计步数据
pedometer.stopPedometerUpdates()      // 停止计数数据的更新
```


# 