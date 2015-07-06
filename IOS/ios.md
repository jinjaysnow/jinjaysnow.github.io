<h1 align="center">iOS应用开发流程</h1>

[TOC]

# 获取工具
在开发之前，需要搭建开发环境，获取开发工具。

开发iOS应用，需要以下工具：
1. Mac电脑
2. Xcode
3. iOS SDK(一般由Xcode自带)

> 注，本教程中使用的是Xcode7 beta版，编写时Xcode7还没有正式发布。

Xcode是苹果的集成开发环境，包括源代码编辑器，图形用户界面编辑器，和其它的功能。iOS SDK作为Xcode的扩展，包括开发iOS应用的一系列工具，编译器，和库函数。
![安装工具](https://developer.apple.com/library/ios/referencelibrary/GettingStarted/RoadMapiOS/Art/install_tools_2x.png)

在App Store中查找Xcode，并点击下载，不到3GB的大小。

# 编程语言
当前，苹果官方的开发语言有两种：Objective-C 和 Swift。Swift是苹果力推的编程语言，所以为了App应用未来的发展，建议使用Swift进行开发。本文主要使用Swift展示如何进行iOS应用开发，针对目前Objective-C上有更多第三方库，后面会讲解如何进行Swift与Object-C的混合编程。因此，为了更好的学些本教程，需要了解Swift和Objective-C语言的基本特性，比如基本类型(int, float...)，数据结构，函数，控制流(while, if...else和for语句等等)。下面介绍Swift语言的基本知识。

## Swift语言
### Playground
使用Playground学习Swift十分友好，Playground是Xcode自带的工具。

#### 新建Playground
1. 打开Xcode，选择Get started with a playground
    <center>![](http://jinjaysnow.github.io/IOS/p1.png)</center>
2. 输入文件名,并点击next
    <center>![](http://jinjaysnow.github.io/IOS/p2.png)</center>
3. 选择需要放置文件的位置后，点击create，创建新文件。
    <center>![](http://jinjaysnow.github.io/IOS/p3.png)</center>

进入编辑模式，左侧为代码编辑区，右侧为实时的运算结果。接下来介绍的Swift基本知识的代码都可以在左侧代码编辑区编写。

### 基本类型
*常量* 是在第一次声明后保持不变的一个值， *变量*是可以改变的值。程序中，如果你知道一个值不会在代码中更改，请使用常量而不是变量。

在Swift中使用`let`定义常量，`var`定义变量。

```Swift
var myVariable = 42
myVariable = 50
let myConstant = 42
```

在Swift中每一个常量和变量都有一个类型，但是你不需要显示的声明类型。编译器会自动推断出常量或变量的类型。在上面的例子中，编译器会把myVariable推断为 整型 。**一旦常量或变量拥有了类型，就不可更改。**

我们可以在变量名后添加类型信息，以免造成编译器的错误推断。如下：

```Swift
let explicitDouble: Double = 70
```

需要将变量转换为另一个类型是，需要显式地进行转换。如下：

```Swift
let label = "The width is"
let width = 94
let widthLabel = label + String(width)
```

使用 `可选(optionals)` 来表示变量值可能不存在。一个可选值表示要么包含一个值，要是是空值(nil)。可选的标记是在类型后面添加 `?` 。

```Swift
let optionalInt: Int? = 9
```

> optionalInt 要么是Int，要么是nil，不能是其他类型

从可选值中获取信息，需要对可选值进行拆包，最直接的方法是在变量后加入拆包符 `!` 。只有在你确定可选值不为`nil`的时候才可以使用拆包运算符。

```Swift
let actualInt: Int = optionalInt!
```

可选在Swift中十分常见。在进行类型转换时十分有用。

```Swift
var myString = "7"
var possibleInt = Int(myString)
print(possibleInt)
```

上述代码中，`possibleInt`的值是7，因为`myString`包含整形数值，但是，当你把`myString`的值更改为其他不能转换为整型的值是，`possibleInt`的值会变为`nil`。
```Swift
myString = "banana"
possibleInt = Int(myString)
print(possibleInt)
```

*数组* 使用`[]`创建数组，通过索引值访问元素，数组的索引值从`0`开始。
```Swift
var ratingList = ["Poor", "Fine", "Good", "Excellent"]
ratingList[1] = "OK"
ratingList
```
创建空数组，请使用初始化语法。
```Swift
// Creates an empty array.
let emptyArray = [String]()
```

上述代码中出现了注释，在Swift中单行注释使用`//`,多行注释使用`/* ... */`。

*隐式可选值* 是一种可以像非可选值那样使用的可选值，它不需要在每一次访问它的时候进行拆包。因为隐式可选值被假定为在值被初始化后总是拥有值，尽管值能够改变。隐式可选值的声明是在类型后使用`!`代替`?`。
```Swift
var implicitlyUnwrappedOptionalInt: Int!
```
在代码中，你几乎不会使用隐式可选值。

### 控制流
Swift有两种类型的控制流声明：条件语句(`if` `switch`)；循环语句(`for-in` `while`)。

```Swift
let number = 23
if number < 10 {
    print("The number is small")
} else if number > 100 {
    print("The number is pretty big")
} else {
    print("The number is between 10 and 100")
}
```

```Swift
let individualScores = [75, 43, 103, 87, 12]
var teamScore = 0
for score in individualScores {
    if score > 50 {
        teamScore += 3
    } else {
        teamScore += 1
    }
}
print(teamScore)
```
可以使用单一的`if`语句绑定多个值，`where`子句追加到后面来进一步检验条件语句。如下所示：
```Swift
var optionalHello: String? = "Hello"
if let hello = optionalHello where hello.hasPrefix("H"), let name = optionalName {
    greeting = "\(hello), \(name)"
}
```

`switch`在swift中很强大，支持任意的类型和比较操作————它不限制为整型和相等比较。
```
let vegetable = "red pepper"
switch vegetable {
case "celery":
    let vegetableComment = "Add some raisins and make ants on a log."
case "cucumber", "watercress":
    let vegetableComment = "That would make a good tea sandwich."
case let x where x.hasSuffix("pepper"):
    let vegetableComment = "Is it a spicy \(x)?"
default:
    let vegetableComment = "Everything tastes good in soup."
}
```

半开区间运算符 `..<`, 闭区间运算符`...`, 通配符 '_'
```Swift
var firstForLoop = 0
for i in 0..<4 { // 4次
    firstForLoop += i
}
print(firstForLoop)

var secondForLoop = 0
for _ in 0...4 { // 5次
    secondForLoop += 1
}
print(secondForLoop)

```

### 函数和方法
*函数*是一个可以重用的命名的代码段，能够在程序中被引用。声明函数使用 `func`。函数可以包含0或多个参数，参数格式为 `参数名: 类型 (name: Type)`，函数可以有返回值或没有，使用 `->` 表示。如下：
```Swift
func greet(name: String, day: String) -> String {
    return "Hello \(name), today is \(day)."
}
```
函数调用时，第一个参数不需要写参数名，后面的参数需要写参数名，如下：
```Swift
greet("Anna", day: "Tuesday")
greet("Bob", day: "Friday")
greet("Charlie", day: "a nice day")
```
*方法*是与特定类型定义在一起的特殊函数。可以将方法看作是类的静态函数。
```Swift
let exampleString = "hello"
if exampleString.hasSuffix("lo") {  // hasSuffix()为方法
    print("ends in lo")
}
```

### 类及初始化
使用`class` 定义类。类属性声明为在类中的常量和变量声明。方法和函数声明写法相同。
```Swift
class Shape {
    var numberOfSides = 0
    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}

var shape = Shape() // 实例化一个类
shape.numberOfSides = 7 // 使用.语法访问实例的属性和方法
var shapeDescription = shape.simpleDescription()
```
上面的例子中，Shape类缺少重要的初始化方法。下面的例子给出一个带有初始化方法的类定义：
```Swift
class NamedShape {
    var numberOfSides = 0
    var name: String
    
    init(name: String) {
        self.name = name
    }
    
    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}
```
可以看到，我们使用self来分辨是否是类属性。初始化是通过类名调用，不需要调用init函数。调用时需要写所有的参数名。
```Swift
let namedShape = NamedShape(name: "my named shape")
```
*继承* 中，需要重写父类的实现时，使用`override`关键字。
```Swift
class Square: NamedShape {
    var sideLength: Double

    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 4
    }

    func area() -> Double {
        return sideLength * sideLength
    }

    override func simpleDescription() -> String {
        return "A square with sides of lenghth \(sideLength)."
    }
}
let testSquare = Square(sideLength: 5.2, name: "my test square")
testSquare.area()
testSquare.simpleDescription()
```
有时候会出现实例化失败的情况，比如给一个圆形的半径赋值为负。可以使用`init?`来声明可能失败的初始化。
```Swift
class Circle: NamedShape {
    var radius: Double
    
    init?(radius: Double, name: String) {
        self.radius = radius
        super.init(name: name)
        numberOfSides = 1
        if radius <= 0 {
            return nil
        }
    }
    
    override func simpleDescription() -> String {
        return "A circle with a radius of \(radius)."
    }
}
let successfulCircle = Circle(radius: 4.2, name: "successful circle")
let failedCircle = Circle(radius: -7, name: "failed circle")
```
初始化还可以使用`designated`和`convenience`来修饰，designated是最基本的初始化，一个类的任何初始化方法都必须调用它；convenience是二级初始化方法，可以用来添加额外的行为和自定义信息，但它最终仍会调用designated初始化。`required`关键字表明类的子类必须实现它自己的相应的初始化方法。

*类型转换* 可以使用类型转换符向下转换为子类类型。由于向下转换可能会失败，所以类型转换有两种形式。可选形式 `as?`，返回你试图向下转换的类型的可选值。强制形式 `as!`，试图向下转换并强制拆包。在你不确定是否能够转换成功的时候使用`as?`,如果不能转换会返回`nil`，你可以进一步进行判断。在你十分确定向下转换能够成功的时候使用`as!`
```Swift
class Triangle: NamedShape {
    init(sideLength: Double, name: String) {
        super.init(name: name)
        numberOfSides = 3
    }
}
 
let shapesArray = [Triangle(sideLength: 1.5, name: "triangle1"), Triangle(sideLength: 4.2, name: "triangle2"), Square(sideLength: 3.2, name: "square1"), Square(sideLength: 2.7, name: "square1")]
var squares = 0
var triangles = 0
for shape in shapesArray {
    if let square = shape as? Square {
        squares++
    } else if let triangle = shape as? Triangle {
        triangles++
    }
}
print("\(squares) squares and \(triangles) triangles.")
```

### 枚举和结构体
使用`enum`来创建枚举。
```Swift
enum Rank: Int {
    case Ace = 1
    case Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten
    case Jack, Queen, King
    func simpleDescription() -> String {
        switch self {
        case .Ace:
            return "ace"
        case .Jack:
            return "jack"
        case .Queen:
            return "queen"
        case .King:
            return "king"
        default:
            return String(self.rawValue)
        }
    }
}
let ace = Rank.Ace
let aceRawValue = ace.rawValue
```
上例中，枚举的原值类型为 `Int`，所以你必须给出第一个原值。其余的值会按序自动赋值。你也可以使用浮点数作为枚举的原值类型。使用 `rawValue`来访问枚举成员的原值。

使用 `init?(rawValue:)` 初始化方法来从原值制造枚举的一个实例。
```Swift
if let convertedRank = Rank(rawValue: 3) {
    let threeDescription = convertedRank.simpleDescription()
}
```
事实上，枚举的成员值是实际的值，并不仅仅是书写它们原值的另一种方式。你可以不提供原值，也可以使用枚举。
```Swift
enum Suit {
    case Spades, Hearts, Diamonds, Clubs
    func simpleDescription() -> String {
        switch self {
        case .Spades:           // 缩写形式，self已知为Suit
            return "spades"
        case .Hearts:
            return "hearts"
        case .Diamonds:
            return "diamonds"
        case .Clubs:
            return "clubs"
        }
    }
}
let hearts = Suit.Hearts
let heartsDescription = hearts.simpleDescription()
```

*结构体*支持很多与类相同的行为，包括方法和初始化。类与结构体最重要的区别之一是：结构体在你的袋中中传递时总是可以被复制，然而类是传引用。结构体用来定义不需要继承和类型转换的轻量级的数据类型。
```Swift
struct Card {
    var rank: Rank
    var suit: Suit
    func simpleDescription() -> String {
        return "The \(rank.simpleDescription()) of \(suit.simpleDescription())"
    }
}
let threeOfSpades = Card(rank: .Three, suit: .Spades)
let threeOfSpadesDescription = threeOfSpades.simpleDescription()
```

### 协议
*协议(protocol)* 定义完成特定的任务或功能的方法、属性和其它要求的蓝本。协议并不提供任何实现，只是描述应该做什么。协议可以被类、结构体或者枚举采用来提供对这些需求的实际的实现。任何满足一个协议的需求的类型都称为遵守该协议。使用`protocol`来定义协议。
```Swift
protocol ExampleProtocol {
    var simpleDescription: String { get }
    func adjust()
}
```
> `{ get }` 表明该属性只读，也即只能查看不能更改。

实现协议与继承格式类似，当一个类继承父类并实现一个协议时，需要将父类写在协议前面。
```Swift
class SimpleClass: ExampleProtocol {
    var simpleDescription: String = "A very simple class."
    var anotherProperty: Int = 69105
    func adjust() {
        simpleDescription += "  Now 100% adjusted."
    }
}
var a = SimpleClass()
a.adjust()
let aDescription = a.simpleDescription
```
协议是第一类类型，这意味着它们可以被看做是命名类型。比如你可以创建一个协议数组。
```Swift
class SimpleClass2: ExampleProtocol {
    var simpleDescription: String = "Another very simple class."
    func adjust() {
        simpleDescription += "  Adjusted."
    }
}
 
var protocolArray: [ExampleProtocol] = [SimpleClass(), SimpleClass(), SimpleClass2()]
for instance in protocolArray {
    instance.adjust()
}
protocolArray
```

### Swift与Cocoa Touch
Cocoa Touch是用来开发iOS应用的开发框架。最经常使用的框架是UIKit，它包含了很多UI层的类。通过导入来使用这些类。更多框架信息可以查阅苹果公司的应用开发手册。
```Swift
import UIKit
```

# 第一个项目————膳食跟踪
## 创建新工程
1. 打开Xcode，出现Xcode的初始界面
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_welcomewindow_2x.png)</center>
2. 在初始界面，点击"Create a new Xcode project"新建一个工程
    这一步后，Xcode会让你显示对话框让你选择一个模版。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_singleviewapp_template_2x.png)</center>
3. 在对话框中点击左侧iOS栏下的Application，选择"Single View Applicaiton"单一视图应用,并点击"Next"进入下一步
4. 弹出新的对话框，在这一个界面设置项目的基本参数
    Product Name: 项目名
    Organization Name: 组织名或你自己的名字，可以留空
    Organization Identifier: 组织的标志符，如果有的话就填写，没有就填默认的com.example
    Bundle Identifier: 自动产生，不需要填写
    Language: 编程语言，选择Swift
    Devices: 应用运行平台，可选iPhone或iPad或Universal(通用)
    Use Core Data: 是否使用内核数据，主要用于数据持久化存储，此处我们不选择
    Include Unit Tests: 是否使用单元测试，此处我们选择
    Include UI Tests: 是否使用UI测试，此处不选择
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_newproject_2x.png)</center>
5. 点击"Next"，弹出对话框，选择你需要将工程保存的位置，并点击"Create"
    Xcode会打开新的工程如下所示。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_workspacewindow_2x.png)</center>

## 熟悉Xcode
Xcode工作空间布局如下：
<center>![](http://jinjaysnow.github.io/IOS/w.png)</center>

## 运行模拟器
iOS模拟器可以模拟多种设备，在开发中经常使用。新建的工程可以直接在模拟器中运行，在模拟器中运行App有以下步骤。
1. 在工具栏的Scheme菜单中选择设备，此处选择iPhone6.
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_schememenu_2x.png)</center>
2. 点击工具栏左上角的运行按钮，或者快捷键操作(Command+r)
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_toolbar_2x.png)</center>
    第一次运行，Xcode会询问是否在Mac上开启开发者模式。请点击Enable允许。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_developermode_2x.png)</center>
3. 在工具栏上可以看到构建的进度。

在Xcode完成构建后，模拟器会自动运行，第一次打开会消耗一些时间。加载App后，你会见到如下的开始界面：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_sim_launchscreen_2x.png)</center>
然后，你会看到应用主界面：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_sim_blank_2x.png)</center>

目前为止，应用只是展示了一个白色的屏幕。

## 查看源代码
查看AppDelegate.swift 
1. 确保导航区的工程导航为打开状态
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_projectnavigator_2x.png)</center>
2. 如果必要，点击左侧的三角形以打开FoodTracker文件夹
3. 选择AppDelegate.swift
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_appdelegate_file_2x.png)</center>

此外，如果双击AppDelegate.swift，会在另外一个窗口打开该文件。

