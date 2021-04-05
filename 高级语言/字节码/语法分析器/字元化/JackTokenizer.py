def process(raw):
    #传入原始文本，返回无空白无注释，按行分割的字符串列表，每个列表元素是一条指令。
    nospace = ''
    for i in raw:
        if i == '\t':
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

def split1(seq_list):
    split_list1 = []
    for i in seq_list:
        if '"' in i:
            l = i.find('"')
            r = i.rfind('"')
            split_list1 += i[:l].split()
            split_list1.append('0'+i[l+1:r])#判字符串
            split_list1 += i[r+1:].split()
        else:
            split_list1 += i.split()
    return split_list1

sym = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
'boolean','void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

def split2(split_list1):
    split_list2 =[]
    for i in split_list1:
        tem = []
        t=0
        for j in range(len(i)):
            if i[j] in sym:
                tem.append(i[t:j])
                tem.append(i[j])
                t=j+1
        tem.append(i[t:])
        split_list2+=tem

    end =[]
    for i in split_list2:
        if len(i) == 0:
            pass
        else:
            end.append(i)
    return end

def returntype(com):
    if com in sym:
        return 'symbol'
    elif com in keyword:
        return 'keyword'
    elif com.isdigit():
        return 'integer'
    elif com[0] == '0':
        return 'string'
    else:
        return 'identifier'

def xml_make(seq_list):
    out = ['<tokens>']
    for i in seq_list:
        if returntype(i) == 'symbol':
            if i == '<':
                xmlseq = '<symbol> '+ '&lt;' +' </symbol>'
            elif i == '>':
                xmlseq = '<symbol> '+ '&gt;' +' </symbol>'
            elif i == '&':
                xmlseq = '<symbol> '+ '&amp;' +' </symbol>'
            else:
                xmlseq = '<symbol> '+ i +' </symbol>'
        elif returntype(i) == 'keyword':
            xmlseq = '<keyword> '+ i +' </keyword>'
        elif returntype(i) == 'integer':
            xmlseq = '<integerConstant> '+ i +' </integerConstant>'
        elif returntype(i) == 'string':
            xmlseq = '<stringConstant> '+ i[1:] +' </stringConstant>'
        else:
            xmlseq = '<identifier> '+ i +' </identifier>'
        out.append(xmlseq)
    out.append('</tokens>')
    return out

def xml_add(xml):
    pass

if __name__ == '__main__':
    path = 'Main.jack'
    fopen = open(path)
    raw = fopen.read()
    fopen.close()
    xmlout = xml_make(split2(split1(process(raw))))
    print(xmlout)
    '''
    pathout = 'fakem.xml'
    fw = open(pathout, 'w')
    for i in xmlout:
        fw.write(i)
        fw.write('\n')
    fw.close()
    '''
