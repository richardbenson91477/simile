''' enums '''

DATA_NONE, DATA_LONG, DATA_LARRAY, DATA_STR =\
    range (4)

VAL_NONE, VAL_VAR, VAL_VAR_DEREF, VAL_LONG, VAL_LARRAY, VAL_STR =\
    range (6)

EMIT_NONE, EMIT_DEF, EMIT_RET, EMIT_END, EMIT_CALL, EMIT_PUSH,\
        EMIT_IF, EMIT_ELSE, EMIT_ENDIF, EMIT_WHILE, EMIT_WEND,\
        EMIT_ADD, EMIT_SUB, EMIT_MUL, EMIT_DIV,\
        EMIT_RES, EMIT_SET,\
        EMIT_ADDTO, EMIT_SUBFROM, EMIT_MULTO, EMIT_DIVFROM\
            = range (21)

FLOW_NONE, FLOW_IF, FLOW_WHILE =\
    range (3)

