import tkinter as tk
import tkinter.filedialog

def gui_path_select():
    #构造选择路径GUI，返回所选择文件的路径
    pathte = []
    def selectPath():
        path_ = tk.filedialog.askopenfilename()
        path.set(path_)
        pathte.append(path_)

    root = tk.Tk()
    path = tk.StringVar()
    ww = 260
    wh = 30
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw-ww) / 2
    y = (sh-wh) / 2
    tk.Label(root,text = "image path:").grid(row = 0, column = 0)
    tk.Entry(root, textvariable = path).grid(row = 0, column = 1)
    tk.Button(root, text = "select", command = selectPath).grid(row = 0, column = 2)
    root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
    root.mainloop()
    return pathte[0]

def process(path):
    #传入路径，返回无空白无注释，按行分割的字符串列表，每个列表元素是一条指令。
    fopen = open(path)
    raw = fopen.read()
    fopen.close()
    nospace = ''
    for i in raw:
        if i == ' ':
            pass
        else:
            nospace += i
    nocomment = ''
    flag = 1
    for i in range(len(nospace)):
        if nospace[i] == '/':
            if nospace[i + 1] == '/':
                flag = 0
            elif nospace[i + 1] == '*':
                flag = -1
            else:
                pass
        if flag == 1:
            nocomment += nospace[i]
        elif flag == 0 and nospace[i] == '\n':
            flag = 1
            nocomment += nospace[i]
        elif flag == -1 and nospace[i - 1] == '*' and nospace[i] == '/':
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


def trans_a(instruct_list):
    #传入指令列表，翻译a指令
    for i in range(len(instruct_list)):
        hack = ''
        if instruct_list[i][0] == '@':
            hack += '0'
            b = '{:015b}'.format(int(instruct_list[i][1:]))
            hack += b
            instruct_list[i] = hack

def parser(ins):
    #传入c指令，将其切分为一个列表
    if '=' in ins:
        l1 = ins.split("=")
        dest = l1[0]
        if ';' in ins:
            l2 = l1[1].split(";")
            comp = l2[0]
            jump = l2[1]
        else:
            comp = l1[1]
            jump = 'null'
    else:
        if ';' in ins:
            l1 = ins.split(";")
            dest = 'null'
            comp = l1[0]
            jump = l1[1]
        else:
            dest = 'null'
            comp = ins
            jump = 'null'
    c = []
    c.append(dest)
    c.append(comp)
    c.append(jump)
    return c

#指令对应机器码
dest_set = {
    'null': '000',
    'M'  : '001',
    'D'  : '010',
    'MD' : '011',
    'A'  : '100',
    'AM' : '101',
    'AD' : '110',
    'AMD': '111'
}

jump_set = {
    'null':'000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

comp_set = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
}

def trans_c(instruct_list):
    #翻译c指令
    for i in range(len(instruct_list)):
        if len(instruct_list[i]) != 16:
            l = parser(instruct_list[i])
            hack = '111'
            hack += comp_set[l[1]]
            hack += dest_set[l[0]]
            hack += jump_set[l[2]]
            instruct_list[i] = hack

#符号集
sym_tab = {
    'SP' : 0,
    'LCL' : 1,
    'ARG' : 2,
    'THIS' : 3,
    'THAT' : 4,
    'SCREEN' : 16384,
    'KBD' : 24576
}

def sym_pro(instruct_list):
    #处理符号
    count = 0
    ad = 16
    dellist = []
    for i in range(len(instruct_list)):
        if instruct_list[i][0] == '(':
            lable = instruct_list[i][1:]
            lable = lable[:-1]
            sym_tab[lable] = count
            dellist.append(i)
        else:
            count += 1

    for i in range(len(instruct_list)):
        if instruct_list[i][0] == '@':
            s = instruct_list[i][1]
            if s.isdigit():
                pass
            else:
                v = instruct_list[i][1:]
                if v in sym_tab.keys():
                    pass
                else:
                    sym_tab[v] = ad
                    ad += 1

    for i in range(len(instruct_list)):
        if instruct_list[i][0] == '@':
            s = instruct_list[i][1]
            if s.isdigit():
                pass
            elif instruct_list[i][1] == 'R':
                s1 = instruct_list[i][2]
                if s1.isdigit():
                    instruct_list[i] = '@' + instruct_list[i][2:]
                else:
                    w = instruct_list[i][1:]
                    instruct_list[i] = '@' + str(sym_tab[w])
            else:
                w = instruct_list[i][1:]
                instruct_list[i] = '@' + str(sym_tab[w])
    delnum = 0
    for i in dellist:
        del instruct_list[i - delnum]
        delnum += 1
    return instruct_list

def main():
    #整合
    path = gui_path_select()
    ins_lis = sym_pro(process(path))
    trans_a(ins_lis)
    trans_c(ins_lis)
    new_path = path[:-3] + 'hack'
    fo = open(new_path, 'w')
    for i in ins_lis:
        fo.write(i)
        fo.write('\n')
    fo.close()

if __name__ == '__main__':
    main()
