''' functions and data '''
import out, enums as e

class Data:
    def __init__ (self, name_s, _type, val, long_len):
        self.name_s = name_s
        self._type = _type
        self.val = val

        if _type == e.DATA_LONG:
            self._len = long_len

        elif _type == e.DATA_LARRAY:
            self._len = long_len * int(val.strip ('[]'))

        elif _type == e.DATA_STR:
            self._len = len(val)

class Var:
    def __init__ (self, name_s, datum):
        self.name_s = name_s
        self.datum = datum

class Fn:
    def __init__ (self, name_s, args, long_len):
        self.name_s = name_s
        self.args = args
        self.data = []
        self.data_n = 0
        self.data_larray_n = 0
        self.data_str_n = 0
        self._vars = []
        self.long_len = long_len
        self.flow_if_n = 0
        self.flow_while_n = 0
        self.flow_ret_t = False
        self.flow_n = 0
        self.flow_cur = []

    def def_data (self, name_s, _type, val):
        _n = self.name_s + '.' + name_s
        datum = Data (_n, _type, val, self.long_len)
        self.data += [datum]
        self.data_n += 1
        if _type == e.DATA_LARRAY:
            self.data_larray_n += 1
        elif _type == e.DATA_STR:
            self.data_str_n += 1
        return datum

    def get_arg (self, name_s):
        try:
            return self.args.index (name_s) + 1
        except:
            return 0

    def get_or_def_var (self, name_s):
        if self.get_arg (name_s):
            out.error ('name "' + name_s + '" taken by function argument')
            return None

        for var in self._vars:
            if var.name_s == name_s:
                return var

        datum = self.def_data (name_s, e.DATA_LONG, [])
        var = Var (name_s, datum)

        self._vars += [var]
        return var

