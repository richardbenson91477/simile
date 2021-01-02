''' code emitters '''
import out, enums as e

class s:
    ''' state '''
    # long_len
    # arg_regs, arg_regs_n
    # regs
    # stack_regs
    pass

def init (long_len):
    s.long_len = long_len
    if long_len == 8:
        s.arg_regs = ['%rdi', '%rsi', '%rdx', '%rcx', 'r8', 'r9']
        s.arg_regs_n = len(s.arg_regs)
        s.regs = ['%rax', '%rbx', '%r10']
        s.stack_regs = ['%rsp', '%rbp']

    elif long_len == 4:
        s.arg_regs = []
        s.arg_regs_n = 0
        s.regs = ['%eax', '%ebx', '%ecx']
        s.stack_regs = ['%esp', '%ebp']

    else:
        out.error ('what year is this???')
        return False

    return True

def emit (fn_cur, et, val, val2 = None):
    if et == e.EMIT_DEF:
        out.put ('.section .text', i_n = 0)
        out.put ('.globl ' + val, i_n = 0)
        out.put (val + ':', i_n = 0)
        out.put ('push ' + s.stack_regs [1])
        out.put ('mov ' + s.stack_regs [0] + ', ' + s.stack_regs [1])
        out.put ('xor ' + s.regs [0] + ', ' + s.regs [0])

    elif et == e.EMIT_RET:
        if val:
            if not get_val (fn_cur, val, s.regs [0]):
                return False
        out.put ('pop ' + s.stack_regs [0])
        out.put ('ret')

    elif et == e.EMIT_END:
        if not fn_cur.flow_ret_t:
            out.put ('pop ' + s.stack_regs [1])
            out.put ('ret')

        if fn_cur.data_n:
            out.put ('.section .data', i_n = 0)
        for datum in fn_cur.data:
            if datum._type == e.DATA_LONG:
                out.put (datum.name_s + ': .zero ' + str(datum._len), i_n = 0)
            elif datum._type == e.DATA_LARRAY:
                out.put (datum.name_s + ': .zero ' + str(datum._len), i_n = 0)
            elif datum._type == e.DATA_STR:
                out.put (datum.name_s + ': .string ' + datum.val, i_n = 0)

    elif et == e.EMIT_CALL:
        arg_n = len (val2)
        for arg_i, arg in enumerate (val2):
            if arg_i < s.arg_regs_n:
                if not get_val (fn_cur, arg, s.arg_regs [arg_i]):
                    return False
            else:
                if not get_val (fn_cur, arg, s.regs [0]):
                    return False
                out.put ('push ' + s.regs [0])
        out.put ('call ' + val)
        if arg_n > s.arg_regs_n:
            out.put ('add $' + str((arg_n - s.arg_regs_n) * s.long_len) +\
                ', ' + s.stack_regs [0])

    elif et == e.EMIT_PUSH:
        if not get_val (fn_cur, val, s.regs [0]):
            return False
        out.put ('push ' + s.regs [0])

    elif et == e.EMIT_IF:
        if not get_val (fn_cur, val, s.regs [0]):
            return False
        out.put ('test ' + s.regs [0] + ', ' + s.regs [0])
        out.put ('jz ' + fn_cur.name_s + '.else.' +\
            str(fn_cur.flow_cur [fn_cur.flow_n - 1][1]))

    elif et == e.EMIT_ELSE:
        out.put ('jmp ' + fn_cur.name_s + '.endif.' +\
            str(fn_cur.flow_cur [fn_cur.flow_n - 1][1]))
        out.put (fn_cur.name_s + '.else.' +\
            str(fn_cur.flow_cur [fn_cur.flow_n - 1][1]) + ':', i_n = 0)

    elif et == e.EMIT_ENDIF:
        out.put (fn_cur.name_s + '.endif.' +\
            str(fn_cur.flow_cur [fn_cur.flow_n - 1][1]) + ':', i_n = 0)

    elif et == e.EMIT_WHILE:
        out.put (fn_cur.name_s + '.while.' +\
            str(fn_cur.flow_cur [fn_cur.flow_n - 1][1]) + ':', i_n = 0)
        if not get_val (fn_cur, val, s.regs [0]):
            return False
        out.put ('test ' + s.regs [0] + ', ' + s.regs [0])
        out.put ('jz ' + fn_cur.name_s + '.wend.' +\
            str(fn_cur.flow_cur [fn_cur.flow_n - 1][1]))

    elif et == e.EMIT_WEND:
        out.put ('jmp ' + fn_cur.name_s + '.while.' +\
            str(fn_cur.flow_cur [fn_cur.flow_n - 1][1]))
        out.put (fn_cur.name_s + '.wend.' +\
            str(fn_cur.flow_cur [fn_cur.flow_n - 1][1]) + ':', i_n = 0)

    elif et == e.EMIT_ADD:
        if not get_val (fn_cur, val, s.regs [1]):
            return False
        out.put ('add ' + s.regs [1] + ', ' + s.regs [0])

    elif et == e.EMIT_SUB:
        if not get_val (fn_cur, val, s.regs [1]):
            return False
        out.put ('sub ' + s.regs [1] + ', ' + s.regs [0])

    elif et == e.EMIT_MUL:
        if not get_val (fn_cur, val, s.regs [1]):
            return False
        out.put ('imul ' + s.regs [1] + ', ' + s.regs [0])

    elif et == e.EMIT_DIV:
        if not get_val (fn_cur, val, s.regs [1]):
            return False
        out.put ('cltd')
        out.put ('idiv ' + s.regs [1])

    elif et == e.EMIT_RES:
        if not set_val (fn_cur, val):
            return False

    elif et == e.EMIT_SET:
        if not get_val (fn_cur, val2, s.regs [0]):
            return False

        if not set_val (fn_cur, val):
            return False

    elif et == e.EMIT_ADDTO:
        if not get_val (fn_cur, val2, s.regs [1]):
            return False
        if not get_val (fn_cur, val, s.regs [0]):
            return False
        out.put ('add ' + s.regs [1] + ', ' + s.regs [0])
        if not set_val (fn_cur, val):
            return False

    elif et == e.EMIT_SUBFROM:
        if not get_val (fn_cur, val2, s.regs [1]):
            return False
        if not get_val (fn_cur, val, s.regs [0]):
            return False
        out.put ('sub ' + s.regs [1] + ', ' + s.regs [0])
        if not set_val (fn_cur, val):
            return False

    elif et == e.EMIT_MULTO:
        if not get_val (fn_cur, val2, s.regs [1]):
            return False
        if not get_val (fn_cur, val, s.regs [0]):
            return False
        out.put ('imul ' + s.regs [1] + ', ' + s.regs [0])
        if not set_val (fn_cur, val):
            return False

    elif et == e.EMIT_DIVFROM:
        if not get_val (fn_cur, val2, s.regs [1]):
            return False
        if not get_val (fn_cur, val, s.regs [0]):
            return False
        out.put ('cltd')
        out.put ('idiv ' + s.regs [1])
        if not set_val (fn_cur, val):
            return False

    else:
        out.put ('uknown emit type')
        return False

    return True