## 解析AppDelegate.swift文件
AppDelegate.swift包含两个主要功能:
· 它创建App的入口和一个运行循环将输入事件转发给App。这个工作是通过`UIApplicationMain`属性完成的(`@UIApplicationMain`)。UIApplicationMain 创建一个负责管理App的生命周期的应用对象和App delegate对象。
· 它定义了AppDelegate类。App delegate创建一个窗口(window)，在window上进行应用的内容绘制并提供响应应用内部的状态转换的场所。`AppDelegate`类是编写自定义的App级代码的地方。

AppDelegate包含一个单一属性`window`。通过这个属性，App追踪应用内容绘制的窗口。这个属性是可选的，意味着在某些时刻可能为nil。AppDelegate也包含几个预定义的方法来允许应用对象能够与App Delegate进行交互。
```Swift
func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool
func applicationWillResignActive(application: UIApplication)
func applicationDidEnterBackground(application: UIApplication)
func applicationWillEnterForeground(application: UIApplication)
func applicationDidBecomeActive(application: UIApplication)
func applicationWillTerminate(application: UIApplication)
```
在App的状态转换过程中，应用对象会调用App Delegate中相应的方法来合适地响应。

## 应用程序的生命周期
### 应用程序的结构
应用开启后，UIApplicationMain会设置一系列的关键对象并开启运行循环。在每一个iOS应用中核心是UIApplication对象，它能够促进系统与应用中的其他对象进行交互。下图展示了在大多数应用中存在的对象。这其中需要注意的是iOS应用使用MVC架构。这个模式将应用的数据和业务逻辑分开。
<center>![](https://developer.apple.com/library/ios/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/Art/core_objects_2x.png)</center>

对象 | 描述
-----|-----
UIApplication | *UIApplication对象* 管理事件循环和高层次的app行为。它也将关键的app状态转换和特殊事件(如推送)告知它的代理(delegate)，这个代理可以自定义。直接使用UIApplication不需要子类化。
App Delegate | *应用程序代理对象* 是自定义代码的核心。它与UIApplicatin对象一起处理app初始化，状态转换和高层次的app事件。在每一个app中只有一个对象，所以通常它被用来设置应用程序的初始数据结构。
Documents and data model | *数据模型对象* 存储app的内容。App可以使用文档对象(`UIDocument`)来管理数据模型对象。文档对象并不是必须的，但是提供了一个便利的方式来组织数据。
View Controller | *视图控制器对象* 管理App在屏幕上的内容的呈现。一个视图控制器管理一个视图及其子视图。`UIViewController`类是所有视图控制器对象的基类。它提供了默认的函数集，包括加载视图、呈现视图、根据设备方向旋转视图及其他标准的系统行为。`UIKit`和其他的框架定义了额外的视图控制类以实现标准系统交互界面，比如图像选择器、导航条、工具栏。
UIWindow | UIWindow对象协调在屏幕上的一个或多个视图。大多数的app只有一个window，有些应用可以在外部显示器上使用额外的window展示内容。
View, Control, layer | 视图是在一个特定的矩形区域进行绘制内容和响应事件的对象。控制是视图的特定类型，负责实现特定功能比如按钮、文本域和开关。Layer层对象实际上是代表可视化内容的数据对象。视图使用层对象来渲染内容。可以添加自定义的层来实现复杂的动画和视觉效果。

<center>![](https://developer.apple.com/library/prerelease/ios/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/Art/view-layer-store.jpg)</center>

### 运行循环
<center>![](https://developer.apple.com/library/ios/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/Art/event_draw_cycle_a_2x.png)</center>
上图展示了运行循环的架构与用户事件如何在app中被响应。在用户与设备进行交互时，与这些交互相关的事件会被系统产生并通过特殊的端口分发给应用。事件会在app内部形成队列，然后一个接一个分发给运行循环进行处理。`UIApplication`对象是第一个接收到事件的对象，它会决定该做些什么。一个触摸事件通常会被分发给主窗口对象，然后结果分发给触摸区域的视图。在iOS系统中存在很多事件，下表介绍了一些常用的事件。

事件类型 | 分发给.. | 注释
--------|----------|----------
触摸 | 事件发生的那个视图 | 视图是响应对象。任何没有被视图处理的事件会向响应链的下一个传递以进行处理。
远程控制、摇动事件 | 第一级响应对象 | 远程控制事件用于媒体回放，暂停等，由耳机和其它配件产生。
加速计、磁力计、陀螺仪 | 你指定的对象 | 与加速计、磁力计和陀螺仪等硬件相关的事件会传递给你指定的对象。
定位 | 你指定的对象 | 使用Core Location framework来注册接收定位事件。
重绘 | 需要更新的视图 | 重绘事件并不需要事件对象，只是告知视图需要绘制。

### App运行状态

状态 | 描述
----|-----
Not Running | 未运行，app还没有启动，或者被系统终止了
Inactive | 不活跃，app运行在前台，但是当前没有收到事件。(可能正在处理其它的代码)在没有事件处理情况下程序通常停留在这个状态
Active | 活跃，程序在前台运行而且接收到了事件。是前台的一个正常的模式
Backgroud | 后台，程序在后台而且能执行代码，大多数程序进入这个状态后会在在这个状态上停留一会。时间到之后会进入挂起状态(Suspended)。有的程序经过特殊的请求后可以长期处于Backgroud状态
Suspended | 挂起，程序在后台不能执行代码。系统会自动把程序变成这个状态而且不会发出通知。当挂起时，程序还是停留在内存中的，当系统内存低时，系统就把挂起的程序清除掉，为前台程序提供更多的内存。

iOS应用状态转换图
<center>![](https://developer.apple.com/library/ios/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/Art/high_level_flow_2x.png)</center>

`func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool`这个方法是应用启动时执行代码的地方。
`func applicationWillResignActive(application: UIApplication)`应用即将进入非活跃状态，在此期间，应用程序不接受消息或事件，比如来电话了。
`func applicationDidEnterBackground(application: UIApplication)`应用被推送到后台时调用，所以要设置后台继续运行，需要在这个函数李金星设置。
`func applicationWillEnterForeground(application: UIApplication)`应用从后台将要重新回到前台时调用。
`func applicationDidBecomeActive(application: UIApplication)`应用进入活跃状态，成为前台app。
`func applicationWillTerminate(application: UIApplication)`应用将被终止，需要进行保存数据等操作。

加载应用程序进入前台：
<center>![](http://img.my.csdn.net/uploads/201209/29/1348884482_7300.png)</center>

加载应用程序进入后台：
<center>![](http://img.my.csdn.net/uploads/201209/29/1348884525_3194.png)</center>

响应中断：
<center>![](http://img.my.csdn.net/uploads/201209/29/1348885212_1391.png)</center>

转到后台运行：
<center>![](http://img.my.csdn.net/uploads/201209/29/1348886673_9662.png)</center>


返回前台运行：
<center>![](http://img.my.csdn.net/uploads/201209/29/1348889472_5280.png)</center>

## 关于ViewController.swift
了解了App的生命周期后，继续来看第一个项目。ViewController.swift定义了一个UIViewController的子类ViewController。当前这个类仅仅只是继承了所有的父类的行为。

## Storyboard文件
Storyboard文件是应用的用户接口的可视化表示，它可以呈现内容屏幕和屏幕之间的切换。打开Main.storyboard文件，看到的界面如下：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_storyboard_empty_2x.png)</center>

## 构建基本UI
接下来开始构建一个基本的用户界面。Xcode提供了很多基础库，能够添加到Storyboard文件中。一些是UI元素比如按钮和文本域，另一些是定义屏幕上app行为的元素比如视图控制器和手势识别器。所有的视图对象都是`UIView`类型或其子类类型。下面开始添加UI元素。

### 添加一个文本域到场景中
1. 打开对象库
    对象库(Object Library)在Xcode功能区的右下角。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/object_library_2x.png)</center>
    对象库是一个显示对象的名称、描述和可视化示例的列表。
2. 在对象库中，下方的搜索栏中输入 text field 来快速查找文本域对象。
3. 将文本域对象拖动到场景中。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_textfield_drag_2x.png)</center>
4. 拖动文本域以使它与场景的左侧对齐。对齐后停止拖动应该看到如下的视图。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_textfield_place_2x.png)</center>
    蓝色的布局线提示你放置文本域。在上图中，这条蓝色的布局线表示场景的最左侧。
5. 如果必要，可以点击文本域改变文本域的大小。
    一般通过拖拉UI元素边界上的调整大小图柄来改变大小。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_textfield_resizehandles_2x.png)</center>
6. 将文本域的左右边界与视图的左右编辑对齐成如下状态。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_textfield_finalsize_2x.png)</center>

尽管在视图层中已经布置了文本域，但是并没有任何提示用户输入什么的信息。这里使用文本域的`placeholder`属性来体术用户输入菜品的名称。

### 配置文本域的placeholder文本
1. 在视图中选中文本域，在功能区打开属性编辑器。
    通过点击功能区最上方的第四个按钮来打开属性编辑器，属性编辑器允许你编辑Storyboard中的对象的属性。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_inspector_attributes_2x.png)</center>
2. 在属性编辑器中，找到Placeholder属性，然后键入“Enter meal name”（请输入食物名称）。
3. 按下回车键以确认修改并会在文本域上显示placeholder文本。

完成上述步骤，视图应该如下图所示：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_textfield_withplaceholder_2x.png)</center>

### 配置文本域的键盘布局
1. 确保文本域处于选中状态。
2. 在属性编辑器中，找到`Return Key`标签域，并选择`Done`。
    这一步会改变默认的 Return 键的显示内容，会更改为`Done`。
3. 在属性编辑器中，选中`Auto-enable Return Key`。
    这一步会保证用户不能输入空值，即必须输入数据才能点按`Done`键。

### 在场景中添加一个标签
1. 在对象库中查找 label 对象。
2. 将标签对象拖动到场景中。
3. 拖动标签对象以使得它的左侧与场景左侧对齐，并刚好处于文本域的上方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_label_place_2x.png)</center>
4. 双击标签并输入"Meal Name"(食物名称)。
5. 按下回车键确认并在标签上显示文本。

<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_label_rename_2x.png)</center>

### 添加一个按钮
1. 在对象库中，查找 button 对象。
2. 拖动按钮对象到场景中。
3. 拖动按钮到如下图所示的位置。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_button_place_2x.png)</center>
4. 双击按钮，并输入"Set Default Label Text"(设置默认标签)。
5. 按下回车键确认并在按钮上显示文本。

<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_button_rename_2x.png)</center>

### 查看大纲视图
1. 在Storyboard中找到大纲视图开关。
    <center>![](http://jinjaysnow.github.io/IOS/outline.png)</center>
2. 如果大纲视图是关闭状态，点击大纲视图开关以打开大纲视图。

在画布左侧的大纲视图展示了在故事板中的对象的层级关系。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_outlineview_2x.png)</center>

### 预览用户界面
间断地预览以保证界面如你希望的那样。可以通过使用 "Assistant Editor"（辅助编辑器）来预览用户界面，在这一界面可以将主编辑器平分为两个。

1. 点击Xcode工具栏上的辅助编辑器按钮来打开辅助编辑器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/assistant_editor_toggle_2x.png)</center>
2. 如果需要更多的显示空间，可以点按导航栏开关和功能区开关来关闭两个区域。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/navigator_utilities_toggle_on_2x.png)</center>
3. 在辅助编辑器上方的编辑器选择栏处，切换辅助编辑器的显示，从 Automatic 到 Preview \> Main.storyboard(Preview)。

<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_assistant_editorselectorbar_2x.png)</center>

在辅助编辑器中会看到文本域并不是处于想要的位置。这是为什么呢？
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_preview_2x.png)</center>

事实上，当前我们编辑的是给不同大小的iPhone和iPad编辑的自适应用户界面。编辑时默认看到的是用户界面的通用版本。这里，我们需要配置用户界面如何根据不同的屏幕大小来自适应调整。比如界面缩小到iPhone的大小时，文本域也应该缩小；界面放大到iPad的大小时，文本域也应该放大。我们可以通过"Auto Layout"技术来进行配置。

### 自动布局Auto Layout
自动布局是一个能够帮助你自适应布局的功能强大的布局引擎。通过描述元素在场景中的位置，布局引擎来决定如何最好的呈现出来。一般是通过`constraints`(约束)来描述你的意图，这个约束通常是描述一个元素如何相对另一个元素进行定位，大小如何或者在空间减少时两个元素中哪一个应该缩小。

结合自动布局，一个有用的工具是堆栈视图(`UIStackView`)。堆栈视图提供了一个流线型的界面，以使大量的师徒布局在一行或一列中。堆栈视图可以帮助你利用自动布局的强大功能，创造出能够自适应设备方向、屏幕大小和可用空间不断改变的用户界面。

#### 给场景添加自动布局约束
1. 点击标准按钮以返回标准编辑器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/standard_toggle_2x.png)</center>
    打开导航栏和功能区。
2. 按住键盘上的`Shift`键，用鼠标选择文本域、标签和按钮。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_shift_select_2x.png)</center>
3. 在画布的右下角，点击堆栈按钮。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_stackmenu_2x.png)</center>
    Xcode会将UI元素自动打包。Xcode还会分析你已经存在的布局并指出对象应该竖直放置而不是水平。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_stack_2x.png)</center>
4. 如果必要，打开大纲视图，选中堆栈视图对象。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_outlineview_2x.png)</center>
5. 在属性编辑器中，找到Spacing标签，输入12，并按回车键。
    可以看到UI元素自动垂直布局，并且堆栈视图自动变化了。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_stackspaced_2x.png)</center>
6. 在画布的右下角，打开 `Pin` 菜单
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_pinmenu_2x.png)</center>
7. 在"Spacing to nearest neighbor"上方，点击两个水平约束，和上方的垂直约束以选中它们。在选中后会变为红色。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_pinconstraints_2x.png)</center>
    这些约束是指距离最近左侧邻元素、右侧邻元素和上方邻元素的空白距离。
8. 设置左右约束的值为0，上方约束的值为60。
9. 在菜单的 `Update Frames`处，选择 `Items of New Constraints`。
    此时 Pin 菜单应该如下所示：
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_stackconstraints_2x.png)</center>
10. 在Pin 菜单中，点击 "Add 3 Constraints"按钮以使约束生效。

完成后，食谱场景应该如下所示。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_stackfinal_2x.png)</center>

应该注意到，文本域并没有伸展到场景的边界处，所以需要进行修改。

#### 调整场景中的文本域的宽度
1. 在Storyboard中，选中文本域。
2. 在画布的右下角，打开 Pin 菜单。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/AL_pinmenu_2x.png)</center>
3. 在"Spacing to nearest neighbor"的上方，选择两个水平约束，选中后会变为红色。
4. 在左右约束处输入0。
5. 在"Update Frames"标签处，选择"Items of New Constraints"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_textfieldconstraints_2x.png)</center>
6. 在Pin菜单中，点击"Add 2 Constraints"按钮。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_add2constraints_2x.png)</center>
7. 保持文本域选中的状态，打开位于功能区的大小指示器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_inspector_size_2x.png)</center>
8. 在"Intrinsic Size"(内部大小)域处，选择"Placeholder"。(这个域在大小指示器的底部，需要滚动到下方才能看到)
    这里，文本域会根据内容自动调整大小，内部大小指的是需要显示所有内容的最小的大小。当前文本域的内容是占位字符串，但是实际中用户输入的文本可能会比这个更长。

现在，场景UI应该如下图所示：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_textfieldfinal_2x.png)</center>

***检查点：***现在在模拟器中运行你的应用。文本域不会再查出屏幕的边界了。点击文本域内部并输入文本（你可以通过按下`Command+K`来打开软键盘）。通过旋转设备(`Command+←`或者`Command+→`)查看自动布局的效果。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_sim_finalUI_2x.png)</center>

如果并不能获得你期待的效果，可以使用Auto Layout调试功能。点击`Resolve Auto Layout Issues`按钮，然后选择`Reset to Suggested Constraints`来使Xcode更新对你的界面。或者点击`Resolve Auto Layout Issues`按钮，选择`Clear Constraints`来清除所有的约束，然后重新添加约束。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_resolvemenu_2x.png)</center>

## 将UI与代码连结
首先了解Storyboard与代码之间的关系。

在Storyboard里，一个场景代表一个内容屏幕和一个典型的视图控制器。视图控制器实现应用的各种行为。一个视图控制器管理一个单一的内容视图及该视图的子视图。视图控制器协调应用的数据模型与显示数据的视图之间的信息流。Xcode已经创建了一个视图控制器类，`ViewController.swift`，并且将它与Storyboard中的场景连结到一起了。可以通过 `Identity inspector`(标识指示器) 来编辑在Storyboard中的对象的属性，比如该对象属于哪一个类。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_inspector_identity_2x.png)</center>

在运行时，Storyboard会创建一个`ViewController`的实例。在应用中看到的屏幕便会显示你在Storyboard中定义的UI元素和在ViewController.swift中定义的行为。

### 给UI元素创建Outlets
Outlets(连接点)提供了在源代码中引用你在Storyboard中定义的界面对象的方式。按住`Control`键，从Storyboard中选中对象并拖动到源代码文件中即可创建一个Outlet。这个操作会在你的文件中创建一个该对象的属性，让你可以在运行时进行操作。下面是具体的操作。

