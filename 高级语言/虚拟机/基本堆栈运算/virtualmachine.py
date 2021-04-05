import os
index0 = 0
symbols = []
def process(raw):
    #传入原始文本，返回无注释，按行分割的字符串列表，每个列表元素是一条指令。
    nocomment = ''
    flag = 1
    for i in range(len(raw)):
        if raw[i] == '/':
            if raw[i + 1] == '/':
                flag = 0
            elif raw[i + 1] == '*':
                flag = -1
            else:
                pass
        if flag == 1:
            nocomment += raw[i]
        elif flag == 0 and raw[i] == '\n':
            flag = 1
            nocomment += raw[i]
        elif flag == -1 and raw[i - 1] == '*' and raw[i] == '/':
            flag = 1
        else:
            pass
    newstr = ''
    f = 0
    for i in range(len(nocomment)):
        if nocomment[i] != '\n':
            f = 1

        if f == 1:
            if nocomment[i - 1] == '\n' and nocomment[i] == '\n':
                pass
            else:
                newstr += nocomment[i]
        else:
            pass
    linelist = newstr.split("\n")
    linelist.pop()
    return linelist

def commandType(com):
    com_list = com.split()
    if com_list[0] == 'push':
        return 'push'
    elif com_list[0] == 'pop':
        return 'pop'
    elif com_list[0] == 'goto':
        return 'goto'
    elif com_list[0] == 'if-goto':
        return 'if'
    elif com_list[0] == 'return':
        return 'return'
    elif com_list[0] == 'function':
        return 'function'
    elif com_list[0] == 'call':
        return 'call'
    else:
        return 'arith'

def arg1(command, type):
    if type == 'arith':
        return command
    else:
        com_list = command.split()
        return com_list[1]

def arg2(command, type):
    if type == 'push' or type == 'pop' or type == 'function' or type == 'call':
        com_list = command.split()
        return com_list[-1]

def createJudgementString(judge, index):
    #先将两个数相减 再根据给出条件 大于 等于 小于 来处理
    #因为判断大小需要用到跳转 所以得随机产生两个不同的symbol作标签
    str1 = ('@SP\r\n'
    + 'AM=M-1\r\n'
    + 'D=M\r\n'
    + 'A=A-1\r\n'
    + 'D=M-D\r\n'
    + '@TRUE' + str(index) + '\r\n' #如果符合条件判断 则跳转到symbol1标记的地址
    + 'D;' + str(judge) + '\r\n' #否则接着往下处理
    + '@SP\r\n'
    + 'AM=M-1\r\n'
    + 'M=0\r\n'
    + '@SP\r\n'
    + 'M=M+1\r\n'
    + '@CONTINUE' + str(index) + '\r\n'
    + '0;JMP\r\n'
    + '(TRUE' + str(index) + ')\r\n'
    + '@SP\r\n'
    + 'AM=M-1\r\n'
    + 'M=-1\r\n'
    + '@SP\r\n'
    + 'M=M+1\r\n'
    + '(CONTINUE' + str(index) + ')\r\n')
    return str1

def writeArithmetic(command):
    global index0
    output = ''
    output1 = ('@SP\r\n'
    + 'AM=M-1\r\n'
    + 'D=M\r\n'
    + 'A=A-1\r\n')

    output2 = ('@SP\r\n'
    + 'AM=M-1\r\n')

    output3 = ('@SP\r\n'
    + 'M=M+1\r\n')

    if command == 'add':
        output = output1 + 'M=M+D\r\n'
    elif command == 'sub':
        output = output1 + 'M=M-D\r\n'
    elif command == 'neg':
        output = output2 + 'M=-M\r\n' + output3
    elif command == 'eq':
        output = createJudgementString('JEQ', index0)
        index0 += 1
    elif command == 'gt':
        output = createJudgementString('JGT', index0)
        index0 += 1
    elif command == 'lt':
        output = createJudgementString('JLT', index0)
        index0 += 1
    elif command == 'and':
        output = output1 + 'M=M&D\r\n'
    elif command == 'or':
        output = output1 + 'M=M|D\r\n'
    elif command == 'not':
        output = output2 + 'M=!M\r\n' + output3
    else:
        pass
    return output

def popTemplate(str, v2, flag):
    if(flag):
        str1 = 'D=M\r\n'
    else:
        str1 = 'D=A\r\n'
    output = (str + str1
    + '@' + v2 + '\r\n'
    + 'D=D+A\r\n'
    + '@R13\r\n'
    + 'M=D\r\n'
    + '@SP\r\n'
    + 'AM=M-1\r\n'
    + 'D=M\r\n'
    + '@R13\r\n'
    + 'A=M\r\n'
    + 'M=D\r\n')
    return output

