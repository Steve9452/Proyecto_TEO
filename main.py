from collections import defaultdict

import ply.lex as lex

from lexer import *
from symbols import symbols
from newTable2 import tabla


def miParser():
    f = open("fuente.c", "r")
    file = f.read() + "\n$"
    lexer.input(file)

    error = False
    tok = lexer.token()
    x = stack[-1]
    prevDataType = None
    while True:
        # print("Pila: ", stack)
        if x == tok.type and x == "eof":
            if error:
                print("\t[ El proceso ha finalizado con errores ]")
            else:
                print("\t[ Fin del proceso ]")
            return
        else:
            if x == tok.type and x != "eof":
                auxNextToken = lexer.token()
                if tok.type == "int" or tok.type == "float" or tok.type == "char":
                    prevDataType = tok.type

                if (tok.type == "id") and auxNextToken.type == "asignacion":
                    # print("---------id-----------")
                    # print(stack[-1])
                    # print("Linea: ", tok.lineno)
                    # print("Actual", tok.value)
                    # print("Tipo:", tok.type)
                    # print("Siguiente:" , auxNextToken.type, auxNextToken.value, auxNextToken.lineno, auxNextToken.lexpos)
                    lexerClonado = lexer.clone()
                    auxNext2Token = lexerClonado.token()

                    insertar_o_actualizar_simbolo(
                        prevDataType,
                        tok.value,
                        auxNext2Token.value,
                        tok.lineno,
                        tok.lexpos,
                    )

                stack.pop()
                x = stack[-1]
                tok = auxNextToken

            if x in tokens and x != tok.type:
                # print("Error Pila: ", stack, stack[-1])
                print(
                    "ERROR en línea: ",
                    tok.lineno,
                    " se esperaba ",
                    symbols[x],
                    "en la posicion: ",
                    tok.lexpos,
                    "  en  '",
                    tok.value,
                    "'\n",
                )

              
                # current_line = file[tok.lexpos :]
                # split_token = current_line[len(tok.value):]
                # corrected_input = getSymbol[x] + split_token
                
                # print("==========================")
                # print(corrected_input)
                # print("==========================")

                
                # # tok = lexer.token()
                # lexer.input(corrected_input)
                # tok = lexer.token()

                # print("=====================================================")
                # print("Siguiente token: ", tok.type, tok.value, tok.lineno, tok.lexpos)
                lexer.skip(0)
                tok = lexer.token()
                # print("Siguiente token: ", tok.type, tok.value, tok.lineno, tok.lexpos)
                stack.pop()
                # print("Pila: ", stack)
                x = stack[-1]
                # print("=====================================================")
                error = True

            if x not in tokens :  # es no terminal
                celda = buscar_en_tabla(x, tok.type)
                if celda is None:
                    if tok.type != "error":
                        print(
                            "ERROR en línea: ",
                            tok.lineno,
                            ", NO SE ESPERABA token de tipo ",
                            symbols[tok.type],
                            "\n",
                        )
                        print("\nERROR en línea: ", tok.lineno, ", NO SE ESPERABA token de tipo ", tok.type,
                              "  se esperaba  ", x, "  en", tok.value, "\n")
                    return
                else:
                    stack.pop()
                    agregar_pila(celda)
                    x = stack[-1]


def buscar_en_tabla(no_terminal, terminal):
    for i in range(len(tabla)):
        if tabla[i][0] == no_terminal and tabla[i][1] == terminal:
            return tabla[i][2]  # retorno la celda


def agregar_pila(produccion):
    for elemento in reversed(produccion):
        
        if elemento != "vacia":  # la vacía no la inserta
            stack.append(elemento)


def encontrar_token_esperado(no_terminal):
    for i in range(len(tabla)):
        if tabla[i][0] == no_terminal:
            return tabla[i][1]  # retorno la celda


def getNewToken():
    tok = lexer.token()
    return tok


# consultar proximo token sin consumirlo
def peek():
    tok = lexer.token()
    return tok


tabla_simbolos = defaultdict(list)


def insertar_simbolo(tipo, nombre, valor, linea, columna):
    tabla_simbolos[nombre].append([tipo, valor, linea, columna])


def insertar_o_actualizar_simbolo(tipo, nombre, valor, linea, columna):
    if nombre in tabla_simbolos:
        actualizar_simbolo(nombre, valor)
    else:
        insertar_simbolo(tipo, nombre, valor, linea, columna)


def buscar_simbolo(nombre):
    return tabla_simbolos[nombre]


def actualizar_simbolo(nombre, valor):
    tabla_simbolos[nombre][0][1] = valor


def eliminar_simbolo(nombre):
    tabla_simbolos.pop(nombre)


def imprimir_tabla_simbolos():
    for key in tabla_simbolos:
        print("--------------------------------------------------")
        print("Nombre: ", key)
        print("Tipo: ", tabla_simbolos[key][0][0])
        print("Valor: ", tabla_simbolos[key][0][1])
        print("Linea: ", tabla_simbolos[key][0][2])
        print("Columna: ", tabla_simbolos[key][0][3], "\n\n")

def imprimir_tabla_resumen():
    print("----------------------------------------------------------------------------------")
    print("| {:20} | {:10} | {:15} | {:10} | {:10} |".format("Nombre", "Tipo", "Valor", "Linea", "Columna"))
    for key in tabla_simbolos:
        nombre, tipo, valor, linea, columna = key, *tabla_simbolos[key][0]
        print("| {:20} | {:10} | {:15} | {:10} | {:10} |".format(nombre, tipo, valor, linea, columna))
    print("----------------------------------------------------------------------------------")




def main():
    miParser()
    # imprimir_tabla_simbolos()
    imprimir_tabla_resumen()


if __name__ == "__main__":
    main()