1. 打开Storyboard文件,`Main.storyboard`。
2. 开启辅助编辑器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/assistant_editor_toggle_2x.png)</center>
3. 如果想要更大的空间进行操作，可以关闭导航栏和功能区。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/navigator_utilities_toggle_on_2x.png)</center>
4. 在辅助编辑器上方的编辑器选择栏处，切换辅助编辑器的显示，从 Preview 到 `Automatic > ViewController.swift`。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_switchtoviewcontroller_2x.png)</center>
5. 在`ViewController.swift`,在ViewController类中添加以下注释：
    `// MARK: Properties`
    `// MARK:`是一个特殊类型的注释，可以帮助你更方便的组织和导航代码。
6. 在Storyboard中，选中文本域。
7. 按住键盘上的`Control`键，选中文本域，并拖动到注释代码的下方，然后停止拖动。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_textfield_dragoutlet_2x.png)</center>
8. 在弹出的对话框中，输入属性名 "nameTextField"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_textfield_addoutlet_2x.png)</center>
9. 点击"Connect"按钮以确定。

Xcode会添加以下代码到ViewController.swift中。
```Swift
@IBOutlet weak var nameTextField: UITextField!
```

解释一下上面发生的事情：`IBOutlet`属性告诉Xcode你从"Interface Builder"中连接了nameTextField属性。`weak`关键字表示这个属性可能为nil。后面的代码表明定义了一个名为nameTextField的UITextField类型的变量。

注意到定义后面的感叹号`!`。感叹号表明这个类型是隐式拆包可选的，即在第一次赋值后总后拥有值。

下面用同样地方式连接标签对象。
1. 在Storyboard中选中标签。
2. `Control`+拖动 从Storyboard的标签处到代码中。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_label_dragoutlet_2x.png)</center>
3. 在弹出的对话框中，输入属性名"mealNameLabel"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_label_addoutlet_2x.png)</center>
4. 点击"Connect"。

Xcode会添加如下代码：
```Swift
@IBOutlet weak var mealNameLabel: UILabel!
```

### 定义执行的动作
iOS应用基于 "event-driven programming"(事件驱动编程)。也即，应用由事件驱动：系统事件和用户动作。这些事件引导app的逻辑执行与数据处理。App对用户动作的响应反映到用户界面上。

创建用户的动作与创建outlet类似：按住`Control`从Storyboard拖动一个特定的对象到视图控制器文件中。接下来就创建一个简单的动作：当用户点击"Set Default Label Text"时，设置标签对象显示的文字为"Default Text"。
1. 在ViewController.swift中，在最后一个`}`前，增加以下注释：
    ```Swift
    // MARK: Actions
    ```
2. 在Storyboard中，选中"Set Default Label Text"按钮。
3. 按住键盘上的"Control"并拖动到刚刚创建的注释下方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_button_dragaction_2x.png)</center>
4. 在弹出的对话框中，在`Connection`处选择`Action`。
5. 设置"Name"为"setDefaultLabelText"。
6. 设置"Type"为"UIButton"。
    你可能会注意到，"Type"的默认值为"AnyObject"。在Swift中，"AnyObject"是一个用来描述可以属于任何类的对象类型。配置动作方法类型为"UIButton"表示只有按钮对象能够连接到该动作。尽管目前看来并没有什么实际意义，但是记住这点在后面会用到的。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_button_addaction_2x.png)</center>
7. 点击"Connect"。
    Xcode会添加如下代码：
    ```Swift
    @IBAction func setDefaultLabelText(sender: UIButton) {
    }
    ```

`sender`参数指向负责触发该动作的对象，在本例中是按钮对象。`IBAction`属性表明这个动作是从Storyboard连接而来的。当前这个函数为空，接下来我们编写具体的执行代码。

在ViewController.swift的`setDefaultLabelText`动作方法中添加一些代码：
```Swift
mealNameLabel.text = "Default Text"
```

***检查点：***在模拟器中运行App查看当前的效果。当你点击"Set Default Label Text"按钮后，标签会从"Meal Name"更改为"Default Text"(在 setDefaultLabelText 方法中设置的值)。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_sim_defaulttext_2x.png)</center>

上面的例子是一个典型的 **"target-action"** 设计模式：在一个事件发生时，将一条消息从一个对象传递给另一个对象。例子中，target是ViewController(动作方法定义的地方)；sender是"Set Default Label Text"按钮；message是在源代码中定义的动作方法。

### 处理用户输入
这里，我们接受用户的输入，并在用户点击按钮后将用户输入的内容更新到标签处。

为了在文本域接受用户的输入，一般情况我们需要使用文本域**委托**。委托是一个对象，它能够与另一个对象的行为呼应。授权(delegating)对象(例子中的文本域)保留对另一个对象(Delegate，委托对象)的引用，然后在合适的时间，授权对象会发送一条消息给委托对象。这条消息告诉委托对象，授权对象正在处理或者已经处理了一个事件。委托对象便会进行响应，比如更新状态和外观等等。

任何对象都能作为一个另一个对象的委托，只要它实现了合适的协议。定义了文本域委托的协议是`UITextFieldDelegate`。在本例中，因为ViewController保留有对文本域的引用，所以你可以让ViewController作为文本域的委托。

#### 采用UITextFieldDelegate协议
1. 打开ViewController.swift。
2. 在该文件中，找到class行，如下所示：
    ```
    class ViewController: UIViewController {
    ```
3. 在UIViewController后，添加`, `和`UITextFieldDelegate`以采用这个协议。
    ```Swift
    class ViewController: UIViewController, UITextFieldDelegate {
    ```

#### 设置ViewController作为nameTextField的委托
1. 在ViewController.swift 中找到`viewDidLoad()`方法。
2. 在`super.viewDidLoad()`行之下，增加如下内容。
    ```Swift
    // Handle the text field’s user input through delegate callbacks.
    nameTextField.delegate = self
    ```

现在ViewController是nameTextField的委托。 UITextFieldDelegate包含两个可选的方法，可选意味着你并不是必须实现它们。不过为了获得你想要的行为，你需要在这里实现这两个方法。
```Swift
func textFieldShouldReturn(textField: UITextField) -> Bool
func textFieldDidEndEditing(textField: UITextField)
```

为了理解这些方法什么时候被调用和它们需要做什么，需要知道文本域是如何响应用户事件的。当用户点击文本域，文本域会自动变为第一级响应者(first responder)。在一个应用中，第一级响应者是获取应用中各种事件的第一个对象。换句话讲，用户产生的大多数事件都会转发给第一响应者。

一旦文本域变成了第一级响应者，iOS会显示键盘并进入编辑会话状态。用户使用键盘输入的信息会插入到文本域中。当用户想要结束编辑是，文本域需要释放它的第一级响应者的状态。这便是UITextFieldDelegate起作用的地方。你需要在用户点击按钮结束编辑的时候指定文本域释放它的第一级响应者状态。这里可以使用`textFieldShouldReturn(_:)`方法来完成。

#### 实现 UITextFieldDelegate 协议方法 textFieldShouldReturn(_:)
1. 在ViewController.swift中，`// MARK: Actions`的上方添加如下代码：
    ```Swift
    // MARK: UITextFieldDelegate
    ```
    你已经添加了几个这样的特殊注释了，Xcode会在源代码的函数菜单处列出这些特殊的注释。函数菜单可以让你快速导航到你想要去的地方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_functionsmenu_2x.png)</center>
2. 在注释的下方，添加下列函数：
    ```Swift
    func textFieldShouldReturn(textField: UITextField) -> Bool {
    }
    ```
3. 在这个方法中，添加下列代码使得文本域释放它的第一级响应状态。
    ```Swift
    // Hide the keyboard.
    textField.resignFirstResponder()
    ```
    尝试使用手工输入代替复制粘贴。这里可以发现Xcode的代码补全功能，十分节省时间。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_code_completion_2x.png)</center>
4. 在这个方法中，增加下面这行代码：
    ```Swift
    return true
    ```
    因为这个方法需要返回一个布尔值，返回`true`表示文本域在用户点击了回车键后应该将键盘消失以进行响应。

#### 实现 UITextFieldDelegate 协议方法 textFieldDidEndEditing(_:)
在`textFieldShouldReturn(_:)`方法之后，增加如下代码：
```Swift
func textFieldDidEndEditing(textField: UITextField) {
    mealNameLabel.text = textField.text
}
```

***检查点：***在模拟器中运行，在文本域输入值并点击"Done"按钮后，标签内容会显示你输入的信息。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/3_sim_finalUI_2x.png)</center>

## 视图控制器
### 理解视图控制器生命周期
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_vclife_2x.png)</center>

上图是视图控制器的视图状态的相互转换图。下面是UIViewController常用的方法：
1. `viewDidLoad()`
    在视图控制器的内容视图被创建和从Storyboard加载时调用。这个方法一般用于初始化设置。由于视图可能会由于资源的限制被清理，所以并不能保证这个方法制备调用一次。
2. `viewWillAppear()`
    在视图显示在屏幕上之前，你可以在这个方法中进行任何操作。因为一个视图的显示可能被其他视图阻隔，因此这个方法总会在内容视图将要显示在屏幕上之前被调用。
3. `viewDidAppear()`
    在视图呈现之后调用，比如用来获取数据或者展示一个动画。因为一个视图的显示可能被其他视图阻隔，这个方法总会在视图显示后被调用。

### 增加一张食物照片
接下来，我们增加一张可以展示食物的照片。
1. 打开Storyboard `Main.storyboard`。
2. 打开功能区的对象库。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/object_library_2x.png)</center>
3. 在对象库中，找到"image view"对象。
4. 将图像视图对象拖动到场景中，放置在堆栈视图中按钮的下方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_imageview_place_2x.png)</center>
5. 保持图像视图的选中状态，打开功能区的大小指示器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_inspector_size_2x.png)</center>
6. 在内部大小域出，选择"Placeholder"。
7. 设置"Width","Height"域的值为320。
    一个空图像并没有内部内容大小。给图像视图一个占位大小可以帮助你在界面中配置合适的约束。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_placeholdersize_2x.png)</center>
8. 在画布的右下角，打开 Pin 菜单。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_imageview_aspectratio_2x.png)</center>
9. 勾选"Aspect Ratio"(纵横比)。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_imageview_aspectratio_2x.png)</center>
10. 在Pin菜单中，点击"Add 1 Constraint"按钮。
    现在你的图像视图拥有1:1的纵横比，所以它会一直是一个正方形。
11. 保持图像视图的选中状态，打开属性编辑器。
12. 在属性编辑器中，设置"Mode"域的值为"Aspect Fill"。
    这一步确保不同纬度大小的图像在图像视图中不会失真。
13. 在属性编辑器中，设置"Interaction"为"User Interaction Enabled"。

此时用户界面看起来如下所示：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_imageview_finalconstraints_2x.png)</center>

### 显示一个默认的图像
需要提示用户选择一张图像。我们采用放置默认体术图像的方式来提示用户选择一张图像。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/defaultphoto_2x.png)</center>

1. 在项目导航栏处，选择 Assets.xcassets 来查看资源目录。
    资源目录是存储和组织应用的图像资源的地方。
2. 在左下角，点击`+`按钮，然后在弹出菜单中选择"New Image Set"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_assetcatalog_2x.png)</center>
3. 双击图像集名称然后重命名为 "defaultPhoto"。
4. 在Mac上选择你想要添加的图像。
5. 拖动并放置图像到 "2x" 位置处。
    *2x* 是iPhone6的显示分辨率所采用的。

为了显示默认的图像，需要进行如下设置。
1. 打开Storyboard，选中图像视图。
2. 打开功能区的属性编辑器。
3. 在属性编辑器中，设置"Image"为"defaultPhoto"

***检查点：***运行你的App，应该看到如下的图像：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_sim_finalUI_2x.png)</center>

### 将图像与代码连接
1. 打开辅助编辑器，辅助编辑器中打开ViewController.swift文件。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/assistant_editor_toggle_2x.png)</center>
2. 如果想要更大的空间进行操作，可以关闭导航栏和功能区。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/navigator_utilities_toggle_on_2x.png)</center>
3. 在Storyboard中，选中图像视图。
4. 按住键盘上的"Control"并拖动图像视图到ViewController中。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_imageview_dragoutlet_2x.png)</center>
5. 在弹出的对话框中，设置"Name"为"photoImageView"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_imageview_addoutlet_2x.png)</center>
6. 点击"Connect"。
    Xcode会增加以下代码：
    ```Swift
    @IBOutlet weak var photoImageView: UIImageView!
    ```

### 创建手势识别
图像视图并不是一个控制类，所以不能像按钮那样响应用户输入。比如你不能通过"Control"+拖动的方式创建一个动作方法。

不过，我们可以通过添加手势识别器来是图像视图具有交互的能力。手势识别允许你将它绑定到某一个视图上并响应动作。在Storyboard上添加手势识别很方便。
1. 打开对象库。
2. 在对象库中查找"Tap Gesture Recognizer"对象，并将其拖动到场景中，放置在图像视图上方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_gesturerecognizer_drag_2x.png)</center>

点击手势识别器会在场景上方的dock上显示。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_scenedock_2x.png)</center>

### 将手势与代码连接
1. 按住键盘上的"Control"并拖动手势到代码中。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_gesturerecognizer_dragaction_2x.png)</center>
2. 在弹出的对话框中，设置"Connection"为"Action"。
3. 设置"Name"为"selectImageFromPhotoLibrary"。
4. 设置"Type"为"UITapGestureRecognizer"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_gesturerecognizer_addaction_2x.png)</center>
5. 点击"Connect"。
    Xcode会添加如下代码：
    ```Swift
    @IBAction func selectImageFromPhotoLibrary(sender: UITapGestureRecognizer) {
    }
    ```

### 创建图像选择器以响应用户点击
用户点击图像视图后应该发生什么？我们可以设想，用户可以从相册中选择一张照片或者拍摄新照片。幸运的是，`UIImagePickerController`类能够实现这个功能。一个图像选择控制器管理一个供用户选取照片和拍摄照片的用户界面。与之前处理文本域委托类似，这里我们需要一个图像选取控制器代理来实现这个功能。代理协议的名字为`UIImagePickerControllerDelegate`。因为ViewController负责呈现 image picker controller，所以有必要采用`UINavigationControllerDelegate`协议，让ViewController具备一些基本的导航特性。

1. 返回标准编辑器视图。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/standard_toggle_2x.png)</center>
2. 在项目导航栏处，选择ViewController.swift。
3. 在UIViewController后增加 UIImagePickerControllerDelegate 和 UINavigationControllerDelegate。
    ```Swift
    class ViewController: UIViewController, UITextFieldDelegate, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    ```
#### 实现selectImageFromPhotoLibrary(_:)动作方法
```Swift
@IBAction func selectImageFromPhotoLibrary(sender: UITapGestureRecognizer) {
    // Hide the keyboard. 
    // 隐藏键盘
    nameTextField.resignFirstResponder()
    
    // UIImagePickerController is a view controller that lets a user pick media from their photo library.
    // 新建一个图像选择控制器实例
    let imagePickerController = UIImagePickerController()
    
    // Only allow photos to be picked, not taken.
    // 只允许从相册选择照片，不允许拍照
    imagePickerController.sourceType = .PhotoLibrary
    
    // Make sure ViewController is notified when the user picks an image.
    // 确保用户选取了图像后视图控制器能够得到通知
    imagePickerController.delegate = self
    
    presentViewController(imagePickerController, animated: true, completion: nil)
}
```

在图像选取控制器呈现后，它的行为由它的代理进行控制。为了确保用户能够选取照片，需要实现UIImagePickerControllerDelegate定义的代理方法。
```Swift
func imagePickerControllerDidCancel(picker: UIImagePickerController)
func imagePickerController(picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : AnyObject])
```

下面是这两个函数的具体内容：
```Swift
func imagePickerControllerDidCancel(picker: UIImagePickerController) {
    // Dismiss the picker if the user canceled.
    // 用户取消时让选取控制器消失
    dismissViewControllerAnimated(true, completion: nil)
}
```

```Swift
func imagePickerController(picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : AnyObject]) {
    // The info dictionary contains multiple representations of the image, and this uses the original.
    // 字典info包含有原始图和可编辑版本图像，这里简单的使用原始图
    let selectedImage = info[UIImagePickerControllerOriginalImage] as! UIImage
    
    // Set photoImageView to display the selected image.
    // 设置photoImageView显示选取的图像
    photoImageView.image = selectedImage
    
    // Dismiss the picker.
    // 选取结束后让控制器消失
    dismissViewControllerAnimated(true, completion: nil)
}
```

***检查点：***运行应用，点击图像视图弹出一个图像选择器。你需要在警告框中点击OK以获得访问照片的权利。然后你可以点击Cancel按钮来释放图像选择器，或者打开相册并选择一个图像。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/4_sim_imagepicker_2x.png)</center>

## 自定义控制视图
为了给食物进行评级，用户需要一个控制视图来给食物选择相应的星级。这里我们采用自定义控制视图来实现。下面会是实现后的结果：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_ratingcontrol_2x.png)</center>

