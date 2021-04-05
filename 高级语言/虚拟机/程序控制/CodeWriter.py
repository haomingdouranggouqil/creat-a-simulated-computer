import os, os.path
from VMConstant import *

class CodeWriter(object):
    def __init__(self, outf):
        self._out_file = open(outf, 'w')
        self._vm_file = ''
        self._labelnum = 0

    def __str__(self):
        pass

    def set_file_name(self, filename):
        self._vm_file, ext = os.path.splitext(filename)

    def close_file(self):
        self._out_file.close()

    def write_init(self):
        self._a_command('256')
        self._c_command('D', 'A')
        self._comp_to_reg(R_SP, 'D')
        self.write_call('Sys.init', 0)

    def write_arithmetic(self, command):
        if   command == 'add':  self._binary('D+A')
        elif command == 'sub':  self._binary('A-D')
        elif command == 'neg':  self._unary('-D')
        elif command == 'eq':   self._compare('JEQ')
        elif command == 'gt':   self._compare('JGT')
        elif command == 'lt':   self._compare('JLT')
        elif command == 'and':  self._binary('D&A')
        elif command == 'or':   self._binary('D|A')
        elif command == 'not':  self._unary('!D')

    def write_push_pop(self, command, seg, index):
        if command == C_PUSH:   self._push(seg, index)
        elif command == C_POP:  self._pop(seg, index)

    def write_label(self, label):
        self._l_command(label)

    def write_goto(self, label):
        self._a_command(label)
        self._c_command(None, '0', 'JMP')

    def write_if(self, label):
        self._pop_to_dest('D')
        self._a_command(label)
        self._c_command(None, 'D', 'JNE')

    def write_call(self, function_name, num_args):
        return_address = self._new_label()
        self._push(S_CONST, return_address)
        self._push(S_REG, R_LCL)
        self._push(S_REG, R_ARG)
        self._push(S_REG, R_THIS)
        self._push(S_REG, R_THAT)
        self._load_sp_offset(-num_args-5)
        self._comp_to_reg(R_ARG, 'D')
        self._reg_to_reg(R_LCL, R_SP)
        self._a_command(function_name)
        self._c_command(None, '0', 'JMP')
        self._l_command(return_address)

    def write_return(self):
        self._reg_to_reg(R_FRAME, R_LCL)
        self._a_command('5')
        self._c_command('A', 'D-A')
        self._c_command('D', 'M')
        self._comp_to_reg(R_RET, 'D')
        self._pop(S_ARG, 0)
        self._reg_to_dest('D', R_ARG)
        self._comp_to_reg(R_SP, 'D+1')
        self._prev_frame_to_reg(R_THAT)
        self._prev_frame_to_reg(R_THIS)
        self._prev_frame_to_reg(R_ARG)
        self._prev_frame_to_reg(R_LCL)
        self._reg_to_dest('A', R_RET)
        self._c_command(None, '0', 'JMP')

    def _prev_frame_to_reg(self, reg):
        self._reg_to_dest('D', R_FRAME)
        self._c_command('D', 'D-1')
        self._comp_to_reg(R_FRAME, 'D')
        self._c_command('A', 'D')
        self._c_command('D', 'M')
        self._comp_to_reg(reg, 'D')

    def write_function(self, function_name, num_locals):
        self._l_command(function_name)
        for i in range(num_locals):
            self._push(S_CONST, 0)

    def _push(self, seg, index):
        if   self._is_const_seg(seg):   self._val_to_stack(str(index))
        elif self._is_mem_seg(seg):     self._mem_to_stack(self._asm_mem_seg(seg), index)
        elif self._is_reg_seg(seg):     self._reg_to_stack(seg, index)
        elif self._is_static_seg(seg):  self._static_to_stack(seg, index)
        self._inc_sp()

    def _pop(self, seg, index):
        self._dec_sp()
        if   self._is_mem_seg(seg):     self._stack_to_mem(self._asm_mem_seg(seg), index)
        elif self._is_reg_seg(seg):     self._stack_to_reg(seg, index)
        elif self._is_static_seg(seg):  self._stack_to_static(seg, index)

    def _pop_to_dest(self, dest):
        self._dec_sp()
        self._stack_to_dest(dest)

    def _is_mem_seg(self, seg):
        return seg in [S_LCL, S_ARG, S_THIS, S_THAT]

    def _is_reg_seg(self, seg):
        return seg in [S_REG, S_PTR, S_TEMP]

    def _is_static_seg(self, seg):
        return seg == S_STATIC

    def _is_const_seg(self, seg):
        return seg == S_CONST


    def _unary(self, comp):
        self._dec_sp()
        self._stack_to_dest('D')
        self._c_command('D', comp)
        self._comp_to_stack('D')
        self._inc_sp()
    def _binary(self, comp):
        self._dec_sp()
        self._stack_to_dest('D')
        self._dec_sp()
        self._stack_to_dest('A')
        self._c_command('D', comp)
        self._comp_to_stack('D')
        self._inc_sp()

    def _compare(self, jump):
        self._dec_sp()
        self._stack_to_dest('D')
        self._dec_sp()
        self._stack_to_dest('A')
        self._c_command('D', 'A-D')
        label_eq = self._jump('D', jump)
        self._comp_to_stack('0')
        label_ne = self._jump('0', 'JMP')
        self._l_command(label_eq)
        self._comp_to_stack('-1')
        self._l_command(label_ne)
        self._inc_sp()                    

    def _inc_sp(self):
        self._a_command('SP')
        self._c_command('M', 'M+1')

    def _dec_sp(self):
        self._a_command('SP')
        self._c_command('M', 'M-1')

    def _load_sp(self):
        self._a_command('SP')
        self._c_command('A', 'M')

    def _val_to_stack(self, val):
        self._a_command(val)
        self._c_command('D', 'A')
        self._comp_to_stack('D')

    def _reg_to_stack(self, seg, index):
        self._reg_to_dest('D', self._reg_num(seg, index))
        self._comp_to_stack('D')

    def _mem_to_stack(self, seg, index, indir=True):
        self._load_seg(seg, index, indir)
        self._c_command('D', 'M')
        self._comp_to_stack('D')

    def _static_to_stack(self, seg, index):
        self._a_command(self._static_name(index))
        self._c_command('D', 'M')
        self._comp_to_stack('D')

    def _comp_to_stack(self, comp):
        self._load_sp()
        self._c_command('M', comp)

    def _stack_to_reg(self, seg, index):
        self._stack_to_dest('D')
        self._comp_to_reg(self._reg_num(seg, index), 'D')

    def _stack_to_mem(self, seg, index, indir=True):
        self._load_seg(seg, index, indir)
        self._comp_to_reg(R_COPY, 'D')
        self._stack_to_dest('D')
        self._reg_to_dest('A', R_COPY)
        self._c_command('M', 'D')

    def _stack_to_static(self, seg, index):
        self._stack_to_dest('D')
        self._a_command(self._static_name(index))
        self._c_command('M', 'D')

    def _stack_to_dest(self, dest):
        self._load_sp()
        self._c_command(dest, 'M')

    def _load_sp_offset(self, offset):
        self._load_seg(self._asm_reg(R_SP), offset)

    def _load_seg(self, seg, index, indir=True):
        if index == 0:
            self._load_seg_no_index(seg, indir)
        else:
            self._load_seg_index(seg, index, indir)

    def _load_seg_no_index(self, seg, indir):
        self._a_command(seg)
        if indir: self._indir(dest='AD')

    def _load_seg_index(self, seg, index, indir):
        comp = 'D+A'
        if index < 0:
            index = -index
            comp = 'A-D'
        self._a_command(str(index))
        self._c_command('D', 'A')
        self._a_command(seg)
        if indir: self._indir()
        self._c_command('AD', comp)

    # Register ops
    def _reg_to_dest(self, dest, reg):
        self._a_command(self._asm_reg(reg))
        self._c_command(dest, 'M')

    def _comp_to_reg(self, reg, comp):
        self._a_command(self._asm_reg(reg))
        self._c_command('M', comp)

    def _reg_to_reg(self, dest, src):
        self._reg_to_dest('D', src)
        self._comp_to_reg(dest, 'D')

    def _indir(self, dest='A'):
        self._c_command(dest, 'M')

    def _reg_num(self, seg, index):
        return self._reg_base(seg)+index

    def _reg_base(self, seg):
        reg_base = {'reg':R_R0, 'pointer':R_PTR, 'temp':R_TEMP}
        return reg_base[seg]

    def _static_name(self, index):
        return self._vm_file+'.'+str(index)

    def _asm_mem_seg(self, seg):
        asm_label = {S_LCL:'LCL', S_ARG:'ARG', S_THIS:'THIS', S_THAT:'THAT'}
        return asm_label[seg]

    def _asm_reg(self, regnum):
        return 'R'+str(regnum)

    def _jump(self, comp, jump):
        label = self._new_label()
        self._a_command(label)
        self._c_command(None, comp, jump)
        return label

    # Generate a new label
    def _new_label(self):
        self._labelnum += 1
        return 'LABEL'+str(self._labelnum)

    # Write an assembler @ command
    def _a_command(self, address):
        self._out_file.write('@'+address+'\n')

    # Write an assembler C command
    def _c_command(self, dest, comp, jump=None):
        if dest != None:
            self._out_file.write(dest+'=')
        self._out_file.write(comp)
        if jump != None:
            self._out_file.write(';'+jump)
        self._out_file.write('\n')

    # Write an assembler L command
    def _l_command(self, label):
        self._out_file.write('('+label+')\n')
