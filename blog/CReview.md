Title:   CReview
Brief:   保研复试C语言复习。
Authors: Jin Jay
Date:    2014-09
codehilite: true
base_url: http://jinjaysnow.github.io

## 保研复试C语言复习
### C与指针
**函数指针**
>函数指针是指向函数的指针变量。C在编译时，每一个函数都有一个入口地址，该入口地址就是函数指针所指向的地址。有了指向函数的指针变量后，可用该指针变量调用函数，就如同用指针变量可引用其他类型变量一样。函数指针有两个用途：调用函数和做函数的参数。

```
#include <stdio.h>

int maxAB(int a, int b) {
    return a>b?a:b;
}
int minAB(int a, int b) {
    return a>b?b:a;
}
// 指针函数作为参数
void funPAsArg(int (*f)(int a, int b), int a, int b){
    printf("result: %d\n", (*f)(a, b));
}

int main(){
    unsigned int a = 0x80000000;    // a=2147483648
    unsigned int b = 0xffffffff;    // b=4294967295
    int m = a;                      // m=-2147483648 = -2^31
    int n = b;                      // n=-1
    unsigned int x = a - b;         // x=2147483649
    unsigned int y = a + b;         // y=2147483647
    int k = m - n;                  // k=-2147483647
    int j = m + n;                  // j=2147483647
    int (*funcpointer)(int, int);   // 定义函数指针
    funcpointer = maxAB;            // 函数指针赋值
    printf("funcpointer: %x\n", funcpointer);
    funPAsArg(funcpointer, m, n);
    funcpointer = minAB;
    printf("minAB: %d\n", (*funcpointer)(m, n));
    // 计算机内部对数的运算
    printf("a=%u, b=%u, m=%d, n=%d, x=%u, y=%u, k=%d, j=%d\n", a, b, m, n, x ,y ,k ,j);
    printf("a=%x, b=%x, m=%x, n=%x, x=%x, y=%x, k=%x, j=%x\n", a, b, m, n, x ,y ,k ,j);
    return 0;
}
```
**指针变量**
>存放地址的变量称为指针变量。指针变量是一种特殊的变量，它不同于一般的变量，一般变量存放的是数据本身，而指针变量存放的是数据的地址。

```
#include <stdio.h>

int main(){
    int a[4][4] = {
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 1, 2, 3,
        4, 5, 6, 7
    };
    int (*p)[4];    // p指向有四个整形元素的数组
    p = a;
    printf("%d\n", (*(p+1))[2]);
    return 0;
}
```

### 几个基本概念

#### switch()语句
switch(c)语句中c可以是int, long, char, unsigned int。不能是浮点型数据。case语句中也不能有变量。

#### for循环
```
#include <stdio.h>
int main(int argc, char const *argv[]) {
    int i = 0;
    for ( i = 0, printf("First = %d ", i); printf("Second = %d ", i), i < 3; ++i, printf("Third = %d ", i)) {
        printf("Fourth = %d\n", i);
    }
    return 0;
}
```

输出结果为
```
First = 0 Second = 0 Fourth = 0
Third = 1 Second = 1 Fourth = 1
Third = 2 Second = 2 Fourth = 2
Third = 3 Second = 3 
```

[TOC]