首先，建立一个自定义视图类————UIView的子类。
1. 按下Command + N，新建一个文件
2. 在弹出的对话框的左侧，选择iOS栏下的Source。
3. 选择"Cocoa Touch Class"，并点击"Next"。
4. 设置"Class"为"RatingControl"。
5. 设置"Subclass of"为"UIView"。
6. 确保"Language"为"Swift"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_newviewclass_2x.png)</center>
7. 点击"Next"。
    默认保存在工程目录下；组选项默认为应用名；在目标选项处，勾选应用，取消勾选"tests for your app"。
8. 保持默认的配置，点击"Create"。
    Xcode会创建一个定义了RatingControl的类文件:RatingControl.swift。
9. 在RatingControl.swift中，删除默认添加的实现代码。
    ```Swift
    import UIKit

    class RatingControl: UIView {

    }
    ```

通常情况下，可以通过以下两种方式创建一个视图：使用frame(边框)初始化一个视图或者允许从Storyboard中加载视图。两种方法对应的初始化函数分别为：`init(frame:)`和`init(coder:)`。这里我们自定义的视图选择使用`init(coder:)`。

重写初始化函数：
1. 在RatingControl类中增加一行注释。
    ```Swift
    // MARK: Initialzation
    ```
2. 在注释下方，输入`init`。
    可以看到代码自动补全如下：
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_initcoder_codecompletion_2x.png)</center>
3. 在补全的代码中选择`init(coder:)`初始化函数，并按下回车键。
4. 点击错误修复来自动添加关键字`required`。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_initcoder_fixit_2x.png)</center>
    `required`表示每一个UIView子类都必须实现`init(coder:)`。Swift知道这一点，所以会提供这个自动修复。
5. 增加父类的初始化函数。
    ```Swift 
    super.init(coder: aDecoder)
    ```
### 显示自定义视图
1. 打开Storyboard。
2. 在对象库中找到View(视图)对象，并拖动到堆栈视图中图像视图的下方。
3. 保持View对象的选中状态，打开大小指示器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_inspector_size_2x.png)</center>
4. 在大小指示器中设置"Intrinsic Size"为"Placeholder"。
5. 在"Intrinsic Size"下方的菜单中设置"Height"为44，设置"Width"为240，并按下回车键以确认。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_viewwithplaceholdersize_2x.png)</center>
6. 保持视图的选中状态，打开标识指示器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_inspector_identity_2x.png)</center>
7. 在标识指示器中设置"Class"为"RatingControl"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_identity_ratingcontrol_2x.png)</center>

### 给自定义视图添加按钮
在`init(coder:)`函数中，增加如下代码：
```Swift
required init(coder aDecoder: NSCoder!) {
    super.init(coder: aDecoder)
    
    // 增加一个红色的按钮
    let button = UIButton(frame: CGRect(x: 0, y: 0, width: 44, height: 44))
    button.backgroundColor = UIColor.redColor()
    // 将按钮添加到RatingControl视图上
    addSubview(button)
}
```

***检查点：***运行应用，可以看到如下的界面:
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_sim_1redbutton_2x.png)</center>

### 给按钮添加动作
1. 在RatingControl.swift中，增加一行注释:
    ```Swift 
    // MARK: Button Action
    ```
2. 在注释下方增加如下函数：
    ```Swift 
    func ratingButtonTapped(button: UIButton) {
        print("Button pressed 👍")
    }
    ```
3. 在`init(coder:)`初始化函数中，在`addSubview(button)`这一行的前面，增加如下代码：
    ```Swift
    button.addTarget(self, action: "ratingButtonTapped:", forControlEvents: .TouchDown)
    ```
    这里使用的是target-action模式，将动作`ratingButtonTapped`与`button`对象绑定，触发条件为`.TouchDown`(按下操作)。这里不需要使用IBAction，因为你没有使用Interface Builder。

现在，`init(coder:)`初始化函数应该如下所示：
```Swift
required init(coder aDecoder: NSCoder!) {
    super.init(coder: aDecoder)
    
    let button = UIButton(frame: CGRect(x: 0, y: 0, width: 44, height: 44))
    button.backgroundColor = UIColor.redColor()
    button.addTarget(self, action: "ratingButtonTapped:", forControlEvents: .TouchDown)
    addSubview(button)
}
```

***检查点：***运行应用，点击红色按钮，应该在控制台看到"Button pressed"消息。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_console_buttonpressed_2x.png)</center>

接下来考虑RatingControl类需要拥有哪些信息？首先是0，1，2，3，4，5等级信息，所以我们需要一个Int型的值来保存，并且还需要UIButton对象数组来体现等级。所以给RatingControl类增加如下属性：
```Swift 
var rating = 0
var ratingButtons = [UIButton]()
```

现在，自定义视图中只有一个按钮，但是我们需要五个。创建五个按钮，我们可以使用`for-in`循环。下面是简单的增加了循环后的代码：
```Swift 
required init(coder aDecoder: NSCoder!) {
    super.init(coder: aDecoder)

    for _ in 0..<5 {
        let button = UIButton(frame: CGRect(x:0, y:0, width: 44, height: 44))
        button.backgroundColor = UIColor.redColor()
        button.addTarget(self, action: "ratingButtonTapped:", forControlEvents: .TouchDown)
        ratingButtons += [button]
        addSubview(button)
    }
}
```

***检查点：***运行应用，可以看到如下的界面。可以发现看起来只有一个按钮，这是因为`for-in`循环中只是简单地把按钮叠加在一起，我们需要对按钮进行布局。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_sim_1redbutton_2x.png)</center>

这种类型的布局代码属于一个叫做`layoutSubviews`的函数，由`UIView`类定义。`layoutSubviews`方法会被系统在合适的时间调用以使`UIView`子类能够对子视图进行布局。下面来重写这一个函数。
```Swift
override func layoutSubviews() {
    var buttonFrame = CGRect(x: 0, y: 0, width: 44, height: 44)

    // Offset each button's origin by the length of the button plus spacing
    // 将每一个按钮的横轴进行适当的偏移
    for (index, button) in ratingButtons.enumerate() {
        buttonFrame.origin.x = CGFloat(index * (44 + 5))
        button.frame = buttonFrame
    }
}
```

***检查点：***运行应用，可以看到如下的界面。现在会有五个按钮，并且点击按钮会调用`ratingButtonTapped(_:)`函数。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_sim_5redbuttons_2x.png)</center>

打开和关闭控制台，使用如下所示的调试开关(Debug toggle)
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/debug_toggle_2x.png)</center>

### 为按钮的大小声明一个常量
应该注意到，在代码中使用了值44。在代码中使用硬编码数值是一个不好的习惯。如果想要一个更大一点的按钮，需要更改每一个地方的值，十分麻烦。相反，我们声明一个常量来代替按钮的大小，在需要改变的时候只需要改变一次即可。下面就来声明一个常量。
1. 在`layoutSubviews()`方法中，在第一行的前面增加如下代码：
    ```Swift 
    // Set the button's width and height to a square the size of the frame's height.
    // 设置按钮的高度和宽度为边框的高度
    let buttonSize = Int(frame.size.height)
    ```
2. 将代码中的44用`buttonSize`替换。
    ```Swift 
    var buttonFrame = CGRect(x: 0, y: 0, width: buttonSize, height: buttonSize)

    // Offset each button's origin by the length of the button plus spacing
    for (index, button) in ratingButtons.enumerate() {
        buttonFrame.origin.x = CGFloat(index * (buttonSize + 5))
        button.frame = buttonFrame
    }
    ```
3. 在`init(coder:)`函数中，改变`for-in`循环的第一行：
    ```Swift
    let button = UIButton()
    ```
    因为在`layoutSubviews()`函数中已经重新设置了边框，所以不需要在创建的时候设置了。

现在，`layoutSubviews()`函数应该如下所示：
```Swift 
override func layoutSubviews() {
    // Set the button's width and height to a square the size of the frame's height.
    let buttonSize = Int(frame.size.height)
    
    var buttonFrame = CGRect(x: 0, y: 0, width: buttonSize, height: buttonSize)

    // Offset each button's origin by the length of the button plus spacing
    for (index, button) in ratingButtons.enumerate() {
        buttonFrame.origin.x = CGFloat(index * (buttonSize + 5))
        button.frame = buttonFrame
    }
}
```

`init(coder:)`函数如下：
```Swift
required init(coder aDecoder: NSCoder!) {
    super.init(coder: aDecoder)

    for _ in 0..<5 {
        let button = UIButton()
        button.backgroundColor = UIColor.redColor()
        button.addTarget(self, action: "ratingButtonTapped:", forControlEvents: .TouchDown)
        ratingButtons += [button]
        addSubview(button)
    }
}
```

***检查点：***运行应用，可以看到如下的界面。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_sim_5redbuttons_2x.png)</center>

### 给按钮添加星形图像
这里我们会给按钮增加空白的和实心的星形图像。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_emptyStar_2x.png)</center>
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_filledStar_2x.png)</center>

将图像添加到项目中：
1. 在项目导航栏处，选择Images.xcassets。
2. 在左下角点击`+`，并在弹出菜单中选择"New Folder"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_assetcatalog_addfolder_2x.png)</center>
3. 双击文件夹，重命名为"Rating Images"。
4. 保持文件夹的选中状态，在左下角点击`+`，并在弹出菜单中选择"New Image Set"。
5. 双击图像集名称并重命名为"emptyStar"。
6. 在Mac上选择空心星形图像。
7. 拖动并放置图像到 "2x" 位置处。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_emptystar_drag_2x.png)</center>
8. 同样的方式，将实心星形图像放入到名为"filledStar"的图像集中。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_filledstar_drag_2x.png)</center>

完成后资源集应该如下所示：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_assetcatalog_final_2x.png)</center>

接下来，编写代码来在合适的时间使用合适的图像。
1. 打开 RatingControl.swift。
2. 在`for-in`循环前，增加如下代码：
    ```Swift 
    let filledStarImage = UIImage(named: "filledStar")
    let emptyStarImage = UIImage(named: "emptyStar")
    ```
3. 在`for-in`循环中，初始化按钮的代码后面添加：
    ```Swift 
    button.setImage(emptyStarImage, forState: .Normal)
    button.setImage(filledStarImage, forState: .Selected)
    button.setImage(filledStarImage, forState: [.Highlighted, .Selected])
    ```
    这里设置了按钮在`.Normal`状态下使用空心星形图像，在`.Selected`状态下和既在`.Selected`又在`.Highlighted`状态下(用户正在点击按钮)使用实心星形图像。
4. 删除设置按钮背景颜色的代码：
    ```Swift 
    button.backgroundColor = UIColor.redColor()
    ```
5. 增加下面的代码：
    ```Swift
    button.adjustsImageWhenHighlighted = false
    ```
    这一步确保按钮在状态转换时不会有额外的高亮显示。

现在，`init(coder:)`代码如下：
```Swift 
required init(coder aDecoder: NSCoder!) {
    super.init(coder: aDecoder)
    
    let emptyStarImage = UIImage(named: "emptyStar")
    let filledStarImage = UIImage(named: "filledStar")
    
    for _ in 0..<5 {
        let button = UIButton()
        
        button.setImage(emptyStarImage, forState: .Normal)
        button.setImage(filledStarImage, forState: .Selected)
        button.setImage(filledStarImage, forState: [.Highlighted, .Selected])
        
        button.adjustsImageWhenHighlighted = false
        
        button.addTarget(self, action: "ratingButtonTapped:", forControlEvents: .TouchDown)
        ratingButtons += [button]
        addSubview(button)
    }
}
```

***检查点：***运行应用，可以看到如下的界面：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_sim_emptystars_2x.png)</center>


### 实现按钮的动作
1. 在 RatingControl.swift 文件中，找到"ratingButtonTapped(_:)"方法。
2. 用下面的代码替换掉print部分的代码：
    ```Swift 
    rating = ratingButtons.indexOf(button)! + 1
    ```
    `indexOf(_:)`方法用来找到被按下的按钮的索引值。这个方法返回一个可选值，因为你寻找的实例在这个集合中可能不存在。然而，因为这里只能是你创建的按钮触发这个动作，所以可以确定不会返回无效值。这样，我们可以使用强制拆包符`!`来访问索引值。因为索引值从0开始，所以需要+1。
3. 增加一个函数：
    ```Swift 
    func updateButtonSelectionStates() {
    }
    ```
    这个函数用来更新按钮的选择状态。
4. 在`updateButtonSelectionStates()`函数中，增加一个`for-in`循环。
    ```Swift 
    for (index, button) in ratingButtons.enumerate() {
        // If the index of a button is less than the rating, that button should be selected.
        button.selected = index < rating
    }
    ```
    通过比较来确定按钮是否被选中。
5. 在`ratingButtonTapped(_:)`函数中，添加对`updateButtonSelectionStates()`函数的调用代码：
    ```Swift 
    func ratingButtonTapped(button: UIButton) {
        rating = ratingButtons.indexOf(button)! + 1
        
        updateButtonSelectionStates()
    }
    ```
6. 在`layoutSubviews()`方法中，最后一行增加对`updateButtonSelectionStates()`的调用。
    ```Swift
    override func layoutSubviews() {
        // Set the button's width and height to a square the size of the frame's height.
        let buttonSize = Int(frame.size.height)
        var buttonFrame = CGRect(x: 0, y: 0, width: buttonSize, height: buttonSize)
        
        // Offset each button's origin by the length of the button plus some spacing.
        for (index, button) in ratingButtons.enumerate() {
            buttonFrame.origin.x = CGFloat(index * (buttonSize + 5))
            button.frame = buttonFrame
        }
        updateButtonSelectionStates()
    }
    ```
    在视图加载后更新按钮的状态十分必要，而不仅仅是在评级更改的时候。
7. 更新rating属性，添加一个观察者：
    ```Swift 
    var rating = 0 {
        didSet {
            setNeedsLayout()
        }
    }
    ```
    属性观察者(property observer)可以获取属性值的改变并进行响应。属性观察者在属性值改变的前或后被调用。特别的是，`didSet`属性观察者在改变后调用。这里，我们包含了一个调用`setNeedsLayout()`，这会在每一次评级更新的时候触发布局更新。这样能够保证用户界面总是显示正确的评级属性。


`updateButtonSelectionStates()`方法如下：
```Swift 
func updateButtonSelectionStates() {
    for (index, button) in ratingButtons.enumerate() {
        // If the index of a button is less than the rating, that button shouldn't be selected.
        button.selected = index < rating
    }
}
```

***检查点：***运行应用，点击第三个星星，可以看到评级更改为3。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_sim_filledstars_2x.png)</center>

### 增加属性：空白间隔和星星的数量
为了保证在代码中没有其它的硬编码数值，添加评级星星的数量和空白间隔这两个属性。
1. 在RatingControl.swift中，添加两个属性：
    ```Swift
    var spacing = 5
    var stars = 5
    ```
2. 替换掉使用这两个属性的数值：
    ```Swift
    buttonFrame.origin.x = CGFloat(index * (buttonSize + spacing))
    ```
    ```Swift
    for _ in 0..<stars {
    ```

### 将评级视图与ViewController连接
这一步设置ViewController类对自定义的rating control的引用。
1. 打开Storyboard，并开启辅助编辑器
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/assistant_editor_toggle_2x.png)</center>
2. "Control"+拖动，将自定义的RatingControl拖动到ViewController中以添加引用。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_ratingcontrol_dragoutlet_2x.png)</center>
3. 在弹出的对话框中，设置"Name"为"ratingControl"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_ratingcontrol_addoutlet_2x.png)</center>
4. 点击"Connect"。

## 清理项目
现在，基本上掌握了应用场景的制作，接下来，我们会实现一些高级的行为并构建与现在不同的用户界面，所以需要清除不需要的部分。

首先，清理用户界面：
1. 返回到标准编辑器状态。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/standard_toggle_2x.png)</center>
2. 打开Storyboard。
3. 选择"Set Default Label Text"按钮，然后按下"Delete"键来删除它。
    堆栈视图会重新组合你的UI元素：
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_deletebutton_2x.png)</center>
4. 如果必要，打开大纲视图，选中堆栈视图对象。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/2_AL_outlineview_2x.png)</center>
5. 打开功能区的属性编辑器。
6. 在属性编辑器中，设置"Alignment"为"Center"。
    堆栈视图中的元素会居中显示：
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_centerstack_2x.png)</center>

接下来，清除与刚刚删除的按钮相关的动作按钮。
1. 打开ViewController.swift。
2. 删除`setDefaultLabelText(_:)`方法。
    ```Swift 
    @IBAction func setDefaultLabelText(sender: UIButton) {
        mealNameLabel.text = "Default Text"
    }
    ```

***检查点：***运行应用，可以看到如下的界面。

> 如果遇到构建错误，尝试按下快捷键 "Command+Shift+K"来清理项目。

<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/5_sim_finalUI_2x.png)</center>

## 数据模型
接下来我们创建数据模型来存储食物信息，首先我们需要定义一个拥有名称、照片和评级的类。
1. 按下"Command+N"新建文件。
2. 在弹出的对话框中，选择iOS栏下的Source。
3. 选择"Swift"文件，点击"Next"。
    与新建RatingControl类不同的是，数据类并没有父类，不需要继承。
