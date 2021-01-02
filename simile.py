#!/usr/bin/env python3
''' simile compiler ''' 
''' by Richard A. Benson <richardbenson91477@gmail.com> '''
import sys, os
import emit, out, util, fn, enums as e

class s:
    ''' state '''
    pass

def init (t, long_len = 8):
    if t:
        s.line_n = 0
        s.fn_cur = None
        if not emit.init (long_len):
            return False
    else:
        pass

    return True

def main ():
    if len (sys.argv) > 1:
        res_ = init (True, int(sys.argv [1]))
    else:
        res_ = init (True)
    if not res_:
        out.error ('init failed')
        return -1

    lines = sys.stdin.readlines ()
    res_ = process (lines)
    if not res_:
        out.error ('process (pass 1) failed at line ' + str(s.line_n + 1))
        return -2
    init (False)

    out.s.output_ = True
    if len (sys.argv) > 1:
        res_ = init (True, int(sys.argv [1]))
    else:
        res_ = init (True)
    res_ = process (lines)
    if not res_:
        out.error ('process (pass 2) failed at line ' + str(s.line_n + 1))
        return -3
    init (False)

    return 0

def process (ls):
    cmdd = {
        'def': (1, 0, do_def),
        'ret': (0, 0, do_ret),
        'end': (0, 0, do_end),
        'call': (1, 0, do_call),
        'if': (1, 1, do_if),
        'else': (0, 0, do_else),
        'endif': (0, 0, do_endif),
        'while': (1, 1, do_while),
        'wend': (0, 0, do_wend),
        'add': (1, 1, do_add),
        'sub': (1, 1, do_sub),
        'mul': (1, 1, do_mul),
        'div': (1, 1, do_div),
        'res': (1, 1, do_res),
        'set': (2, 2, do_set),
        'addto': (2, 2, do_addto),
        'subfrom': (2, 2, do_subfrom),
        'multo': (2, 2, do_multo),
        'divfrom': (2, 2, do_divfrom)
    }

    for s.line_n, s_raw in enumerate(ls):
        if not s_raw:
            continue

        # strip beginning and ending whitespaces
        s_stp = s_raw.strip ()
        if not s_stp:
            continue

        # split at unquoted spaces 
        s_spl = util.q_split (s_stp)
        keyword1 = s_spl [0]
        args = s_spl [1:]
        args_n = len (args)

        # ignore
        if keyword1[0] == '#':
            continue
        else:
            try:
                _c = cmdd [keyword1]
            except:
                out.error ('"' + keyword1 + '" keyword unknown')
                return False

            if args_n < _c [0]:
                out.arg_n_error (keyword1, _c [0], _c [1])
                return False

            elif _c [1] and args_n > _c [1]:
                out.arg_n_error (keyword1, _c [0], _c [1])
                return False

            if (not s.fn_cur) and keyword1 != 'def':
                out.error ('outside function')
                return False

            res_ = _c [2](args)
            if not res_:
                return False

    return True

def do_def (args):
    if s.fn_cur:
        out.error ('nested function')
        return False

    _fn = fn.Fn (args [0], args [1:], emit.s.long_len)
    if not _fn:
        return False

    s.fn_cur = _fn

    res_ = emit.emit (s.fn_cur, e.EMIT_DEF, args [0])
    return res_

def do_ret (args):
    if not s.fn_cur.flow_n:
        s.fn_cur.flow_ret_t = True
    if len(args):
        res_ = emit.emit (s.fn_cur, e.EMIT_RET, args [0])
    else:
        res_ = emit.emit (s.fn_cur, e.EMIT_RET, None)
    return res_

def do_end (args):
    if s.fn_cur.flow_n:
        out.error ('unclosed flow control')
        return False

    res_ = emit.emit (s.fn_cur, e.EMIT_END, '')
    s.fn_cur = None
    return res_

def do_call (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_CALL, args [0], val2=args [1:])
    return res_

def do_if (args):
    s.fn_cur.flow_cur += [[e.FLOW_IF, s.fn_cur.flow_if_n]]
    s.fn_cur.flow_if_n += 1
    s.fn_cur.flow_n += 1
    res_ = emit.emit (s.fn_cur, e.EMIT_IF, args [0])
    return res_

def do_else (args):
    if (not s.fn_cur.flow_n) or\
            (s.fn_cur.flow_cur [s.fn_cur.flow_n - 1][0] != e.FLOW_IF):
        out.error ('outside flow control')
        return False

    res_ = emit.emit (s.fn_cur, e.EMIT_ELSE, None)
    return res_

def do_endif (args):
    if (not s.fn_cur.flow_n) or\
            (s.fn_cur.flow_cur [s.fn_cur.flow_n - 1][0] != e.FLOW_IF):
        out.error ('outside flow control')
        return False

    res_ = emit.emit (s.fn_cur, e.EMIT_ENDIF, None)

    s.fn_cur.flow_cur.pop ()
    s.fn_cur.flow_n -= 1
    return res_

def do_while (args):
    s.fn_cur.flow_cur += [[e.FLOW_WHILE, s.fn_cur.flow_while_n]]
    s.fn_cur.flow_while_n += 1
    s.fn_cur.flow_n += 1
    res_ = emit.emit (s.fn_cur, e.EMIT_WHILE, args [0])
    return res_

def do_wend (args):
    if (not s.fn_cur.flow_n) or\
            (s.fn_cur.flow_cur [s.fn_cur.flow_n - 1][0] != e.FLOW_WHILE):
        out.error ('outside flow control')
        return False

    res_ = emit.emit (s.fn_cur, e.EMIT_WEND, None)

    s.fn_cur.flow_cur.pop ()
    s.fn_cur.flow_n -= 1
    return res_

def do_add (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_ADD, args [0]);
    return res_

def do_sub (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_SUB, args [0]);
    return res_

def do_mul (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_MUL, args [0]);
    return res_

def do_div (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_DIV, args [0]);
    return res_

def do_res (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_RES, args [0]);
    return res_

def do_set (args): 
    res_ = emit.emit (s.fn_cur, e.EMIT_SET, args [0], val2 = args [1])
    return res_

def do_addto (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_ADDTO, args [0], val2 = args [1])
    return res_

def do_subfrom (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_SUBFROM, args [0], val2 = args [1])
    return res_

def do_multo (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_MULTO, args [0], val2 = args [1])
    return res_

def do_divfrom (args):
    res_ = emit.emit (s.fn_cur, e.EMIT_DIVFROM, args [0], val2 = args [1])
    return res_

if __name__ == '__main__':
    sys.exit (main())

