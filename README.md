
### 从零构造一台模拟计算机

本项目旨在从基础逻辑门开始，一步一步自底向上，经历CPU，汇编，虚拟机，高级语言，操作系统（库函数），构建起整个计算机硬件和软件体系，使其能在模拟器上运行，且配套的高级语言可编写简易游戏运行在该模拟计算机上。

该项目层次如下：

- 基础逻辑门

  使用硬件设计语言(hdl)，以与非门为基础，在硬件模拟器上构建了and dmux mux not or xor等逻辑门。

  ![11](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/11.png)

  在硬件模拟器（HardwareSimulator.bat）上运行代码并测试，图为and门，测试结果正确。

  

  ![12](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/12.png)

- 算术逻辑单元（ALU）

  使用基础逻辑门，实现了半加器，全加器，加法器，增量器，最后组装成ALU。
  ![21](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/21.png)

  将组装好的ALU在硬件模拟器上运行，测试结果如下，正确。

  ![22](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/22.png)

- RAM

  以DFF门为基础，实现了触发器，计数器，与多位寄存器。

  ![31](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/31.png)

  RAM16K测试无误。

  ![32](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/32.png)

- 计算机硬件模拟整合

  以之前实现的模块为基础，整合为一个16位冯诺依曼机的硬件平台，有3个寄存器（数据寄存器，地址寄存器，程序计数器），两个内存模块（指令内存与数据内存），两个内存映像I/O设备（屏幕键盘）。整体内存前16K划分为RAM（即指令内存与数据内存），16K-24K划为屏幕内存映像与键盘内存映像。

  ![41](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/41.png)

  在硬件模拟器上测试无误。

  ![42](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/42.png)

- 汇编语言设计

  基于此前实现的硬件平台设计一种汇编语言，每条指令16位宽，支持直接寻址，立即寻址，间接寻址三种寻址方式，通过内存映射操作IO设备。

  分为2种指令：

  - A指令：@value

    作用：

    - 为A寄存器（地址寄存器）设置15位的值。
    - 唯一一种将常数输入计算机的方法。
    - 将目标数据内存单元地址存入A寄存器中，为将来相应C指令提供地址。
    - 为执行跳转的C指令提供条件。

  - C指令：dest=comp;jump

    作用：

    - comp表示计算什么。
    - dest指明结果存放到什么地方。
    - jump描述转移条件。

  有6种符号：

  - 预定义符号：RAM地址特殊子集，可通过预定义符号被所有汇编程序引用
  - 虚拟寄存器：用R0到R15代表0到15号RAM地址
  - 预定义指针：SP，LCL，ARG，THIS，THAT被预定为0到4号内存地址
  - I/O指针：SREEN和KBD表示RAM地址16384（0x4000）和24576（0x6000），即屏幕和键盘基地址。
  - 标签符号：用户自定义标签来标记goto命令跳转目的地址，一个标签只能被定义一次，可在全局使用（即时出现在定义之前）。
  - 变量符号：若某符号非预定义符号也非标签，则被视为变量，并赋予其一个独立的内存地址（从RAM16，即0x0010开始）

  可通过“//”注释。

  以此汇编语言规范编写了一个乘法程序，在CPU模拟器上运行测试，结果正确。

  ![51](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/51.png)

- 汇编器实现

  使用Python作为实现语言，编写一个将汇编语言译为机器码的汇编器程序。

  包含以下模块：

  - gui_path_select：构造选择路径GUI，返回所选择文件的路径。
  - process：传入原始文本，返回无空白无注释，按行分割的字符串列表，每个列表元素是一条指令。
  - sym_pro：处理符号。
  - trans_a：传入指令列表，翻译a指令。
  - parser：传入c指令，将其切分为一个列表。
  - trans_c：翻译c指令
  - main：功能整合，先选择文件，接着调用process函数去除空白与注释，在对符号进行处理，接着翻译两种指令，最后输出翻译后的机器码文件。

  汇编器效果图示：

![61](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/61.png)

在CPU模拟器上运行翻译后的机器码文件，效果与汇编程序一致。

![62](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/62.png)