4. 设置"Save As"为"Meal"。
5. 保存文件到默认的工程目录下。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/6_createmealclass_2x.png)</center>
6. 点击"Create"。

在Swift中，属性"名称"可以使用`String`，"照片"可以使用"UIImage"类型，"评级"可以使用`Int`表示。
1. 按照如下代码定义属性。
    ```Swift 
    class Meal {
        // MARK: Properties
        
        var name: String
        var photo: UIImage?
        var rating: Int
    }
    ```
2. 定义初始化函数。
    ```Swift
    // MARK: Initialization
     
    init(name: String, photo: UIImage?, rating: Int) {
    }
    ```
3. 在初始化函数中设置基本的属性。
    ```Swift
    // Initialize stored properties
    self.name = name
    self.photo = photo
    self.rating = rating
    ```
    不过，想一想如果试图使用错误的数值创建一个Meal的实例会发生什么？所以，我们需要设置在不能错误的情况下返回nil。
4. 增加如下代码来返回nil。
    ```Swift 
    // Initialization should fail if there is no name or if the rating is negative.
    if name.isEmpty || rating < 0 {
        return nil
    }
    ```
    由于初始化函数可能返回为nil,所以需要给初始化函数指明。
5. 通过点击`fix-it`错误提示，在`init`关键词后增加一个`?`。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/6_init_fixit_2x.png)</center>
    ```Swift
    init?(name: String, photo: UIImage?, rating: Int) {
    ```

下面是完整的`init?(name:photo:rating:)`函数：
```Swift 
// MARK: Initialization
 
init?(name: String, photo: UIImage?, rating: Int) {
    // Initialize stored properties.
    self.name = name
    self.photo = photo
    self.rating = rating
    
    // Initialization should fail if there is no name or if the rating is negative.
    if name.isEmpty || rating < 0 {
        return nil
    }
}
```

***检查点：***按下快捷键"Command+B"来构建项目。构建项目可以让编译器验证你是否有输入错误，比如忘记输入`?`。如果有，你可以通过点按`fix-it`来自动修复问题。


### 测试数据
尽管数据模型代码能够被构建，但是还没有在应用中真正起作用。所以很难说是否真正正确地实现了所有事情。那么接下来我们来编写单元测试以检验是否正确。

Xcode已经自动创建了单元测试文件。
1. 打开项目导航栏出的 "FoodTrackerTests" 文件夹。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/6_foodtrackertests_2x.png)</center>
2. 打开 "FoodTrackerTests.swift"文件。

```Swift 
import UIKit
import XCTest
 
class FoodTrackerTests: XCTestCase {
    
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testExample() {
        // This is an example of a functional test case.
        XCTAssert(true, "Pass")
    }
    
    func testPerformanceExample() {
        // This is an example of a performance test case.
        self.measureBlock() {
            // Put the code you want to measure the time of here.
        }
    }
    
}
```

先来理解一下这个文件。XCTest框架库是Xcode的测试框架库。单元测试定义为一个类 "FoodTrackerTests", 并继承自 "XCTestCase"。注释解释了`setUp()`和`tearDown()`方法。

我们能够编写的测试主要是函数功能测试和性能测试。当前我们主要编写功能测试代码。以测试Meal类的对象为例：
1. 删除默认的模版测试代码：
    ```Swift
    import UIKit
    import XCTest
     
    class FoodTrackerTests: XCTestCase {
        
    }
    ```
2. 现增加如下注释：
    ```Swift
    // MARK: FoodTracker Tests
    ```
    养成编写注释的好习惯😊。
3. 在注释的下方，添加下列单元测试函数：
    ```Swift
    // Tests to confirm that the Meal initializer returns when no name or a negative rating is provided.
    func testMealInitialization() {
    }
    ```
4. 首先，添加一个能够正确通过的测试用例。
    ```Swift
    // Success case.
    let potentialItem = Meal(name: "Newest meal", photo: nil, rating: 5)
    XCTAssertNotNil(potentialItem)
    ```
    `XCTAssertNotNil`检测Meal对象在初始化后是否为nil。
5. 现在，增加一个不应该成功初始化的测试用例。
    ```Swift
    // Failure cases.
    let noName = Meal(name: "", photo: nil, rating: 0)
    XCTAssertNil(noName, "Empty name is invalid")
    ```
    `XCTestAssertNil`警告一个对象是nil。
6. 现在添加一个Meal对象应该初始化失败但是尝试警告初始化应该能成功的测试用例。
    ```Swift
    let badRating = Meal(name: "Really bad rating", photo: nil, rating: -1)
    XCTAssertNotNil(badRating)
    ```

现在，`testMealInitialization`测试函数应该如下：
```Swift 
// Tests to confirm that the Meal initializer returns when no name or a negative rating is provided.
func testMealInitialization() {
    // Success case.
    let potentialItem = Meal(name: "Newest meal", photo: nil, rating: 5)
    XCTAssertNotNil(potentialItem)
    
    // Failure cases.
    let noName = Meal(name: "", photo: nil, rating: 0)
    XCTAssertNil(noName, "Empty name is invalid")
    
    let badRating = Meal(name: "Really bad rating", photo: nil, rating: -1)
    XCTAssertNotNil(badRating)
}
```

通过按下快捷键 "Command+U" 来一次运行所有的单元测试。最后一个测试用例应该不会通过。

只运行一个单元测试：
1. 在`FoodTrackerTests.swift`文件中，找到`testMealInitialization`单元测试。
2. 在测试名的左侧，找到一个方块形的图标。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/6_preparetest_2x.png)</center>
3. 鼠标悬停在方块上方以使一个小的运行按钮显现。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/6_runtest_2x.png)</center>
4. 点击运行按钮，运行这个单元测试。

***检查点：***运行这个单元测试，前两个用例应该能够通过，后面一个用例不能通过。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/6_failtest_2x.png)</center>

可以看到，单元测试能够帮助我们捕获代码中的错误。下面更改最后一个测试用例，让它打印出正常的错误提示。

直接更改最后一个测试用例的最后一行：
```Swift
XCTAssertNil(badRating, "Negative ratings are invalid, be positive")
```

现在`testMealInitialization()`函数应该如下所示：
```Swift 
// Tests to confirm that the Meal initializer returns when no name or a negative rating is provided.
func testMealInitialization() {
    // Success case.
    let potentialItem = Meal(name: "Newest meal", photo: nil, rating: 5)
    XCTAssertNotNil(potentialItem)
    
    // Failure cases.
    let noName = Meal(name: "", photo: nil, rating: 0)
    XCTAssertNil(noName, "Empty name is invalid")
    
    let badRating = Meal(name: "Really bad rating", photo: nil, rating: -1)
    XCTAssertNil(badRating, "Negative ratings are invalid, be positive")
}
```

***检查点：***运行测试，所有的测试用例都应该通过。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/6_passtest_2x.png)</center>

> 编写代码中单元测试是必要的，它能够帮助我们捕获程序中可能忽略的错误。

## 创建表视图
### 制作开场场景
目前，我们的应用有一个让用户添加和评级食物的界面。现在我们来创建一个展示所有食物列表的界面。这里我们使用iOS内建的表视图(UITableView)来实现。表视图通过表视图控制器(UITableViewController, UIViewController的子类)来管理。
1. 打开Storyboard文件。
2. 在功能区的对象库中找到"Table View Controller"对象。
3. 拖动"Table View Controller"对象放到画布中。

现在在故事版上有了两个场景了，一个用来显示食物列表，一个用来增加新的食物。

让用户启动应用时首先看到食物列表会更好，所以接下来我们要设置Xcode把刚刚新建的"Table View Controller"最为第一个场景。

1. 通过关闭导航栏和功能区来获得更大的编辑界面。
2. 将"Storyboard entry point"(故事板入口)从食物场景拖动到表视图控制器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_newtableview_2x.png)</center>
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_storyboardentrypoint_2x.png)</center>

***检查点：***运行你的App，应该看到如下的开场界面：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_sim_emptytv_2x.png)</center>

接下来配置表视图:
1. 打开Storyboard的大纲视图，并选中表视图(Table View)
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_outlineview_table_2x.png)</center>
2. 保持表视图的选中，打开功能区的大小指示器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_inspector_size_2x.png)</center>
3. 设置"Row Height"为 90 ,并按下回车键以确认。

### 设计自定义的表单元
表视图中的每一行通过`UITableViewCell`进行管理。表视图单元有一系列的预定义的行为和默认单元样式，不过这里我们需要更多的功能，所以需要自定义我们的表单元。
1. 按下快捷键"Command+N"来新建文件。
2. 在弹出的对话框中，选择iOS栏下的Source。
3. 选择"Cocoa Touch Class"，并点击"Next"。
4. 设置"Class"为"Meal"。
5. 设置"Subclass of"为"UITableViewCell"。
    这里类的标题会自动更改为"MealTableViewCell"。Xcode在你自定义创建表单元时会对名称进行处理以使代码更加清晰，所以保持新的命名。
6. 确保"Language"为"Swift"。
7. 点击"Next"。
    保存文件到默认的工程目录下。
8. 其它设置保持不变，点击"Create"。

现在打开故事板，查看表视图控制器，注意到在表视图中只显示了一个表单元。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_singletvcell_2x.png)</center>

这一个表单元代表了其它的单元，接下来需要做一些配置工作，将表单元与自定义的表单元子类连接。
1. 在大纲视图中，选中"Table View Cell"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_outlineview_cell_2x.png)</center>
2. 打开功能区的属性编辑器。
3. 设置"Identifier"为"MealTableViewCell"。按下回车键以确认。
    这是重要的一步，后面会解释。
4. 在属性编辑器中，设置"Selection"为"None"。
    这一步会使表单元在用户点击的时候不会显示高亮。
5. 打开大小指示器。
6. 设置"Row Height"为"93"。
    确保在右侧的"Custom"为选中的状态。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_inspector_size_cell_2x.png)</center>
    按下回车键确认。
7. 打开标识指示器。
8. 设置"Class"为"MealTableViewCell"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_inspector_identity_cell_2x.png)</center>

配置完这个表单元后，我们要设计自定的用户界面，最后能够如下图所示，可以先自己想想如何设计并实现：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_sim_tablecellUI_2x.png)</center>

下面来设计自定义表单元的用户界面：
1. 在菜单中选择 `Editor > Canvas > Show Bounds Rectangles`来显示UI元素的边界，以使得调整UI元素更加清晰。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_showbounds_2x.png)</center>
2. 在对象库中，找到图像视图对象，并拖动到表单元中。
3. 拖动并改变图像视图的大小，让它处于单元视图的左侧，如下图所示：
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_imageview_resize_2x.png)</center>
4. 接下来给图像视图添加默认的图像。
5. 保持图像视图的选中状态，打开属性编辑器。
6. 在属性编辑器中，设置"Image"为"defaultPhoto"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_imageview_setdefault_2x.png)</center>
7. 在对象库中找到标签对象，并拖动到表单元中。
8. 拖动标签对象让它处于图像视图的右侧并于表单元的上边框对齐，如下图所示。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_label_drag_2x.png)</center>
9. 改变标签的大小，让它的右边框与表单元的右边框对齐：
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_label_resize_2x.png)</center>
10. 在对象库中找到View(视图)对象，并拖动到表单元中。
11. 保持视图对象的选中，打开大小指示器。
12. 在大小指示器中设置"Height"为"44"，"Width"为"240"。并按下回车键以确认
13. 拖动视图动向使它与标签的左边框对齐并位于标签对象的下方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_ratingcontrol_resize_2x.png)</center>
14. 保持视图的选中状态，打开标识指示器。
15. 设置"Class"为"RatingControl"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_inspector_identity_control_2x.png)</center>
16. 保持视图的选中状态，打开属性编辑器。
17. 找到"Interaction"属性，取消选中"User Interaction Enabled"。
    在表单元中显示时，不需要有交互功能。

现在，用户界面应该如下图所示:
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_tablecellUI_2x.png)</center>

***检查点：***运行应用，可以看到如下的界面。尽管更改了UI元素，但是仍然显示为空，这是为什么？
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_sim_wideemptycells_2x.png)</center>

在故事板中，一个表格视图能够配置成显示静态的数据(有Storyboard提供)或者动态的数据(有表视图控制器逻辑提供)。表视图默认使用动态数据，所以我们需要在代码中加载数据，不过目前为止还并没有实现这一行为。这意味着在故事板中提供的静态内容并不能在运行时呈现，所以我们看不到任何东西。接下来，我们在辅助编辑器中预览用户界面。
1. 打开辅助编辑器，如果需要更大的空间，可以关闭导航栏和功能区。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/assistant_editor_toggle_2x.png)</center>
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/navigator_utilities_toggle_on_2x.png)</center>
2. 在编辑器选择栏中，从"Automatic"切换到"Preview > Main.storyboard(Preview)"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_assistant_switchtopreview_2x.png)</center>

Xcode应该看起来如下图所示：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_assistant_preview_2x.png)</center>

### 添加图像到工程中
这里我们添加一些示例图像到工程中，作为应用启动时的初始食物数据。
1. 在项目导航栏处，选择Images.xcassets。
2. 在左下角点击`+`，并在弹出菜单中选择"New Folder"。
3. 双击文件夹，重命名为"Sample Images"。
4. 保持文件夹的选中状态，在左下角点击`+`，并在弹出菜单中选择"New Image Set"。
5. 双击图像集名称并重命名，这个名称会在代码中使用。
6. 在Mac上选择你想要添加的图像。
7. 拖动并放置图像到 "2x" 位置处。

重复步骤4-7，添加更多的图像，这里我们的示例添加了三个不同的图像：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_assetcatalog_2x.png)</center>

### 将表单元UI与代码连接
1. 打开辅助编辑器，如果需要更大的空间，可以关闭导航栏和功能区。
2. 在编辑器选择栏中，选择"Automatic > MealTableViewCell.swift"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_assistant_switchtocode_2x.png)</center>
3. 在MealTableViewCell内中添加以下注释:
    ```Swift 
    // MARK: Properties
    ```
4. 按住"Control"键，并拖动标签到注释代码下方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_label_dragoutlet_2x.png)</center>
5. 在弹出的对话框中，设置"Name"为"nameLable"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_label_addoutlet_2x.png)</center>
6. 保持其他的默认选项，点击"Connect"。
7. 选中图像视图，按住"Control"键，拖动到"nameLabel"下方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_imageview_dragoutlet_2x.png)</center>
8. 在弹出的对话框中，设置"Name"为"photoImageView"。
    保持其他的默认选项，点击"Connect"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_imageview_addoutlet_2x.png)</center>
9. 选中评级控制视图，按住"Control"键，拖动到"photoImageView"下方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_ratingcontrol_dragoutlet_2x.png)</center>
10. 在弹出的对话框中，设置"Name"为"ratingControl"。
    保持其他的默认选项，点击"Connect"。

"MealTableViewCell.swift"中的属性应该如下所示：
```Swift 
@IBOutlet weak var nameLabel: UILabel!
@IBOutlet weak var photoImageView: UIImageView!
@IBOutlet weak var ratingControl: RatingControl!
```

### 加载初始化数据
首先，创建一个自定义的表视图控制器来管理食物列表界面。
1. 按下快捷键"Command+N"来新建文件。
2. 在弹出的对话框中，选择iOS栏下的Source。
3. 选择"Cocoa Touch Class"，并点击"Next"。
4. 设置"Class"为"MealTableViewController"。
5. 设置"Subclass of"为"UITableViewController"。
6. 确保"Language"为"Swift"。
7. 确保"Also create XIB file"为取消选中状态。
7. 点击"Next"。
    保存文件到默认的工程目录下。
8. 其它设置保持不变，点击"Create"。

在这个自定义的类中，我们需要定义一个属性来存储食物对象。Swift标准库中包含了`Array`这个结构，能够很好的记录对象列表。
1. 在`MealTableViewController`类中添加如下代码：
    ```Swift 
    // MARK: Properties
    var meals = [Meal]()
    ```
2. 在`viewDidLoad()`方法后面，新建一个方法：
    ```Swift 
    func loadSampleMeals() {
    }
    ```
3. 在`loadSampleMeals()`方法中添加代码来创建一些Meal对象。
    ```Swift 
    let photo1 = UIImage(named: "meal1.jpg")!
    let meal1 = Meal(name: "Caprese Salad", photo: photo1, rating: 4)!
     
    let photo2 = UIImage(named: "meal2.jpg")!
    let meal2 = Meal(name: "Chicken and Potatoes", photo: photo2, rating: 5)!
     
    let photo3 = UIImage(named: "meal3.jpg")!
    let meal3 = Meal(name: "Pasta with Meatballs", photo: photo3, rating: 3)!
    ```
4. 将这些对象加入到meals数组中。
    ```Swift 
    meals += [meal1, meal2, meal3]
    ```
5. 删除`viewDidLoad()`方法中的注释，在`super.viewDidLoad()`后面添加如下代码：
    ```Swift 
    // Load the sample data.
    loadSampleMeals()
    ```