def pushTemplate(str, v2, flag):
    if flag:
        str1 = 'D=M\r\n'
    else:
        str1 = 'D=A\r\n'
    output = (str + str1
    + '@' + v2 + '\r\n'
    + 'A=D+A\r\n'
    + 'D=M\r\n'
    + '@SP\r\n'
    + 'A=M\r\n'
    + 'M=D\r\n'
    + '@SP\r\n'
    + 'M=M+1\r\n')
    return output

def change(a):
    s = str(a)
    return s

def processSegment(v1, v2, type, fileName):
    output = ''
    if v1 == 'CONSTANT':
        s2 = change(v2)
        output = ('@' + s2 + '\r\n'
        + 'D=A\r\n'
        + '@SP\r\n'
        + 'A=M\r\n'
        + 'M=D\r\n'
        + '@SP\r\n'
        + 'M=M+1\r\n')
    elif v1 == 'STATIC':
        if type == 'push':
            s2 = change(v2)
            output = ('@' + fileName + '.' + s2 + '\r\n'
            + 'D=M\r\n'
            + '@SP\r\n'
            + 'A=M\r\n'
            + 'M=D\r\n'
            + '@SP\r\n'
            + 'M=M+1\r\n')
        else:
            s2 = change(v2)
            output = ('@SP\r\n'
            + 'AM=M-1\r\n'
            + 'D=M\r\n'
            + '@' + fileName + '.' + s2 + '\r\n'
            + 'M=D\r\n')
    elif v1 == 'POINTER':
        if v2 == 0:
            v1 = 'THIS'
        elif v2 == 1:
            v1 = 'THAT'
        else:
            pass
        if type == 'push':
            output = ('@' + v1 + '\r\n'
            + 'D=M\r\n'
            + '@SP\r\n'
            + 'A=M\r\n'
            + 'M=D\r\n'
            + '@SP\r\n'
            + 'M=M+1\r\n')
        else:
            output = ('@' + v1 + '\r\n'
            + 'D=A\r\n'
            + '@R13\r\n'
            + 'M=D\r\n'
            + '@SP\r\n'
            + 'AM=M-1\r\n'
            + 'D=M\r\n'
            + '@R13\r\n'
            + 'A=M\r\n'
            + 'M=D\r\n')
    elif v1 == 'TEMP':
        if type == 'push':
            output = pushTemplate('@R5\r\n', v2, False)
        else:
            output = popTemplate('@R5\r\n', v2, False)
    else:
        str = ''
        if v1 == 'LOCAL':
            str = '@LCL\r\n'
        elif v1 == 'ARGUMENT':
            str = '@ARG\r\n'
        else:
            str = '@' + v1 + '\r\n'
        if type == 'push':
            output = pushTemplate(str, v2, True)
        else:
            output = popTemplate(str, v2, True)
    return output

def writePushPop(command, type, fileName):
    v1 = arg1(command, type).upper()
    v2 = arg2(command, type)
    return processSegment(v1, v2, type, fileName)

def writeLabel(command):
    com_list = command.split()
    label = com_list[-1]
    output = '(' + label + ')\r\n'
    return output

def writeGoto(command):
    com_list = command.split()
    label = com_list[-1]
    output = '@' + label + '\r\n' + '0;JMP\r\n'
    return output

def writeIf(command):
    com_list = command.split()
    label = com_list[-1]
    output = ('@SP\r\n'
            + 'AM=M-1\r\n'
            + 'D=M\r\n'
            + '@' + label + '\r\n'
            + 'D;JNE\r\n')
    return output

callIndex = -1
callArry = ['LCL', 'ARG', 'THIS', 'THAT']

def writeCall(command, type):
    global callIndex
    callIndex  += 1
    funcName = arg1(command, type).upper()
    argumentNum = arg2(command, type)
    output = ('@' + funcName + 'RETURN_ADDRESS' + str(callIndex) + '\r\n'
            + 'D=A\r\n'
            + '@SP\r\n'
            + 'A=M\r\n'
            + 'M=D\r\n'
            + '@SP\r\n'
            + 'M=M+1\r\n')

    for i in callArry:
        output += ('@' + i + '\r\n'
                + 'D=M\r\n'
                + '@SP\r\n'
                + 'A=M\r\n'
                + 'M=D\r\n'
                + '@SP\r\n'
                + 'M=M+1\r\n')

    output += ('@' + str(argumentNum) + '\r\n'
            + 'D=A\r\n'
            + '@5\r\n'
            + 'D=D+A\r\n'
            + '@SP\r\n'
            + 'D=M-D\r\n'
            + '@ARG\r\n'
            + 'M=D\r\n'
            + '@SP\r\n'
            + 'D=M\r\n'
            + '@LCL\r\n'
            + 'M=D\r\n'
            + '@' + funcName + '\r\n'
            + '0;JMP\r\n'
            + '(' + funcName + 'RETURN_ADDRESS' + str(callIndex) + ')\r\n')
    return output

