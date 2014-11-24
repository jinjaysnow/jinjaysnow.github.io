Author: JinJay
Date: 2014-05
Title: Scheme语言学习
description: 记录Scheme语言的学习，主要是常用函数的运用。
keywords: Scheme

# MIT-Scheme学习
**平台：** Mac OS X
## 安装
建议使用homebrew进行安装：

    brew install mit-scheme

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
