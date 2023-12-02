code = '''PROGRAM -> FUNC PROGRAM
PROGRAM -> ''
FUNC -> TYPE id parentesis_izquierdo ARGS parentesis_derecho inicio_bloque STMTS fin_bloque
TYPE -> int
TYPE -> float
TYPE -> char
TYPE -> void
ARGS -> TYPE id MORE_ARGS 
ARGS -> ''
MORE_ARGS -> coma TYPE id MORE_ARGS
MORE_ARGS -> ''
STMTS -> STMT STMTS 
STMTS -> ''
STMT -> id STMT_PRIME
STMT -> DECL
STMT -> CONTROL
STMT -> RETURN STMT_END
STMT_PRIME -> asignacion EXPR STMT_END 
STMT_PRIME -> parentesis_izquierdo ARGS_LIST parentesis_derecho STMT_END
STMT_PRIME -> INC_DEC 
INC_DEC -> aumentar
INC_DEC -> reducir
DECL -> TYPE id INIT STMT_END
INIT -> asignacion EXPR
INIT -> ''
ARRAY_INIT -> asignacion inicio_bloque EXPR_LIST fin_bloque
ARRAY_INIT -> ''
EXPR_LIST -> EXPR MORE_EXPRS
EXPR_LIST -> ''
MORE_EXPRS -> coma EXPR MORE_EXPRS
MORE_EXPRS -> ''
ARGS_LIST -> EXPR MORE_ARGS
ARGS_LIST -> ''
CONTROL -> IF_STMT
CONTROL -> FOR_STMT
CONTROL -> WHILE_STMT
CONTROL -> DO_WHILE_STMT
IF_STMT -> if parentesis_izquierdo COND_EXPR parentesis_derecho inicio_bloque STMTS fin_bloque ELSE_PART
ELSE_PART -> else inicio_bloque STMTS fin_bloque
ELSE_PART -> ''
FOR_STMT -> for parentesis_izquierdo DECL COND_EXPR STMT_END STMT parentesis_derecho inicio_bloque STMTS fin_bloque
WHILE_STMT -> while parentesis_izquierdo COND_EXPR parentesis_derecho inicio_bloque STMTS fin_bloque
DO_WHILE_STMT -> do inicio_bloque STMTS fin_bloque while parentesis_izquierdo COND_EXPR parentesis_derecho STMT_END

COND_EXPR -> EXPR REL_OP EXPR
RETURN -> return EXPR
EXPR -> TERM EXPR_PRIME
EXPR_PRIME -> suma TERM EXPR_PRIME
EXPR_PRIME -> ''
TERM -> FACTOR TERM_PRIME
TERM_PRIME -> multiplicacion FACTOR TERM_PRIME
TERM_PRIME -> ''
FACTOR -> CONST_INT
FACTOR -> CONST_FLOAT
FACTOR -> CONST_CHAR
FACTOR -> id
FACTOR -> parentesis_izquierdo EXPR parentesis_derecho
STMT_END -> fin_instruccion

REL_OP -> menor_que
REL_OP -> mayor_que
REL_OP -> igual
REL_OP -> diferente


STMT -> PRINTF_STMT
STMT -> SCANF_STMT
PRINTF_STMT -> printf parentesis_izquierdo const_string coma ARGS_LIST parentesis_derecho STMT_END
SCANF_STMT -> scanf parentesis_izquierdo const_string coma SCANF_ARGS parentesis_derecho STMT_END
SCANF_ARGS -> ampersand id MORE_SCANF_ARGS
MORE_SCANF_ARGS -> coma ampersand id MORE_SCANF_ARGS
MORE_SCANF_ARGS -> ''

'''