现在，`viewDidLoad()`方法为：
```Swift 
override func viewDidLoad() {
    super.viewDidLoad()
    
    // Load the sample data.
    loadSampleMeals()
}
```

现在，`loadSampleMeals()`方法为：
```Swift 
func loadSampleMeals() {
    let photo1 = UIImage(named: "meal1.jpg")!
    let meal1 = Meal(name: "Caprese Salad", photo: photo1, rating: 4)!
    
    let photo2 = UIImage(named: "meal2.jpg")!
    let meal2 = Meal(name: "Chicken and Potatoes", photo: photo2, rating: 5)!
    
    let photo3 = UIImage(named: "meal3.jpg")!
    let meal3 = Meal(name: "Pasta with Meatballs", photo: photo3, rating: 3)!
    
    meals += [meal1, meal2, meal3]
}
```

***检查点：***构建工程，应当能够顺利通过构建。

### 显示数据
为了显示动态的数据，表视图需要两个重要的辅助：数据源和委托。表视图数据源是给表视图提供需要显示的数据；表视图委托帮助表视图管理波表单元的选择、设置行高度和其它的属性。默认情况下，`UITableViewController`类及其子类使用`UITableViewDataSource`和`UITableViewDelegate`这两个协议来实现。所以我们需要实现这两个协议。

需要实现的数据源方法如下：
```Swift 
func numberOfSectionsInTableView(tableView: UITableView) -> Int
func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int
func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell
```

第一个方法告知表视图需要显示多少节。节是一组表单元的表示，在拥有大量数据时十分有用。对于我们这个简单应用来说，只需要一个节就足够了，所以`numberOfSectionsInTableView(_:)`的实现十分简单。
```Swift 
override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
    return 1
}
```

第二个方法告知表视图在给定的节中有多少行数据需要显示。这里，行数应该是Meals数组中Meal对象的个数。
```Swift 
override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
    return meals.count
}
```

最后一个方法配置如何显示一个单元行。对于拥有少量行的表视图，所有的行可能会在屏幕上直接全部显示，所以这个方法会被表的每一行进行调用。但是对于有大量行数据的表视图来说，每次只有少部分需要显示，所以只让需要显示的表单元进行调用是更高效的，`tableView(_:cellForRowAtIndexPath:)`便允许表视图这样做。

直接给出相应的代码和注释：
```Swift 
override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
    // Table view cells are reused and should be dequeued using a cell identifier.
    // 创建一个在Storyboard中定义过的标识的常量数据
    let cellIdentifier = "MealTableViewCell"
    // 从队列中通过cellIdentifier获取对应的单元
    let cell = tableView.dequeueReusableCellWithIdentifier(cellIdentifier, forIndexPath: indexPath) as! MealTableViewCell
    
    // Fetches the appropriate meal for the data source layout.
    // 获取单元对应的食物并进行配置
    let meal = meals[indexPath.row]
    
    cell.nameLabel.text = meal.name
    cell.photoImageView.image = meal.photo
    cell.ratingControl.rating = meal.rating
    
    return cell
}
```

最后一步是将自定义的表视图控制器与Storyboard中的场景进行连接。
1. 打开Storyboard。
2. 选中表视图控制器。
3. 打开标识指示器。
4. 设置"Class"为"MealTableViewController"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_inspector_identity_tablevc_2x.png)</center>

***检查点：***运行应用，可以看到如下的界面。注意到表视图与上方的状态栏有部分重叠，后面我们回来修复它。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_sim_finalUI_2x.png)</center>

### 给食物场景添加导航做准备
给应用添加导航，我们需要删除一些无用的UI和部分代码。

1. 打开Storyboard，并找到食物场景。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_mealsceneUI_old_2x.png)</center>
2. 选中Meal Name标签，按下"Delete"键来删除它。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_mealsceneUI_new_2x.png)</center>
3. 打开ViewController.swift。
4. 在ViewController.swift中，找到`textFieldDidEndEditing(_:)`方法。 
5. 删除标签属性部分代码。
    ```Swift
    mealNameLabel.text = textField.text
    ```
6. 删除mealNamelabel属性。
    ```Swift 
    @IBOutlet weak var mealNameLabel: UILabel!
    ```

重命名ViewController.swift文件。
1. 在项目导航栏处，单击"ViewController.swift"文件，然后按下回车键进行重命名。
2. 重命名为"MealViewController.swift"。按下回车键以确认。
3. 并将该文件中的ViewController类名更改为"MealViewController"。
    ```Swift 
    class MealViewController: UIViewController, UITextFieldDelegate, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    ```
4. 把最上方的文件注释信息也更改一下。
5. 打开Storyboard。
6. 通过单击场景以选中食物场景。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_scenedock_mealscene_2x.png)</center>
7. 打开标识指示器。
8. 设置"Class"为"MealViewController"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/7_mealscenefinal_2x.png)</center>

***检查点：*** 构建或运行应用，一切都应与之前相同。

## 导航
### 添加导航栏
导航控制器能够管理一系列视图控制器的前后转换。有导航控制器管理的视图控制器集合成为导航控制器的导航堆栈。堆栈中的第一个成为根视图控制器，并且永远不会从堆栈中移除。下面我们给食物列表场景添加一个导航控制器。
1. 打开Storyboard，选中表格视图控制器。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_scenedock_table_2x.png)</center>
2. 在菜单栏中选择`Editor > Embed In > Navigation Controller`。
    这一步会让Xcode在故事板中增加一个新的导航控制器，并设置它为故事板的入口，然后会给新的导航控制器与表视图控制器创建联系。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_navcontrolleradded_2x.png)</center>

在画布上，两个视图控制器之间的图标代表根视图控制器关系。故事板的入口被设置为导航控制器，因为导航控制器现在是表格控制器的容器。

注意到表视图控制器的上方现在有一个横栏，这个就是导航栏，在堆栈中的每一个控制器都有一个导航栏，导航栏包含向前和向后导航。接下来，我们回给这个导航栏增加一个导航到食物场景的按钮。

***检查点：***运行应用，可以看到如下的界面。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_sim_emptynavbar_2x.png)</center>

### 给场景配置导航栏
我们给导航栏增加一个标题和一个按钮。
1. 双击食物列表场景中的导航栏。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_rename_meallist_2x.png)</center>
    双击后，会出现光标，让你输入文本。
2. 输入"Your Meals"并按下回车键以保存。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_meallist_newname_2x.png)</center>
3. 打开对象库，选择"Bar Button Item"对象，并将它拖动到导航栏的最后侧。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_meallist_barbutton_2x.png)</center>
4. 选中这个导航栏按钮，并打开属性编辑器。
5. 设置"System Item"为"Add"。
    按钮会变为"+"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_meallist_addbutton_2x.png)</center>

***检查点：***运行应用，可以看到如下的界面。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_sim_navbar_2x.png)</center>

我们希望点击加号按钮后，能够进入食物场景中，所以这里我们需要增加一个进入食物场景的触发点。
1. 在画布上，选择添加按钮("+")。
2. 按住键盘上的"Control"并拖动到食物场景上。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_addbutton_drag_2x.png)</center>
    会弹出一个动作前进(Action Segue)菜单，如下所示：
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_addbutton_segue_2x.png)</center>
    动作前进菜单让我们选择在点击添加按钮后从食物列表视图转到食物视图使用哪一种类型的转换。
3. 在动作前进菜单中选择"show"。

Xcode会设置"show segue"，并会把食物场景配置到导航控制器中。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_showsegue_2x.png)</center>

***检查点：***运行应用，点击添加按钮，会进入食物场景。由于使用的是"show segue"，所以向后的返回导航会显示给我们，也就是说我们点击返回按钮可以返回到食物列表视图。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_sim_showsegue_2x.png)</center>

使用"show segue"的推入式导航并不完全是我们增加食物时想要的效果。被设计成向下进入界面的推入导航让我们可以在用户选择时提供更多的信息。添加一个新的数据，是一种模态操作————用户执行的动作是完整且自包含的，然后从该场景返回到主导航视图。这里最合适的呈现方式是使用"modal segue"。我们不需要删除之前的segue，只需要简单的更改属性即可。
1.选中食物列表场景与食物场景之间的segue。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_selectsegue_2x.png)</center>
2. 在属性编辑器中，设置"Segue"为"Present Modally"。
3. 设置"Identifier"为"AddItem"，并按下回车键以确认。
    后面我们会用到这个标识符。

模态视图控制器并不会添加到导航控制器堆栈中，所以在食物视图上方并不会有导航栏。下面我们给食物场景嵌入它自己的导航控制器。
1. 通过点击以选中食物场景。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_scenedock_mealscene_2x.png)</center>
2. 在菜单栏中选择`Editor > Embed In > Navigation Controller`。

与之前一样，Xcode会给食物场景增加一个导航栏。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_navcontroller_mealscene_2x.png)</center>

下面，我们给食物场景的导航栏添加标题和两个按钮。
1. 双击食物场景中的导航栏。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_rename_mealscene_2x.png)</center>
2. 输入"New Meal"并按下回车键以确认。
3. 从对象库中拖动"Bar Button Item"对象到导航栏的最左侧。
4. 在属性编辑器中，设置"System Item"为"Cancel"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_mealscene_cancelbutton_2x.png)</center>
5. 再拖动一个"Bar Button Item"到导航栏的最右侧。
6. 在属性编辑器中，设置"System Item"为"Save"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_mealscene_savebutton_2x.png)</center>

***检查点：***运行应用，点击添加按钮，会进入食物场景：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_sim_saveandcancel_2x.png)</center>

### 使用自动布局设置用户界面
先来对堆栈视图布局进行更新。
1. 在食物场景中，选中堆栈视图。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_selectstackview_2x.png)</center>
2. 在画布的右下角，打开"Resolve Auto Layout Issues"菜单。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_AL_resolvemenu_2x.png)</center>
3. 在"Selected Views"下方，选择"Update Constraints"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_stackview_updateconstraints_2x.png)</center>
    这一步会使堆栈视图与导航栏的下边框对齐。

食物场景约束和用户界面如下图所示：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_stackview_final_2x.png)</center>

***检查点：***运行应用，点击添加按钮，会进入与之前相同的食物场景：
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_sim_saveandcancel_2x.png)</center>

### 在食物列表中存储新的食物
在用户输入新的食物信息并点击保存按钮时，我们需要创建一个Meal对象并将其传递给MealTableViewController来显示。因此我们首先给MealViewController增加一个属性"Meal"。

打开MealViewController.swift，添加如下代码：
```Swift 
/*
This value is either passed by `MealListTableViewController` in `prepareForSegue(_:sender:)`
or constructed as part of adding a new meal.
*/
var meal = Meal?()
```

将保存按钮与代码连接：
1. 打开辅助编辑器，如果需要更大的空间，可以关闭导航栏和功能区。
2. 选择保存按钮，按住"Control"键拖动到代码中。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_savebutton_dragoutlet_2x.png)</center>
3. 在弹出的对话框中，设置"Name"为"saveButton"。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_savebutton_addoutlet_2x.png)</center>
4. 点击"Connect"。

接下来就是将Meal对象传递给MealTableViewController。为了完成这项工作，我们需要使用`unwind segue`。"unwind segue"允许用户从当前界面回退到任意一个已经存在的视图控制器，也即可以返回多级。这里我们使用`prepareForSegue(_:sender:)`这个方法来存储数据并在源视图控制器中做一些必要的清理工作。
1. 返回标准编辑器视图。
2. 在MealViewController.swift中增加一行注释。
    ```Swift 
    // MARK: Navigation
    ```
3. 在注释的下方，添加下列函数：
    ```Swift 
    // This method lets you configure a view controller before it's presented.
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // === 恒等运算符，检查saveButton是否与sender是同一个对象实例
        if saveButton === sender {
            // ?? 空值联合运算符，对一个可选值，有值时返回该值，无值时返回默认值
            let name = nameTextField.text ?? ""
            let photo = photoImageView.image
            let rating = ratingControl.rating
            
            // Set the meal to be passed to MealListTableViewController after the unwind segue.
            meal = Meal(name: name, photo: photo, rating: rating)
        }
    }
    ```

接下来，给MealTableViewController增加一个动作方法来实现转场。这个方法应该被标记为"IBAciont"，并且有一个segue参数(`UIStoryboardSegue`)。

打开MealTableViewController.swift，增加如下函数：
```Swift 
@IBAction func unwindToMealList(sender: UIStoryboardSegue) {
    /*  as? 可选类型强制转换符，将源视图控制器强制转换为MealViewController类型。
        如果强制转换不成功，则会返回nil，否则会赋值给本地变量sourceViewController,
        接着将sourceViewController.meal赋值给本地变量meal。
        最后执行if判断。
     */
    if let sourceViewController = sender.sourceViewController as? MealViewController, meal = sourceViewController.meal {
        // Add a new meal.
        let newIndexPath = NSIndexPath(forRow: meals.count, inSection: 0)
        meals.append(meal)
        // 插入新的表单元，并产生动画效果
        tableView.insertRowsAtIndexPaths([newIndexPath], withRowAnimation: .Bottom)
    }
}
```

现在，我们需要做的是将保存按钮与`unwindToMealList`方法连接起来：
1. 打开故事板，在画布上，按住"Control"键，拖动保存按钮到菜单场景的"Exit"上方。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_savebutton_dragunwind_2x.png)</center>
    接着会弹出一个对话框
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_savebutton_unwindsegue_2x.png)</center>
2. 从对话框菜单中选择`unwindToMealList:`。 

***检查点：***运行应用，点击添加按钮，创建新的事物，然后点击保存，在食物列表中应该能够看到新建的食物。

### 用户未输入食物名时，禁止保存
用户没有输入食物名就点击保存，会发生什么？新建的食物不会被创建并添加！有必要在用户未输入食物名时，禁止用户点击保存。
1. 在MealViewController.swift中，找到 `// MARK: UITextFieldDelegate`，在它的后添加一个新的方法：
    ```Swift 
    func textFieldDidBeginEditing(textField: UITextField) {
        // Disable the Save button while editing.
        saveButton.enabled = false
    }
    ```
    这个函数会在用户开始编辑的时候被调用。
2. 在上面的函数后面继续添加新函数：
    ```Swift 
    fucn checkValidMealName() {
        // Disable the Save button if the text field is empty.
        let text = nameTextField.text ?? ""
        saveButton.enabled = !text.isEmpty
    }
    ```
3. 找到"textFieldDidEndEditing(_:)"方法之后，增加如下代码：
    ```Swift 
    checkValidMealName()
    navigationItem.tile = textField.text
    ```
4. 在`viewDidLoad()`方法中添加：
    ```Swift 
    // Enable the Save button only if the text field has valid Meal name.
    checkValidMealName()
    ```

下面是完整的`viewDidLoad()`函数：
```Swift 
override func viewDidLoad() {
    super.viewDidLoad()

    // Handle the text field’s user input through delegate callbacks.
    nameTextField.delegate = self

    // Enable the Save button only if the text field has a valid Meal name.
    checkValidMealName()
}
```

完整的`textFieldDidEndEditing(_:)`方法：
```Swift 
func textFieldDidEndEditing(textField: UITextField) {
    checkValidMealName()
    navigationItem.title = textField.text
}
```

***检查点：***运行应用，点击添加按钮，在没有输入食物名的情况下，不能点击保存按钮。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_sim_savebuttondisabled_2x.png)</center>

### 取消新食物的添加
1. 打开故事板，开启辅助编辑器，选中取消按钮。
2. 按住键盘上的"Control"并拖动取消按钮到代码中。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_cancelbutton_dragaction_2x.png)</center>
3. 设置"Name"为"cancel"。
4. 设置"Type"为"UIBarButtonItem"，其它选项保持默认。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/8_cancelbutton_addaction_2x.png)</center>
5. 点击"Connect"。
    Xcode会产生如下代码：
    ```Swift 
    @IBAction func cancel(sender: UIBarButtonItem) {
    }
    ```
4. 在上述函数中添加代码：
    ```Swift 
    dismissViewControllerAnimated(true, completion: nil)
    ```
    这一步会不存储任何信息退出食物场景。

***检查点：***运行应用，点击添加按钮，再点击取消按钮，应该能够不添加食物而直接返回到食物列表界面。

## 实现编辑与删除
### 允许对已经存在的食物进行编辑
1. 返回标准编辑器，打开Storyboard。
2. 选中画布上的表视图单元。
3. 按住"Control"键，并拖动表单元到食物场景上。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_drag_tabletomealscene_2x.png)</center>
    会弹出一个菜单。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_seguemenu_2x.png)</center>
4. 选择"show"。
5. 拖动食物列表场景与食物场景之前的导航控制器以使新的`segue`显现。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_drag_navcontroller_2x.png)</center>
6. 在画布上选中新建的`segue`。 
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_selectsegue_2x.png)</center>
7. 在属性编辑器中，设置"Identifier"为"ShowDetail"。并按下回车键以确认。
    <center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_inspector_attributes_segue_2x.png)</center>

当`segue`被触发时，会将食物场景的视图控制器推入食物列表场景的导航控制器堆栈中。

***检查点：***运行应用，在食物列表场景中点击表单元，会导航到食物场景，但是内容为空。