- 高级语言

  我们已经可以在该模拟计算机上编写简单汇编语言代码并运行，可以以此为基础设计一门高级语言。

  - Jack语言设计：

    - 模仿Java语言，设计一门简单的面向对象编程，且运行在堆栈式虚拟机上的高级语言，取名为Jack，该语言为一种简易的类Java语言。

    - Jack的基本编程单元是类，定义具有如下格式：

      > class name{
      >
      > ​	成员字段(field)和静态变量声明
      >
      > ​	子程序声明
      >
      > }

    - 符号：

      | //   | 单行注释                 |
      | ---- | ------------------------ |
      | /**/ | 多行注释                 |
      | ()   | 封装算术表达式和参数列表 |
      | []   | 数组索引                 |
      | ,    | 变量列表分隔符           |
      | ;    | 语句终止符               |
      | .    | 类成员                   |

    - 保留字

      | class,constructor,method,function | 程序组件 |
      | --------------------------------- | -------- |
      | int,boolean,char,void             | 基本类型 |
      | var,static,field                  | 变量声明 |
      | let,do,if,else,while,return       | 表达式   |
      | true,false,null                   | 常数     |
      | this                              | 对象引用 |

    - 数据类型

      | int     | 16位2补码   |
      | ------- | ----------- |
      | boolean | false或true |
      | char    | Unicode字符 |

  - 构建语法分析器模块

    - 先实现字元化功能，将jack源代码文件输出为xml文件。

      ![101](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/101.png)

    - 语法分析：承接之前工作，输出带有语法分析结构的xml文件

      ![102](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/102.png)

  - 构建代码生成器

    - 语法分析树已完成，通过后缀表示法来生成字节码

    - 内存分配

      | 子程序局部变量 | local虚拟段    |
      | -------------- | -------------- |
      | 子程序参数变量 | argument虚拟段 |
      | 类文件静态变量 | static虚拟段   |
      | 访问类对象     | this虚拟段     |
      | 访问数组对象   | that虚拟段     |

    - 子程序调用

      - 调用函数前，调用者本身将函数的参数压入堆栈，若是类方法，则参数须是该方法操作对象的引用
      - 构造方法或函数时，需要为新对象分配内存段并将this指向该内存段基地址。

  - 经过构建语法分析器和代码生成器两个阶段，成功将Jack语言代码转化为虚拟机字节码vm文件，最终代码与效果如下图所示：

    

    ![111](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/111.png)

    ![112](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/112.png)

  - 构建虚拟机：

    - 我们已经生成了字节码，现构建一个虚拟机程序将字节码转化为汇编代码，再由汇编器编译为机器码在硬件模拟器上运行。

    - 内存管理

      | 段名      | 功能                                 | 说明                                                         |
      | --------- | ------------------------------------ | ------------------------------------------------------------ |
      | argument  | 存储函数的参数                       | 进入函数时为函数参数动态分配内存                             |
      | local     | 存储函数局部变量                     | 进入函数时动态分配内存且初始化为0                            |
      | static    | 存储同一vm文件中所有函数共享静态变量 | 被同一vm文件所有函数共用                                     |
      | constant  | 包含所有常数，范围0~32767            | 对程序中所有程序可见                                         |
      | this/that | 通用段，与堆中不同区域对应           | 任何函数可使用这两段曹总堆中区域                             |
      | pointer   | 由2内存单元组成，保存this/that基地址 | 任何函数可将pointer0/1设置到某一地址上，相当于将this\that段联结到起始于该地址的堆区域 |
      | temp      | 由8个内存单元组成，保存临时变量      | 被任何函数共享                                               |

      此8个虚拟内存段由pop与push命令直接操作

    - 程序流程控制

      | label symbol    | 标签声明                 |
      | --------------- | ------------------------ |
      | goto symbol     | 无条件分支               |
      | if-goto symbol  | 条件分支                 |
      | function 函数名 | 函数声明                 |
      | call 函数名     | 调用函数                 |
      | return          | 将程序控制权返回给调用者 |

    - RAM使用

      - 该模拟计算机有32K个16位字节，分配如下

        | RAM地址     | 功能                              |
        | ----------- | --------------------------------- |
        | 0-15        | 16个虚拟存储器                    |
        | 0           | SP，栈指针，指向栈顶              |
        | 1           | LCL，指向当前函数local段基地址    |
        | 2           | ARG，指向当前函数argument段基地址 |
        | 3           | THIS，指向当前this段在堆中基地址  |
        | 4           | THAT，指向当前that段在堆中基地址  |
        | 5~12        | 保存temp段内容                    |
        | 13~15       | 用作通用寄存器                    |
        | 16~255      | 存储静态变量                      |
        | 256~2047    | 栈                                |
        | 2048~16383  | 堆（存储对象与数组）              |
        | 16384~24575 | 内存映像I/O                       |

    - 分两部分成功构建虚拟机，第一部分成功实现堆栈运算和内存访问，第二部分在此基础实现程序控制功能。

      ![72](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/72.png)

      测试如下，左图为翻译后的汇编，右图为原始vm文件在vm模拟器上运行结果，可见效果一致。

      ![71](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/71.png)

  - 构建OS标准库

    - 高级语言业已完成，若想要方便的在该模拟计算机上用高级语言编程，需要编写一些基本的OS库。

    - | Math     | 提供基本数学运算                     |
      | -------- | ------------------------------------ |
      | String   | 实现字符串String类型和字符串相关操作 |
      | Array    | 实现数组Array类型和数组相关操作      |
      | Output   | 处理屏幕文字输出                     |
      | Screen   | 处理屏幕上图像输出                   |
      | Keyboard | 处理键盘用户输入                     |
      | Memory   | 处理内存操作                         |
      | Sys      | 提供与程序执行相关的服务             |

    - ![121](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/121.png)

- 整体测试
  - 使用高级语言编写一个碰球小游戏，使其被编译为机器码后能运行在硬件模拟器上
  - ![131](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/131.png)