PROGRAM = 0
FUNC = 1
TYPE = 2
ARGS = 3
MORE_ARGS = 4
STMTS = 5
STMT = 6
DECL = 7
INIT = 8
ARRAY_INIT = 9
EXPR_LIST = 10
MORE_EXPRS = 11
ARGS_LIST = 12
CONTROL = 13
IF_STMT = 14
ELSE_PART = 15
FOR_STMT = 16
WHILE_STMT = 17
DO_WHILE_STMT = 18
COND_EXPR = 19
RETURN = 20
EXPR = 21
EXPR_PRIME = 22
TERM = 23
TERM_PRIME = 24 
FACTOR = 25
STMT_END = 26
REL_OP = 27
STMT_PRIME = 28
INC_DEC = 29
MORE_ARGS_LIST = 30
PRINTF_STMT = 31
SCANF_STMT = 32
SCANF_ARGS = 33
MORE_SCANF_ARGS = 34


tabla = [
    [PROGRAM, "int" ,   [FUNC, PROGRAM]],
    [PROGRAM, "float" , [FUNC, PROGRAM]],
    [PROGRAM, "char" ,  [FUNC, PROGRAM]],
    [PROGRAM, "void" ,  [FUNC, PROGRAM]],
    [PROGRAM, 'eof',    ['vacia']],

    [INC_DEC, "aumentar", ["aumentar"]],
    [INC_DEC, "reducir", ["reducir"]],
    

    [FUNC, "int",   [TYPE, "id", 'parentesis_izquierdo', ARGS, "parentesis_derecho", "inicio_bloque", STMTS, "fin_bloque" ]],
    [FUNC, "float", [TYPE, "id", 'parentesis_izquierdo', ARGS, "parentesis_derecho", "inicio_bloque", STMTS, "fin_bloque" ]],
    [FUNC, "char",  [TYPE, "id", 'parentesis_izquierdo', ARGS, "parentesis_derecho", "inicio_bloque", STMTS, "fin_bloque" ]],
    [FUNC, "void",  [TYPE, "id", 'parentesis_izquierdo', ARGS, "parentesis_derecho", "inicio_bloque", STMTS, "fin_bloque" ]],

    [TYPE, "int",   ["int"]],	
    [TYPE, "float", ["float"]],
    [TYPE, "char",  ["char"]],
    [TYPE, "void",  ["void"]],

    [ARGS, "parentesis_derecho", ['vacia']],
    [ARGS, "int",   [TYPE, "id", MORE_ARGS]],
    [ARGS, "float", [TYPE, "id", MORE_ARGS]],
    [ARGS, "char",  [TYPE, "id", MORE_ARGS]],
    [ARGS, "void",  [TYPE, "id", MORE_ARGS]],

    [MORE_ARGS, "coma", ["coma", TYPE, "id", MORE_ARGS]],
    [MORE_ARGS, "parentesis_derecho", ['vacia']],

    [STMTS, "fin_bloque", ['vacia']],
    [STMTS, "int", [STMT, STMTS]],
    [STMTS, "id", [STMT, STMTS]],
    [STMTS, "float", [STMT, STMTS]],
    [STMTS, "char", [STMT, STMTS]],
    [STMTS, "void", [STMT, STMTS]],
    [STMTS, "return", [STMT, STMTS]],
    [STMTS, "if", [STMT, STMTS]],
    [STMTS, "for", [STMT, STMTS]],
    [STMTS, "while", [STMT, STMTS]],
    [STMTS, "do", [STMT, STMTS]],
    [STMTS, "printf", [STMT, STMTS]],
    [STMTS, "scanf", [STMT, STMTS]],

    [STMT, "int", [DECL]],
    [STMT, "id", ["id", STMT_PRIME]],
    [STMT, "float", [DECL]],
    [STMT, "char", [DECL]],
    [STMT, "void", [DECL]],
    [STMT, "if", [CONTROL]],
    [STMT, "for", [CONTROL]],
    [STMT, "while", [CONTROL]],
    [STMT, "do", [CONTROL]],
    [STMT, "return", [RETURN, STMT_END]],
    [STMT, "printf", [PRINTF_STMT]],
    [STMT, "scanf", [SCANF_STMT]],


    [STMT_PRIME, "asignacion", ["asignacion", EXPR, STMT_END]],
    [STMT_PRIME, "parentesis_izquierdo", ["parentesis_izquierdo", ARGS_LIST, "parentesis_derecho", STMT_END]],
    [STMT_PRIME, "aumentar", [INC_DEC]],
    [STMT_PRIME, "reducir", [INC_DEC]],
    [STMT_PRIME, "fin_instruccion", [STMT_END]],
    
    [PRINTF_STMT, "printf", ["printf", "parentesis_izquierdo", "const_string", "coma", ARGS_LIST, "parentesis_derecho", STMT_END]],
    [SCANF_STMT, "scanf", ["scanf", "parentesis_izquierdo", "const_string", "coma", SCANF_ARGS, "parentesis_derecho", STMT_END]],

    [SCANF_ARGS, "ampersand", ["ampersand", "id", MORE_SCANF_ARGS]],

    [MORE_SCANF_ARGS, "coma", ["coma", "ampersand", "id", MORE_SCANF_ARGS]],
    [MORE_SCANF_ARGS, "parentesis_derecho", ['vacia']],

    [DECL, "int", [TYPE, "id", INIT, STMT_END]],
    [DECL, "float", [TYPE, "id", INIT, STMT_END]],
    [DECL, "char", [TYPE, "id", INIT, STMT_END]],
    [DECL, "void", [TYPE, "id", INIT, STMT_END]],

    [INIT, "asignacion", ["asignacion", EXPR]],
    [INIT, "fin_instruccion", ['vacia']],

    [ARRAY_INIT, "asignacion", ["asignacion", "inicio_bloque", EXPR_LIST, "fin_bloque"]],
    [ARRAY_INIT, "fin_instruccion", ['vacia']],

    [EXPR_LIST, "id", [EXPR, MORE_EXPRS]],
    [EXPR_LIST, "parentesis_izquierdo", [EXPR, MORE_EXPRS]],
    [EXPR_LIST, "const_int", [EXPR, MORE_EXPRS]],
    [EXPR_LIST, "const_float", [EXPR, MORE_EXPRS]],
    [EXPR_LIST, "const_char", [EXPR, MORE_EXPRS]],
    [EXPR_LIST, "fin_bloque", ['vacia']],

    [MORE_EXPRS, "coma", ["coma", EXPR, MORE_EXPRS]],
    [MORE_EXPRS, "fin_bloque", ['vacia']],

    [ARGS_LIST, "id", [EXPR, MORE_ARGS_LIST]],
    [ARGS_LIST, "parentesis_izquierdo", [EXPR, MORE_ARGS]],
    [ARGS_LIST, "const_int", [EXPR, MORE_ARGS]],
    [ARGS_LIST, "const_float", [EXPR, MORE_ARGS]],
    [ARGS_LIST, "const_char", [EXPR, MORE_ARGS]],
    [ARGS_LIST, "parentesis_derecho", ['vacia']],

    [MORE_ARGS_LIST, "coma", ["coma", EXPR, MORE_ARGS_LIST]],
    [MORE_ARGS_LIST, "parentesis_derecho", ['vacia']],

    [CONTROL, "if", [IF_STMT]],
    [CONTROL, "for", [FOR_STMT]],
    [CONTROL, "while", [WHILE_STMT]],
    [CONTROL, "do", [DO_WHILE_STMT]],

    [IF_STMT, "if", ["if", "parentesis_izquierdo", COND_EXPR, "parentesis_derecho", "inicio_bloque", STMTS, "fin_bloque", ELSE_PART]],

    [ELSE_PART, "else", ["else", "inicio_bloque", STMTS, "fin_bloque"]],
    [ELSE_PART, "int", ['vacia']],
    [ELSE_PART, "fin_bloque", ['vacia']],
    [ELSE_PART, "id", ['vacia']],
    [ELSE_PART, "float", ['vacia']],
    [ELSE_PART, "char", ['vacia']],
    [ELSE_PART, "void", ['vacia']],
    [ELSE_PART, "return", ['vacia']],
    [ELSE_PART, "if", ['vacia']],
    [ELSE_PART, "for", ['vacia']],
    [ELSE_PART, "while", ['vacia']],
    [ELSE_PART, "do", ['vacia']],
    [ELSE_PART, "printf", ['vacia']],
    [ELSE_PART, "scanf", ['vacia']],

    [FOR_STMT, "for", ["for", "parentesis_izquierdo", DECL, COND_EXPR, STMT_END, STMT, "parentesis_derecho", "inicio_bloque", STMTS, "fin_bloque"]],

    [WHILE_STMT, "while", ["while", "parentesis_izquierdo", COND_EXPR, "parentesis_derecho", "inicio_bloque", STMTS, "fin_bloque"]],

    [DO_WHILE_STMT, "do", ["do", "inicio_bloque", STMTS, "fin_bloque", "while", "parentesis_izquierdo", COND_EXPR, "parentesis_derecho", STMT_END]],

    [COND_EXPR, "id", [EXPR, REL_OP, EXPR]],
    [COND_EXPR, "parentesis_izquierdo", [EXPR, REL_OP, EXPR]],
    [COND_EXPR, "const_int", [EXPR, REL_OP, EXPR]],
    [COND_EXPR, "const_float", [EXPR, REL_OP, EXPR]],
    [COND_EXPR, "const_char", [EXPR, REL_OP, EXPR]],

    [RETURN, "return", ["return", EXPR]],

    [EXPR, "id", [TERM, EXPR_PRIME]],
    [EXPR, "parentesis_izquierdo", [TERM, EXPR_PRIME]],
    [EXPR, "const_int", [TERM, EXPR_PRIME]],
    [EXPR, "const_float", [TERM, EXPR_PRIME]],
    [EXPR, "const_char", [TERM, EXPR_PRIME]],

    [EXPR_PRIME, "suma", ["suma", TERM, EXPR_PRIME]],
    [EXPR_PRIME, "parentesis_derecho", ['vacia']],
    [EXPR_PRIME, "fin_bloque", ['vacia']],
    [EXPR_PRIME, "asignacion", ['vacia']],
    [EXPR_PRIME, "fin_instruccion", ['vacia']],
    [EXPR_PRIME, "coma", ['vacia']],
    [EXPR_PRIME, "parentesis_izquierdo", ['vacia']],
    [EXPR_PRIME, "parentesis_derecho", ['vacia']],
    [EXPR_PRIME, "menor_que", ['vacia']],
    [EXPR_PRIME, "mayor_que", ['vacia']],
    [EXPR_PRIME, "igual", ['vacia']],
    [EXPR_PRIME, "diferente", ['vacia']],

    [TERM, "id", [FACTOR, TERM_PRIME]],
    [TERM, "parentesis_izquierdo", [FACTOR, TERM_PRIME]],
    [TERM, "const_int", [FACTOR, TERM_PRIME]],
    [TERM, "const_float", [FACTOR, TERM_PRIME]],
    [TERM, "const_char", [FACTOR, TERM_PRIME]],

    [TERM_PRIME, "multiplicacion", ["multiplicacion", FACTOR, TERM_PRIME]],
    [TERM_PRIME, "parentesis_derecho", ['vacia']],
    [TERM_PRIME, "fin_bloque", ['vacia']],
    [TERM_PRIME, "coma", ['vacia']],
    [TERM_PRIME, "suma", ['vacia']],
    [TERM_PRIME, "fin_instruccion", ['vacia']],
    [TERM_PRIME, "menor_que", ['vacia']],
    [TERM_PRIME, "mayor_que", ['vacia']],
    [TERM_PRIME, "igual", ['vacia']],
    [TERM_PRIME, "diferente", ['vacia']],

    [FACTOR, "id", ["id"]],
    [FACTOR, "parentesis_izquierdo", ["parentesis_izquierdo", EXPR, "parentesis_derecho"]],
    [FACTOR, "const_int", ["const_int"]],
    [FACTOR, "const_float", ["const_float"]],
    [FACTOR, "const_char", ["const_char"]],

    [STMT_END, "fin_instruccion", ["fin_instruccion"]],

    [REL_OP, "menor_que", ["menor_que"]],
    [REL_OP, "mayor_que", ["mayor_que"]],
    [REL_OP, "igual", ["igual"]],
    [REL_OP, "diferente", ["diferente"]]
]
