Author: JinJay
Date: 2014-05
Title: Scheme语言学习
description: 记录Scheme语言的学习，主要是常用函数的运用。
keywords: Scheme

<h1>MIT-Scheme学习</h1>
**平台：** Mac OS X
## 安装
建议使用homebrew进行安装：

    brew install mit-scheme

## 变量
### 变量定义

    (define (var params) (body))

### 更改变量值

    (set! var value)

## 基本数据结构
### boolean
\#t、\#f代表true、false。boolean只有一个操作not，not后面不是#f，一律返回#t。

### number
整数(define i 1)、有理数(define p 3.14)、实数(define f 22/7)、复数(define c 3+2i)。  
二进制(#b10100)、八进制(#o567)、十六进制(#xfff)

### char
以\#\\开始。`#\space`表示空格，`#\newline`表示换行符。

### 符号类型
`(define a 'xyz)`或`(define a (quote xyz)):a的值为xyz。相当于枚举。  
**符号类型与字符串不同的是符号类型不能象字符串那样可以取得长度或改变其中某一成员字符的值，但二者之间可以互相转换。**

### string
使用双引号括起来。  
**取得字符串长度**

    (string-length str)

**设置字符串某一个位置字符(位置从0开始)**

    (string-set! str pos char)

### pair
`(cons a b)`定义成`a.b`，a为这个pair的car，b为pair的cdr。使用如下命令设置  

    (set-car! var val)
    (set-cdr! var val)

### list
`(list val1 val2 ..)`，获取长度使用`(length alist)`，获取特定位置(从0开始)值使用(`list-ref alist pos)`，创建列表使用`(make-list num val)`。  
**事实上列表是在点对的基础上形成的一种特殊格式。**

### vector
向量，一种元素按照整形索引的对象。

    (define v #(1 2 3 4))

## 基本运算
### 类型判断

    (boolean? *)
    (char? *)
    (integer? *) 
    (rational *)
    (real *)
    (number *)
    (symbol? *)
### 比较
`eq?`是判断两个参数是否指向同一个对象，如果是才返回#t；`equal?`则是判断两个对象是否具有相同的结构并且结构中的内容是否相同，它用`eq?`来比较结构中成员的数量；`equal?`多用来判断点对，列表，向量表，字符串等复合结构数据类型。

### 算术运算
+、-、\*、/和expt(指数运算)。

### 转换

    (number->string 123)  ; 数字转换为字符串
    "123"
    (string->number "456")  ; 字符串转换为数字
    456
    (char->integer #\a)   ;字符转换为整型数，小写字母a的ASCII码值为96
    97
    (char->integer #\A)  ;大写字母A的值为65
    65
    (integer->char 97)  ;整型数转换为字符
    #\a
    (string->list "hello")   ;字符串转换为列表
    (#\h #\e #\l #\l #\o) 
    (list->string (make-list 4 #\a)) ; 列表转换为字符串
    "aaaa"
    (string->symbol "good")  ;字符串转换为符号类型
    good
    (symbol->string 'better)  ;符号类型转换为字符串
    "better"


## 过程定义

    (define 过程名 ( lambda (参数 ...) (操作过程 ...)))  ;使用lambda
    (define (过程名 参数) (过程内容 …))                  ;不适用lambda

使用proc代表一个过程参数，例如：

    (define fun
        (lambda(proc x y)
                (proc x y)))

## 常用结构
### 顺序结构
使用`(begin (expr1) (expr2) ..)`。

    (begin (display "hello world")
           (newline))  ;经典的helloworld程序
### if结构

    (if test pro1 pro2) ;pro2可省略，相当于没有else

### cond结构
    (cond (condition1 pro1)
          (condition2 pro2)
          (...)
          (else elsepro))

### case结构
    (case (表达式) ((值) 操作))   ... (else 操作)))

### 其他
`(and )`与`(or )`或。

## 递归
    (define  factoral (lambda (x)
        (if (<= x 1) 1
            (* x (factoral (- x 1))))))

    (define (factoral n)
        (define (iter product counter)
            (if (> counter n)
            product
            (iter (* counter product) (+ counter 1))))
        (iter 1 1))

**在Scheme语言中只有通过递归才能实现循环**

    (define loop
        (lambda(x y)
            (if (<= x y)
            (begin (display x) (display #\\space) (set! x (+ x 1))
                    (loop x y)))))

## 变量
### 局部变量
`(let ((var1) (var2)...) sentence)`

    (let ((x 2) (y 5))
        (let* ((x 6)(z (+ x y)))  ;此时x的值已为6，所以z的值应为11，如此最后的值为66
        (* z x)))
    (letrec ((even?
                (lambda(x)
                (if (= x 0) #t
                        (odd? (- x 1)))))
            (odd?
                (lambda(x)
                (if (= x 0) #f
                        (even? (- x 1))))))
        (even? 88))

**letrec将内部定义的过程或变量间进行相互引用。.**

### apply
apply的功能是为数据赋予某一操作过程，它的第一个参数必须是一个过程，随后的其它参数必须是列表.

### map
map的功能和apply有些相似，它的第一个参数也必需是一个过程，随后的参数必需是多个列表，返回的结果是此过程来操作列表后的值。

## 输入和输出

    (current-input-port)
    (current-output-port)
    (open-input-file)
    (close-output-file)
    (read) ;不带参数时等待键盘输入
    (write 对象 端口) ;对象值要输出的信息，端口指要输出的端口号或者文件



### 一个小题
> 依序遍历 0 到 100 闭区间内所有的正整数，如果该数字能被 3 整除，则输出该数字及 ‘\*’ 标记；如果该数字能被 5 整除，则输出该数字及 ‘#’ 标记；如果该数字既能被 3 整除又能被 5 整除，则输出该数字及 ‘\*#’ 标记。

#### C语言实现
```
for (int i = 1; i <= 100; i++) {
    if (i % 3 == 0) {
        if (i % 5 == 0) {
            printf("%d*#", i);
        } else {
            printf("%d*", i);
        }
    } else {
        if (i % 5 == 0) {
            printf("%d#", i);
        } else {
            ; // Do nothing
        }
    }
}
```

#### Scheme语言实现
```
#lang racket
(require math/number-theory)
(require racket/match)

(define (range-closed from to [step 1])
  (range from (+ 1 to) step))

(let ([numbers (range-closed 1 100)])
  (for ([x numbers])
    (match `(,(divides? 3 x) . ,(divides? 5 x))
      ['(#t . #t) (printf "~A*#" x)]
      ['(#t . #f) (printf "~A*" x)]
      ['(#f . #t) (printf "~A#" x)]
      [else (void)])))
```



[TOC]