def get_val (fn_cur, val, reg):
    val_type = get_val_type (val)
    if not val_type:
        out.error ('unknown val type "' + val + '"')
        return False

    elif val_type == e.VAL_LARRAY:
        datum = fn_cur.def_data ('.l' + str(fn_cur.data_larray_n),\
            e.DATA_LARRAY, val)
        out.put ('mov ' + '$' + datum.name_s + ', ' + reg)

    elif val_type == e.VAL_STR:
        datum = fn_cur.def_data ('.s' + str(fn_cur.data_str_n),\
            e.DATA_STR, val)
        out.put ('mov ' + '$' + datum.name_s + ', ' + reg)

    elif val_type == e.VAL_LONG:
        out.put ('mov $' + val + ', ' + reg)

    elif val_type == e.VAL_VAR:
        arg_i = fn_cur.get_arg (val)
        if arg_i:
            arg_i -= 1
            if arg_i < s.arg_regs_n:
                _s = s.arg_regs [arg_i]
            else:
                _s = str((arg_i + 1) * s.long_len) + '(' + s.stack_regs [1] +\
                    ')'
            out.put ('mov ' + _s + ', ' + reg)
        else:
            var = fn_cur.get_or_def_var (val)
            if not var:
                return False
            out.put ('mov ' + var.datum.name_s + ', ' + reg)

    elif val_type == e.VAL_VAR_DEREF:
        _n = val [1:]
        arg_i = fn_cur.get_arg (_n)
        if arg_i:
            # TODO support this
            out.error ('dereferencing arg')
            return False
        else:
            var = fn_cur.get_or_def_var (_n)
            if not var:
                return False
        out.put ('mov ' + var.datum.name_s + ', ' + reg)
        out.put ('mov (' + reg + '), ' + reg)

    return True

def set_val (fn_cur, val):
    reg0 = s.regs [0]
    reg2 = s.regs [2]

    val_type = get_val_type (val)
    if \
            val_type == e.VAL_STR or\
            val_type == e.VAL_LARRAY or\
            val_type == e.VAL_LONG:
        out.error ('can\'t assign to this type')
        return False

    elif val_type == e.VAL_VAR:
        arg_i = fn_cur.get_arg (val)
        if arg_i:
            arg_i -= 1
            if arg_i < s.arg_regs_n:
                _s = s.arg_regs [arg_i]
            else:
                _s = str((arg_i + 1) * s.long_len) + '(' + s.stack_regs [1] +\
                    ')'
            out.put ('mov ' + reg0 + ', ' + _s)
        else:
            var = fn_cur.get_or_def_var (val)
            if not var:
                return False
            out.put ('mov ' + reg0 + ', ' + var.datum.name_s)

    elif val_type == e.VAL_VAR_DEREF:
        _n = val [1:]
        arg_i = fn_cur.get_arg (_n)
        if arg_i:
            out.error ('can\'t modify function arg')
            return False
        else:
            var = fn_cur.get_or_def_var (_n)
            if not var:
                return False
        out.put ('mov ' + var.datum.name_s + ', ' + reg2)
        out.put ('mov ' + reg0 + ', (' + reg2 + ')')

    return True

def get_val_type (_s):
    if not _s:
        return e.VAL_NONE

    elif _s [0] == '-' or _s.isdigit () or _s [0] == "'":
        return e.VAL_LONG

    elif _s [0] == '[':
        return e.VAL_LARRAY

    elif _s [0] == '"':
        return e.VAL_STR

    elif _s [0] == '@':
        return e.VAL_VAR_DEREF

    else:
        return e.VAL_VAR

