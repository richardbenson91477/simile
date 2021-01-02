''' output '''
import sys

class s:
    ''' state '''
    indent_sp = 4
    output_ = False

def put (code, i_n = 1):
    if s.output_:
        sys.stdout.write (' ' * i_n * s.indent_sp + code + '\n')

def error (_s):
    sys.stderr.write ('error: ' + _s + '\n')

def arg_n_error (_s, _min, _max):
    error ('"' + _s + '" expects from ' + str(_min) + ' to ' + str(_max) + \
        ' arguments')

