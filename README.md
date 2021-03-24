
### 从零构造一台模拟计算机

本项目旨在从基础逻辑门开始，一步一步自底向上，经历CPU，汇编，虚拟机，高级语言，操作系统（库函数），构建起整个计算机硬件和软件体系，使其能在模拟器上运行，且配套的高级语言可编写简易游戏运行在该模拟计算机上。

该项目层次如下：

- 基础逻辑门

  使用硬件设计语言(hdl)，以与非门为基础，在硬件模拟器上构建了and dmux mux not or xor等逻辑门。

  ![11](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/11.png)

  在硬件模拟器（HardwareSimulator.bat）上运行代码并测试，图为and门，测试结果正确。

  

  ![12](https://github.com/haomingdouranggouqil/creat-a-simulated-computer/blob/main/pic/12.png)

- 算术逻辑单元（ALU）

  使用基础逻辑门，实现了半加器，全加器，加法器，增量器，最后组装成ALU。![21](\pic\21.png)

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