pointerArry = ['THAT', 'THIS', 'ARG', 'LCL']

def writeReturn(command):
    str1 = ''
    for i in pointerArry:
        str1 +=('@R13\r\n'
            + 'D=M-1\r\n'
            + 'AM=D\r\n'
            + 'D=M\r\n'
            + '@' + i + '\r\n'
            + 'M=D\r\n')
    output = ('@LCL\r\n'
            + 'D=M\r\n'
            + '@R13\r\n'
            + 'M=D\r\n'
            + '@5\r\n'
            + 'A=D-A\r\n'
            + 'D=M\r\n'
            + '@R14\r\n' #保存返回地址
            + 'M=D\r\n'
            + '@SP\r\n'
            + 'AM=M-1\r\n'
            + 'D=M\r\n'
            + '@ARG\r\n'
            + 'A=M\r\n'
            + 'M=D\r\n'
            + '@ARG\r\n'
            + 'D=M+1\r\n'
            + '@SP\r\n'
            + 'M=D\r\n'
            + str1
            + '@R14\r\n'
            + 'A=M\r\n'
            + '0;JMP\r\n')
    return output


def writeFunction(command, type, filename):
    funcName = arg1(command, type).upper()
    localNum = int(arg2(command, type))
    output = '(' + funcName + ')\r\n'
    while (localNum > 0):
        output += writePushPop('push constant 0', 'push', filename)
        localNum -= 1
    return output

def createJudgementString(judge, index):
    #先将两个数相减 再根据给出条件 大于 等于 小于 来处理
    #因为判断大小需要用到跳转 所以得随机产生两个不同的symbol作标签
    str1 = ('@SP\r\n'
        + 'AM=M-1\r\n'
        + 'D=M\r\n'
        + 'A=A-1\r\n'
        + 'D=M-D\r\n'
        + '@TRUE' + str(index) + '\r\n' #如果符合条件判断 则跳转到symbol1标记的地址
        + 'D;' + judge + '\r\n' #否则接着往下处理
        + '@SP\r\n'
        + 'A=M-1\r\n'
        + 'M=0\r\n'
        + '@CONTINUE' + str(index) +  '\r\n'
        + '0;JMP\r\n'
        + '(TRUE' + str(index) + ')\r\n'
        + '@SP\r\n'
        + 'A=M-1\r\n'
        + 'M=-1\r\n'
        + '(CONTINUE' + str(index) + ')\r\n')
    return str1

def writeInit():
    output = ('@256\r\n'
            + 'D=A\r\n'
            + '@SP\r\n'
            + 'M=D\r\n')
    output += writeCall('call Sys.init 0', 'call')
    return output

def advance(command, fileName):
    output = ''
    type = commandType(command)
    if type == 'push' or type == 'pop':
        output = writePushPop(command, type, fileName)
    elif type == 'arith':
        output = writeArithmetic(command)
    elif type == 'label':
        output = writeLabel(command, type, fileName)
    elif type == 'goto':
        output = writeGoto(command)
    elif type == 'if':
        output = writeIf(command)
    elif type == 'return':
        output = writeReturn(command)
    elif type == 'function':
        output = writeFunction(command, type, fileName)
    elif type == 'call':
        output = writeCall(command, type)
    else:
        output = writeArithmetic(command)
    return output

def parser(commands, fileName):
    output = ''
    for command in commands:
        output += advance(command, fileName)
    return output

if __name__ == '__main__':
    path = 'BasicLoop'
    if path[-3:] == '.vm':
        #单个文件
        fopen = open(path)
        raw = fopen.read()
        fopen.close()
        asm = parser(process(raw), path)
        fw = open(path[:-3] + '.asm', 'w')
        fw.write(asm)
        fw.close()
    else:
        #文件夹
        Filelist = []
        asm = ''
        for home, dirs, files in os.walk(path):
            for filename in files:
                Filelist.append(os.path.join(path, filename))
                #Filelist.append( filename)
        for i in Filelist:
            filename = i.split('\\')[-1]
            if i[-3:] == '.vm':
                fopen = open(i)
                raw = fopen.read()
                fopen.close()
                if i[-6:] == 'Sys.vm':
                    asm += writeInit()
                else:
                    asm += parser(process(raw), filename)
        fw = open(path + '.asm', 'w')
        fw.write(asm)
        fw.close()