现在的情况是，我们在同一个场景上有两个`segue`，素以我们需要一个确定用户正在使用哪一个的方法。之前我们使用了`prepareForSegue(_:sender:)`这个函数，这个函数在任意的`segue`执行时都会被调用。所以我们可以使用这个函数来确认哪一个`segue`正在被触发。
1. 打开MealTableViewController.swift，找到`prepareForSegue(_:sender:)`方法并去掉相应的注释。
2. 完整的代码如下：

```Swift 
override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
    // 点击表单元
    if segue.identifier == "ShowDetail" {
        let mealDetailViewController = segue.destinationViewController as! MealViewController
        
        // Get the cell that generated this segue.
        if let selectedMealCell = sender as? MealTableViewCell {
            let indexPath = tableView.indexPathForCell(selectedMealCell)!
            let selectedMeal = meals[indexPath.row]
            mealDetailViewController.meal = selectedMeal
        }
    }
    // 点击增加按钮
    else if segue.identifier == "AddItem" {
        print("Adding new meal.")
    }
}
```

在MealViewController.swift中我们需要实现部分工作来让用户界面正确地响应。在用户点击单元格时，我们应该显示该单元格的内容。
1. 打开MealViewController.swift，修改 `viewDidLoad()` 方法如下：


```Swift 
override func viewDidLoad() {
    super.viewDidLoad()
    
    // Handle the text field’s user input via delegate callbacks.
    nameTextField.delegate = self
    
    // Set up views if editing an existing Meal.
    if let meal = meal {
        navigationItem.title = meal.name
        nameTextField.text   = meal.name
        photoImageView.image = meal.photo
        ratingControl.rating = meal.rating
    }
    
    // Enable the Save button only if the text field has a valid Meal name.
    checkValidMealName()
}
```

***检查点：***运行应用，点击表单元来导航到食物场景中，应该看到如下所示界面。但是这个时候我们点击保存按钮，会新建一个食物而不是修改，所以接下来我们需要修复这个功能点。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_sim_editmeal_2x.png)</center>

修复这个功能点，我们需要更新`unwindToMealList(_:)`函数来处理两种不同的情况。更新后的函数如下：
```Swift
@IBAction func unwindToMealList(sender: UIStoryboardSegue) {
    if let sourceViewController = sender.sourceViewController as? MealViewController, meal = sourceViewController.meal {
        // 通过表视图中的某一行是否被选中来判断是否是新建食物信息
        if let selectedIndexPath = tableView.indexPathForSelectedRow {
            // Update an existing meal.
            // 更新已经存在的食物信息
            meals[selectedIndexPath.row] = meal
            tableView.reloadRowsAtIndexPaths([selectedIndexPath], withRowAnimation: .None)
        }
        else {
            // Add a new meal.
            // 新建一个食物信息
            let newIndexPath = NSIndexPath(forRow: meals.count, inSection: 0)
            meals.append(meal)
            tableView.insertRowsAtIndexPaths([newIndexPath], withRowAnimation: .Bottom)
        }
    }
}
```

***检查点：***运行应用，点击表单元并修改后，点击保存按钮能够覆盖掉之前的信息。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_sim_overwritemeal_2x.png)</center>


### 取消对已保存的食物信息的编辑
用户可能会决定不保存对一个食物的编辑，想返回到食物列表视图。因此我们需要更新取消按钮的行为。取消依赖于呈现的类型，需要对呈现的类型进行判断。当使用模态呈现的时候(点击增加按钮)，通过调用`dismissViewControllerAnimated(_:)`来取消；当通过推入导航呈现时，通过导航控制器来取消。
1. 打开MealViewController.swift。
2. 更新`cancel(_:)`函数如下：

```Swift
@IBAction func cancel(sender: UIBarButtonItem) {
    // Depending on style of presentation (modal or push presentation), this view controller needs to be dismissed in two different ways.
    // 根据呈现样式的不同来决定使用哪一个dismiss
    let isPresentingInAddMealMode = presentingViewController is UINavigationController
    
    if isPresentingInAddMealMode {
        dismissViewControllerAnimated(true, completion: nil)
    }
    else {
        navigationController!.popViewControllerAnimated(true)
    }
}
```

***检查点：***运行应用，在点击增加按钮后点击取消按钮，应该能够返回食物列表且不会增加新的食物。

### 删除食物
接下来，我们允许用户从食物列表中删除一个食物。我们需要在食物列表视图的导航栏上增加一个编辑按钮。
1. 打开MealTableViewController.swift。重写viewDidLoad()方法如下：

```Swift 
override func viewDidLoad() {
    super.viewDidLoad()
    
    // Use the edit button item provided by the table view controller.
    // 使用系统默认的编辑样式按钮。
    navigationItem.leftBarButtonItem = editButtonItem()
    
    // Load the sample data.
    loadSampleMeals()
}
```

***检查点：***运行应用，食物列表视图应该如下图所示。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_sim_editbutton_2x.png)</center>

完成编辑功能，我们需要实现表视图的委托方法`tableView(_:commitEditingStyle:forRowAtIndexPath:)`。这个方法用来管理处于编辑状态时的表中行的管理。

打开MealTableViewController.swift，修改该方法为：
```Swift 
// Override to support editing the table view.
override func tableView(tableView: UITableView, commitEditingStyle editingStyle: UITableViewCellEditingStyle, forRowAtIndexPath indexPath: NSIndexPath) {
    if editingStyle == .Delete {
        // Delete the row from the data source
        // 从数据源处删除行数据
        meals.removeAtIndex(indexPath.row)
        tableView.deleteRowsAtIndexPaths([indexPath], withRowAnimation: .Fade)
    } else if editingStyle == .Insert {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    }
}
```

