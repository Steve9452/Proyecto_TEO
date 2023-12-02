import ply.lex as lex

# List of token names. Required
tokens = [
    "parentesis_izquierdo",
    "parentesis_derecho",
    "inicio_bloque",
    "fin_bloque",
    "corchete_izquierdo",
    "corchete_derecho",
    "const_int",
    "const_float",
    "const_char",
    "const_string",
    "aumentar",
    "reducir",
    "suma",
    "resta",
    "multiplicacion",
    "division",
    "mod",
    "and",
    "or",
    "diferente",
    "igual",
    "menor_que",
    "mayor_que",
    "id",
    "coma",
    "fin_instruccion",
    "comentario_linea",
    "comentario_bloque",
    "asignacion",
    "ampersand",
    "eof",
]

palabras_reservadas = {
    "int",
    "void",
    "return",
    "float",
    "char",
    "if",
    "else",
    "do",
    "while",
    "for",
    "break",
    "printf",
    "scanf",
}

palabras_reservadas1 = {
    "int",
    "void",
    "return",
    "float",
    "char",
    "if",
    "else",
    "do",
    "while",
    "for",
    "break",
    "printf",
    "scanf",
}

# Add words reserved to tokens array
tokens += palabras_reservadas

# Regular expression rules for simple tokens
t_suma = r"\+"
t_resta = r"-"
t_multiplicacion = r"\*"
t_division = r"/"
t_mod = r"\%"
t_and = r"\&\&"
t_or = r"\|\|"
t_aumentar = r"\+\+"
t_reducir = r"\-\-"
t_diferente = r"\!\="
t_igual = r"\=\="
t_menor_que = r"\<"
t_mayor_que = r"\>"
t_parentesis_izquierdo = r"\("
t_parentesis_derecho = r"\)"
t_corchete_izquierdo = r"\["
t_corchete_derecho = r"\]"
t_inicio_bloque = r"\{"
t_fin_bloque = r"\}"
t_fin_instruccion = r"\;"
t_asignacion = r"\="
t_coma = r"\,"
t_ampersand = r"\&"
t_eof = r"\$"


# A regular expression rule


def t_const_char(t):
    r"(\')(.*)(\')"
    return t


def t_const_string(t):
    r"(\")(.)*(\")"
    return t


def t_comentario_linea(t):
    r"\/\/.*"
    pass


def t_comentario_bloque(t):
    r"\/\*(.|\n)*\*\/"
    pass


def t_id(t):
    r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|\d|_)*"
    t.type = (
        t.value if t.value in palabras_reservadas else "id"
    )  # Check for reserved words
    return t


def t_const_float(t):
    r"[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)"
    t.value = float(t.value)
    return t


def t_const_int(t):
    r"\d+(\.\d+)?"
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"


# Error handling rule
def t_error(t):
    print("Error. Caracter ilegal:'%s'" % t.value[0])
    t.lexer.skip(1)
    return t


stack = ["eof", 0]

# Build the lexer
lexer = lex.lex()