***检查点：***运行应用，点击编辑按钮，点击表单元左侧的指示器，表单元右侧会出现"Delete"按钮让我们确认是否删除。另外，我们也可以通过在表单元上向左滑动来快速删除按钮，这是表视图的内建手势行为。
<center>![](https://developer.apple.com/library/prerelease/ios/referencelibrary/GettingStarted/DevelopiOSAppsSwift/Art/9_sim_deletebehavior_2x.png)</center>

## 持久化数据
### 保存和加载食物信息
使用`NSCoding`方法让`Meal`类能够控制存储和加载它的所有的属性。首先，我们创建一个储存关键字符串的结构体，来在代码中的各个地方都能使用常量来代替输入字符串。

在Meal.swift中，在`// MARK: Properties`节的下方定义：
```Swift
struct PropertyKey {
    static let nameKey = "name"
    static let photoKey = "photo"
    static let ratingKey = "rating"
}
```

为了能够编码和解码Meal类及其属性，Meal类需要实现`NSCoding`协议。实现这个协议，需要Meal继承自"NSObject"。按如下修改Meal类：
```Swift 
class Meal: NSObject, NSCoding {
```

NSCoding协议定义了两个方法用于编码和解码：
```Swift
func encodeWithCoder(aCoder: NSCoder)
init(coder aDecoder: NSCoder)
```

第一个方法将类的信息压缩，第二个方法将数据解压缩。下面是压缩函数（编码）的代码：

```Swift
func encodeWithCoder(aCoder: NSCoder) {
    // encodeObject方法将任意类型的对象进行编码，encodeInteger值对整型进行编码
    aCoder.encodeObject(name, forKey: PropertyKey.nameKey)
    aCoder.encodeObject(photo, forKey: PropertyKey.photoKey)
    aCoder.encodeInteger(rating, forKey: PropertyKey.ratingKey)
}
```

解压函数（解码）代码：
```Swift
// required表明方法必须被实现；convenience表明是第二级初始化函数
required convenience init?(coder aDecoder: NSCoder) {
    let name = aDecoder.decodeObjectForKey(PropertyKey.nameKey) as! String
    
    // Because photo is an optional property of Meal, use conditional cast.
    let photo = aDecoder.decodeObjectForKey(PropertyKey.photoKey) as? UIImage
    
    let rating = aDecoder.decodeIntegerForKey(PropertyKey.ratingKey)
    
    // Must call designated initializer.
    self.init(name: name, photo: photo, rating: rating)
}
```

更新Meal类的第一级初始化函数：
```Swift
init?(name: String, photo: UIImage?, rating: Int) {
    // Initialize stored properties.
    self.name = name
    self.photo = photo
    self.rating = rating
    
    super.init()
    
    // Initialization should fail if there is no name or if the rating is negative.
    if name.isEmpty || rating < 0 {
        return nil
    }
}
```

接下来，我们需要文件系统中的一个路径来存储数据。这里我们声明一个全局变量。在Meal.swift中`// MARK: Properties`下方增加代码：
```Swift 
// MARK: Archiving Paths
static let DocumentsDirectory = NSFileMannager().URLsForDirectory(.DocumentDirecotry, inDomains: .UserDomainMask).first!
static let ArchiveURL = DocumentsDirectory.URLByAppendingPathComponent("Meals")
```

***检查点：***按下"Comman+B"来进行构建，应该能够构建通过。

### 保存和加载食物列表
1. 打开MealTableViewController.swift，现在最后一个括号"}"前添加注释：
    ```Swift 
    // MARK: NSCoding
    ```
2. 添加新函数`saveMeals()`。

```Swift
func saveMeals() {
    let isSuccessfulSave = NSKeyedArchiver.archiveRootObject(meals, toFile: Meal.ArchiveURL.path!)
    if !isSuccessfulSave {
        print("Failed to save meals...")
    }
}
```
这个函数将meals数组进行打包到特定的位置，如果成功就返回true。

实现加载数据的函数：
```Swift
func loadMeals() -> [Meal]? {
    return NSKeyedUnarchiver.unarchiveObjectWithFile(Meal.ArchiveURL.path!) as? [Meal]
}
```

在用户增加、删除和编辑食物后保存食物列表，首先更新`MealTableViewController.swift`的`unwindToMealList()`函数：
```Swift
@IBAction func unwindToMealList(sender: UIStoryboardSegue) {
    if let sourceViewController = sender.sourceViewController as? MealViewController, meal = sourceViewController.meal {
        if let selectedIndexPath = tableView.indexPathForSelectedRow {
            // Update an existing meal.
            meals[selectedIndexPath.row] = meal
            tableView.reloadRowsAtIndexPaths([selectedIndexPath], withRowAnimation: .None)
        }
        else {
            // Add a new meal.
            let newIndexPath = NSIndexPath(forRow: meals.count, inSection: 0)
            meals.append(meal)
            tableView.insertRowsAtIndexPaths([newIndexPath], withRowAnimation: .Bottom)
        }
        // Save the meals.
        // 保存数据
        saveMeals()
    }
}
```

然后更新`MealTableViewController.swift`的`tableView(_:commitEditingStyle:forRowAtIndexPath:)`函数：
```Swift
// Override to support editing the table view.
override func tableView(tableView: UITableView, commitEditingStyle editingStyle: UITableViewCellEditingStyle, forRowAtIndexPath indexPath: NSIndexPath) {
    if editingStyle == .Delete {
        // Delete the row from the data source
        meals.removeAtIndex(indexPath.row)
        saveMeals()
        tableView.deleteRowsAtIndexPaths([indexPath], withRowAnimation: .Fade)
    } else if editingStyle == .Insert {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    }
}
```

现在，食物列表能够在合适的时间进行保存，我们还需要让食物信息在合适的时间被加载。接下来更改`viewDidLoad()`函数：
```Swift
override func viewDidLoad() {
    super.viewDidLoad()
    
    // Use the edit button item provided by the table view controller.
    navigationItem.leftBarButtonItem = editButtonItem()
    
    // Load any saved meals, otherwise load sample data.
    // 加载已经保存的数据，如果没有就加载示例数据
    if let savedMeals = loadMeals() {
        meals += savedMeals
    } else {
        // Load the sample data.
        loadSampleMeals()
    }
}
```

***检查点：***运行应用，增加一些食物信息，在下一次开启应用的时候，新增的食物信息会显示。到此为止，我们的应用完成了。

# 学习资源
以下是苹果官方的文档：

**注册成为一名开发者：** [App Distribution Quick Start](https://developer.apple.com/library/prerelease/ios/documentation/IDEs/Conceptual/AppStoreDistributionTutorial/Introduction/Introduction.html#//apple_ref/doc/uid/TP40013839)指导如何注册成为一名苹果开发者。  
**学习设计良好的应用界面；** [iOS Human Interface Guidelines](https://developer.apple.com/library/prerelease/ios/documentation/UserExperience/Conceptual/MobileHIG/index.html#//apple_ref/doc/uid/TP40006556)指导如何设计一致的用户界面。[Auto Layout Guides](https://developer.apple.com/library/prerelease/ios/documentation/UserExperience/Conceptual/AutolayoutPG/Introduction/Introduction.html#//apple_ref/doc/uid/TP40010853)指导如何穿件自适应的用户界面。  
**学习Swift编程语言：** [The Swift Programming Language](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/index.html#//apple_ref/doc/uid/TP40014097)讲述Swift语言的知识。  
**学习如何开发良好的应用：** [App Programming Guide for iOS](https://developer.apple.com/library/prerelease/ios/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40007072)讲解开发iOS应用你必须了解的最基本的事情。  
**学习能够使用的技术：** [iOS Technology Overview](https://developer.apple.com/library/prerelease/ios/documentation/Miscellaneous/Conceptual/iPhoneOSTechOverview/Introduction/Introduction.html#//apple_ref/doc/uid/TP40007898)讲解在iOS开发中慧使用的各种库及一些技巧。  
**调试和测试应用：** [Debugging with Xcode](https://developer.apple.com/library/prerelease/ios/documentation/DeveloperTools/Conceptual/debugging_with_xcode/index.html#//apple_ref/doc/uid/TP40015022)讲解如何使用Xcode调试和测试应用。  
**发布应用** [App Distribution Guide](https://developer.apple.com/library/prerelease/ios/documentation/IDEs/Conceptual/AppDistributionGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40012582) 指导如何进行内测和将应用发布到应用商店。

# 在Cocoa和Objective-C中使用Swift
Swift在设计之初就考虑到了与Cocoa和Objective-C的无缝兼容。在Swift中可以使用Objective-C的API，也可以在Objective-C中使用Swift API。

先来理解Swift的import过程：  
任何Objective-C库(或者C库)都能够被Swift当做一个模块直接导入。比如Objective-C常用的库：Foundation, UIKit, SpriteKit。导入Foundation库只需要一个import语句：
```Swift 
import Foundation
```
这个导入使得Foundation 的所有API，比如NSDate、NSURL、NSMutableData及其方法和属性等，都能被Swift直接使用。不过导入过程会将OC的部分类型转换为Swift语言相对应的类型。

下面介绍两种语言的互用性。
## 互用性
### 初始化
在Swift中初始化一个OC的类，我们可以使用Swift的语法来调用这个类的某一个初始化函数。"init"前缀会被对齐然后变为一个表明该方法是初始化函数的关键字。对于以"initWith"开头的初始化函数，"With"也会被丢弃。接着"init"或"initWith"后面的第一个单词首字母会变为小写，并且会被当做第一个参数名。其余的会作为另外的参数名。举例如下：

在OC中，我们可能会有如下初始化：
```Objective-C
UITableView *myTableView = [[UITableView alloc] initWithFrame:CGRectZero style: UITableViewStyleGrouped];
```
在Swift中，我们这样做：
```Swift
let myTableView: UITableView = UITableView(frame: CGRectZero, style: .Grouped)
```
我们不需要调用alloc，Swift会自动处理。注意到"init"没有在Swift的初始化调用中出现。

在初始化的过程中，我们可以明确的输入对象类型，或者省略类型。Swift的类型引用会自动正确地确定对象的类型。
```Swift
let myTextField = UITextField(frame: CGRect(x: 0.0, y: 0.0, width: 200.0, height: 40.0))
```

这些UITableView和UITextField对象拥有在OC中相同的功能。可以如在OC中一样使用它们，比如访问属性和调用方法。

为了一致性和简便性，OC的工厂方法会被映射为Swift中的"convenience initializer"。比如OC中的如下工厂方法：
```Objective-C
UIColor *color = [UIColor colorWithRed: 0.5 green: 0.0 blue: 0.5 alpha: 1.0];
```
在Swift中我们可以这样调用：
```Swift 
let color = UIColor(red: 0.5, green: 0.0, blue: 0.5, alpha: 1.0)
```

### 允许失败的初始化
在OC中，初始化函数直接返回它初始化的对象。为了通知调用者初始化失败，OC初始化会返回nil。在Swift中，这一模式被内建为一种语言特性——`failable initialization`。使用`init(...)`表示一定能成功的初始化，`init?(...)`表示可能会失败的初始化。比如`UIImage(contentsOfFile:)`初始化在图像文件不存在时会失败。我们可以使用可选绑定来拆包这个初始化的结果：
```Swift 
if let image = UIImage(contentsOfFile: "MyImage.png") {
    // loaded the image successfully
} else {
    // could not load the image
}
```

### 访问属性
访问和设置OC对象的属性使用点语法：
```Swift 
myTextField.textColor = UIColor.darkGrayColor()
myTextField.text = "hello world"
```

### 类方法
在Swift中调用OC方法也使用点语法：

OC函数：
```Objective-C
[myTableView insertSubview: mySubview atIndex: 2];
```
Swift函数：
```Swift 
myTableView.insertSubview(mySubview, atIndex: 2)
```

### id兼容性
Swift使用一个名为`AnyObject`的协议类型来表示任一种类型，OC中使用`id`。因此Swift会将OC中的id映射为AngObject。我们可以给AnyObject赋值为任何一个类型的对象，我们还可以更改为另外一种类型的对象。
```Swift 
var myObject: AnyObject = UITableViewCell()
myObject = NSDate()
```

不过，由于AnyObject对象的类型只能在运行时确定，所以很可能会编写不安全的代码，很可能产生运行时错误。我们可以采用Swift中的可选来消除这一类型的错误。当我们调用一个AnyObject对象的方法时，这个调用会作为隐式拆包可选来进行。

> AnyObject的属性访问总是返回一个可选值。

下面的例子中，第一行与第二行代码并不会得到执行，因为NSDate对象并不具有count属性和characterAtIndex方法。myCount常量会被推断为可选Int型，然后设置为nil。我们可以使用if-let语句来按条件拆包一个方法的执行结果。
```Swift 
let myCount = myObject.count
let myChar = myObject.characterAtIndex?(5)
if let fifthCharacter = myObject.characterAtIndex?(5) {
    print("Found \(fifthCharacter) at index5")
}
```

SWift中，将AnyObject向下转换到一个具体的对象类型并不能保证成功，所以会返回一个可选值。我们可以检查这个可选值来确定是否能够转换成功。
```Swift 
let userDefaults = NSUserDefaults.standardUserDefaults()
let lastRefershDate: AnyObject? = userDefaults.objectForKey("LastRefreshDate")
if let date = lastRefershDate as? NSDate {
    print("\(date.timeIntervalSinceReferenceData)")
}
```

当然，在我们确定对象的类型不为空时，我们可以强制转换。
```Swift 
let myDate = lastRefershDate as! NSDate
let tiemInterval = myDate.timeIntervalSinceReferenceData
```

### 可空与可选
OC中我们使用指针来引用对象，指针可能为NULL。在Swift中，所有的值，包括结构体和对象引用，保证为非空。我们使用可选类型来表示一个值可能为空。

OC:
```Objective-C
@property (nullable) id  nullableProperty;
@property (nonnull) id nonNullProperty;
@property id unannotatedProperty;
 
NS_ASSUME_NONNULL_BEGIN
- (id)returnsNonNullValue;
- (void)takesNonNullParameter:(id)value;
NS_ASSUME_NONNULL_END
 
- (nullable id)returnsNullableValue;
- (void)takesNullableParameter:(nullable id)value;
 
- (id)returnsUnannotatedValue;
- (void)takesUnannotatedParameter:(id)value;
```

Swift:
```Swift
var nullableProperty: AnyObject?
var nonNullProperty: AnyObject
var unannotatedProperty: AnyObject!
 
func returnsNonNullValue() -> AnyObject
func takesNonNullParameter(value: AnyObject)
 
func returnsNullableValue() -> AnyObject?
func takesNullableParameter(value: AnyObject?)
 
func returnsUnannotatedValue() -> AnyObject!
func takesUnannotatedParameter(value: AnyObject!)
```

### 扩展
Swift扩展(Extension)与OC的category类似。扩展允许给一个已经存在的类、结构体和枚举等增添行为。

我们给UIBezierPath类进行扩展使它能够创建等边三角形的简单Bézier路径。
```Swift 
extension UIBezierPath {
    convenience init(triangleSideLength: CGFloat, origin: CGPoint) {
        self.init()
        let squareRoot = CGFloat(sqrt(3.0))
        let altitude = (squareRoot * triangleSideLength) / 2
        moveToPoint(origin)
        addLineToPoint(CGPoint(x: origin.x + triangleSideLength, y: origin.y))
        addLineToPoint(CGPoint(x: origin.x + triangleSideLength / 2, y: origin.y + altitude))
        closePath()
    }
}
```

我们还可以使用扩展增加属性。
```Swift
extension CGRect {
    var area: CGFloat {
        return width * height
    }
}
let rect = CGRect(x: 0.0, y: 0.0, width: 10.0, height: 50.0)
let area = rect.area
```

### 闭包
OC中的代码块(Block)会自动作为Swift闭包(Closure)导入。

OC:
```Objective-C
void (^completionBlock)(NSData *, NSError *) = ^(NSData *data, NSError *error) {
   /* ... */
}
```

```Swift
let completionBlock: (NSData, NSError) -> Void = { (data, error) in
    /* ... */
}
```

### 对象比较
在Swift中有两种类型的对象比较。第一是是相等比较`==`，比较对象的内容；第二种是恒等`===`，比较是否是同一个对象实例。

### 轻量级的范型
OC中的NSArray, NSSet, NSDictionary类型使用轻量级的范型参数，Swift导入后会将相应的内容类型信息保留。

OC:
```Objective-C
@property NSArray<NSDate *>* dates;
@property NSSet<NSString *>* words;
@property NSDictionary<KeyType: NSURL *, NSData *>* cachedDate;
```

Swift:
```Swift
var dates: [NSDate]
var words: Set<String>
var cachedData: [NSURL: NSData]
```

### OC选择器
OC选择器是一种能够引用OC中某一个方法的类型。在Swift中，OC选择器由Selector结构体代替。
```Swift
import UIKit
class MyViewController: UIViewController {
    let myButton = UIButton(frame: CGRect(x: 0, y: 0, width: 100, height: 50))
    
    override init?(nibName nibNameOrNil: String?, bundle nibBundleOrNil: NSBundle?) {
        super.init(nibName: nibNameOrNil, bundle: nibBundleOrNil)
        myButton.addTarget(self, action: "tappedButton:", forControlEvents: .TouchUpInside)
    }
    
    func tappedButton(sender: UIButton!) {
        print("tapped button")
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
    }
}
```

## 编写具有OC行为的Swift类
### 从OC类继承
继承使用冒号语法：
```Swift
import UIKit
class MySwiftViewController: UIViewController {
    // define the class
}
```

### 配置类属性的属性
#### Strong和Weak
Swift的属性默认为strong。使用weak关键词表明一个属性对存储确定值的对象拥有弱引用。这个关键词只有在属性是可选类类型时使用。

### Read/Write和Read-Only
在Swift中并没有readwrite和readonly。声明属性的时候使用let表明是read-only，使用var表明是read/write。

#### copy语法
在Swift中，OC的copy属性被转换为@NSCopying。

### Cocoa数据类型
#### 字符串
Swift将String类型与NSString类进行了自动桥接。事实上，Swift导入OC API时，会将所有的NSString转换为String类型。所以我们应该更经常使用String对象。NSSting总是能够转换为String。
```Swift 
import Foundation
let myString: NSString = "123"
if let integerValue = Int(myString as String) {
    print("\(myString) is the integer \(integerValue)")
}
// prints "123 is the integer 123"
```

此外，在OC中我们常常使用NSLocalizedString一系列宏来本地化字符串，在Swift中我们只需要使用单一的范数来进行本地化——`NSLocalizedString(key:tableName:bundle:value:comment:)`。

#### 集合类
Swift将NSArray, NSSet, NSDictionary与Array, Set, Dictionary进行了桥接。

OC:
```Objective-C
@property NSDictionary<NSURL *, NSData *>* cachedData;
- (NSDictionary<NSURL *, NSNumber *> *)fileSizesForURLsWithSuffix:(NSString *)suffix;
- (void)setCacheExpirations:(NSDictionary<NSURL *, NSDate *> *)expirations;
```

Swift:
```Swift 
var cachedData: [NSURL: NSData]
func fileSizesForURLsWithSuffix(suffix: String) -> [NSURL: NSNumber]
func setCacheExpirations(expirations: [NSURL: NSDate])
```

### Cocoa设计模式
#### 委托
```Swift 
class MyDelegate: NSObject, NSWindowDelegate {
    func window(NSWindow, willUseFullScreenContentSize proposedSize: NSSize) -> NSSize {
        return proposedSize
    }
}
var myDelegate: NSWindowDelegate? = MyDelegate()
if let fullScreenSize = myDelegate?.window?(myWindow, willUseFullScreenContentSize: mySize) {
    print(NSStringFromSize(fullScreenSize))
}
```

#### 错误处理
捕获和处理错误，OC:
```Objective-C
NSFileManager *fileManager = [NSFileManager defaultManager];
NSURL *URL = [NSURL fileURLWithPath:@"/path/to/file"];
NSError *error = nil;
BOOL success = [fileManager removeItemAtURL:URL error:&error];
if (!success && error) {
    NSLog(@"Error: %@", error.domain);
}
```

```Swift 
let fileManager = NSFileManager.defaultManager()
let URL = NSURL.fileURLWithPath("/path/to/file")
do {
    try fileManager.removeItemAtURL(URL)
} catch let error as NSError {
    print("Error: \(error.domain)")
}
```

抛出异常，OC:
```Objective-C
// an error occurred
if (errorPtr) {
   *errorPtr = [NSError errorWithDomain:NSURLErrorDomain
                                   code:NSURLErrorCannotOpenFile
                               userInfo:nil];
}
```

Swift:
```Swift
// an error occurred
throw NSError(domain: NSURLErrorDomain, code: NSURLErrorCannotOpenFile, userInfo: nil)
```

#### 键值观察
键值观察是一种允许对象在两一个对象的某一个属性改变时得到通知的机制。
1. 给想要观察的属性添加一个`dynamic`修饰器。
    ```Swift 
    class MyObjectToObserve: NSObject {
        dynamic var myDate = NSDate()
        func updateDate() {
            myDate = NSDate()
        }
    }
    ```
2. 创建一个全局变量
    ```Swift 
    private var myContext = 0
    ```
3. 给键路径创建一个观察者，重写函数`observeValueForKeyPath:ofObject:change:context:`,然后在`deinit`中移除观察者。
    ```Swift 
    class MyObserver: NSObject {
        var objectToObserve = MyObjectToObserve()
        override init() {
            super.init()
            objectToObserve.addObserver(self, forKeyPath: "myDate", options: .New, context: &myContext)
        }
        
        override func observeValueForKeyPath(keyPath: String?, ofObject object: AnyObject?, change: [NSObject : AnyObject]?, context: UnsafeMutablePointer<Void>) {
            if context == &myContext {
                if let newValue = change?[NSKeyValueChangeNewKey] {
                    print("Date changed: \(newValue)")
                }
            } else {
                super.observeValueForKeyPath(keyPath, ofObject: object, change: change, context: context)
            }
        }
        
        deinit {
            objectToObserve.removeObserver(self, forKeyPath: "myDate", context: &myContext)
        }
    }
    ```

#### 内省法
在OC中我们使用`isKindOfClass:`来检查对象是否是某一个类的对象，`conformsToProtocol:`检查对象是否实现了特定的协议。在Swift中，我们使用`is`操作符和`as?`操作符来完成。

```Swift 
if object is UIButton {
    // object is of type UIButton
} else {
    // object is not of type UIButton
}

if let dataSource = object as? UITableViewDataSource {
    // object conforms to UITableViewDataSource and is bound to dataSource
} else {
    // object not conform to UITableViewDataSource
}
```

### 与C API 进行交互
#### 基本类型

C类型 | Swift类型
-----|---------
bool | CBool
char, signed char | CChar
unsigned char | CUnsignedChar
short|CShort
unsigned short|CUnsignedShort
int|CInt
unsigned int|CUnsignedInt
long|CLong
unsigned long|CUnsignedLong
long long|CLongLong
unsigned long long|CUnsignedLongLong
wchar_t|CWideChar
char16_t|CChar16
char32_t|CChar32
float|CFloat
double|CDouble

#### 指针

C Syntax|Swift Syntax
------|------
const Type * | UnsafePointer<Type>
Type * | UnsafeMutablePointer<Type>

## Swift与OC混合编程
OC和Swift能够在同一个项目中共存，处理流程依据编写app还是库而有所不同。
<center>![](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/BuildingCocoaApps/Art/DAG_2x.png)</center>


### 将OC导入Swift
将OC导入Swift需要依赖`Objective-C bridging header`的帮助。
<center>![](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/BuildingCocoaApps/Art/bridgingheader_2x.png)</center>
点击"Yes"后Xcode会额外创建一个头文件，并会命名为项目名+"-Bridging-Header.h"。

我们需要进一步编写这个头文件以将OC的代码暴露给Swift进行调用。
1. 在新建的桥接头文件中，导入所有的想要暴露给Swift的OC头文件。例如：
    ```Objective-C
    #import "XYZCustomer.h"
    #import "XYZCustomerView.h"
    #import "XYZCustomerViewController.h"
    ```
2. 在构建设置`Building Settings`中，确保`Swift Compiler - Code Generation`下的`Objective-C Bridging Header`包含指向该头文件的路径。

任何在这个桥接头文件中列出的公众OC头文件都对Swift可见。OC文件中的功能在Swift文件中可以自动变为可用，不用使用import语句。
```Swift 
let myCell = XYZCustomCell()
myCell.subtitle = "A custom cell"
```

### 将Swift导入OC
与将OC导入Swift类似，将Swift导入OC中时，我们依赖于Xcode产生的头文件来将这些文件暴露给OC。这个头文件的名称一般为项目名+"-Swift.h"。默认情况下，产生的头文件会包含使用`public`修饰的Swift声明，并且如果项目使用了桥接头文件还会包含使用了`internal`修饰的Swift声明。使用`private`修饰的声明不会被包含在这个头文件中，除非明确地使用了`@IBAction`,`@IBOutlet`,`@objc`。

基本上不用做任何事情来产生这个文件，直接在OC中导入这个文件就可以使用文件的内容。如果在Swift中使用了自定义的OC类型，请确保在导入这个Swift头文件前将这些类型的OC头文件导入到想要访问Swift代码的OC ".m"文件中。
```Objective-C
#import "ProductModuleName-Swift.h"
```

代码 |导入Swift | 导入OC
--|---------|-------
Swift代码 | 不需要import | #import "ProductModuleName-Swift.h"
OC代码 | 不需要import语句；需要OC桥接头文件 | #import "Header.h"

### 在同一个库中导入代码
编写混合语言的库时，需要额外注意。

将OC导入Swift：
1. 在`Building Settings`中，设置`Packaging`中的`Defines Module`为`Yes`。
2. 使用尖括号包含头文件。
    ```Swift
    #import <XYZ/XYZCustomCell.h>
    ```

将Swift导入OC：
1. 在`Building Settings`中，设置`Packaging`中的`Defines Module`为`Yes`。
2. 使用尖括号包含头文件。
    ```Objective-C
    #import <ProductName/ProductModuleName-Swift.h>
    ```

### 导入外部库

库 | 导入Swift | 导入OC 
---|----------|------
任意语言的库 | `import FrameWorkName` | `@import FrameworkName;`


### 在OC中使用Swift
将Swift代码导入OC中后，需要使用规范的OC语法来操作Swift类。
```Swift 
MySwiftClass *swiftObject = [[MySwiftClass alloc] init];
[swiftObject swiftMethod];
```

Swift中的类或协议必须被标记为`@objc`才能在OC中访问和使用。

在OC头文件中引用Swift类或协议：
```Swift 
// MyObjcClass.h
@class MySwiftClass;
@protocol MySwiftProtocol;
 
@interface MyObjcClass : NSObject
- (MySwiftClass *)returnSwiftClassInstance;
- (id <MySwiftProtocol>)returnInstanceAdoptingSwiftProtocol;
/* ... */
@end
```

### 为OC接口重写Swift方法名
Swift编译器会自动导入OC代码作为conventional代码，将OC的工厂方法变为初始化方法。可能存在一些边界情况导致代码不能正确处理。所以需要进行进一步处理。

工厂方法可能出现问题，我们可以使用`NS_SWIFT_NAME`宏来使其正确地处理:
```Objective-C
+ (instancetype)recordWithRPM:(NSUInteger)RPM NS_SWIFT_NAME(init(RPM:));
+ (id)recordWithQuality:(double)quality NS_SWIFT_NAME(record(quality:));
```

枚举类型，可以使用`NS_SWIFT_NAME`宏来处理：
```Objective-C
typedef NS_ENUM(NSInteger, ABCRecordSide) {
  ABCRecordSideA,
  ABCRecordSideB NS_SWIFT_NAME("FlipSide"),
};
```

### 故障建议和提示
* 将Swif与OC文件作为同一个代码集，注意命名冲突。
* 在制作库时，确保设置`Packaging`中的`Defines Module`为`Yes`。
* OC桥接文件中，确保`Swift Compiler - Code Generation`下的`Objective-C Bridging Header`包含指向该头文件的路径。
* Xcode使用product module name而不是target name来命名桥接文件和给OC用的Swift头文件。
* Swift类必须是OC类的子类或者被标记为`@objc`才能被OC使用。
* 如果在Swift中使用了自定义的OC类型，请确保在导入这个Swift头文件前将这些类型的OC头文件导入到想要访问Swift代码的OC ".m"文件中。

## 将OC代码迁移到Swift
迁移用来重新审视现存的OC应用，通过使用Swift来改善应用的架构、逻辑和性能。





























