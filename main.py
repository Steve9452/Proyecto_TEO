from collections import defaultdict

import ply.lex as lex

from lexer import *
from symbols import symbols
from newTable2 import tabla, getNonTerminalName


class parentNode:
    def __init__(self, node, toNonTerminal=None):
        self.node = node
        self.fromNonTerminal = toNonTerminal


def miParser(ats=[]):
    f = open("fuente.c", "r")
    file = f.read() + "\n$"
    lexer.input(file)

    error = False
    tok = lexer.token()
    x = stack[-1]
    prevDataType = None

    raiz = NodoDerivacion("Raíz")

    
    context_stack = []
    # context_stack.append(ats)
    # print("Contexto inicial: ", context_stack[-1].type)
    while True:
        # if stack[-1] == 1:
        #     print(">>>>>>>>>>>>Pila: ", stack, "\n", "Entrada:\n\tTipo:", tok.type,"Valor:", tok.value)
        # else:
        #     print("Pila: ", stack, "\n", "Entrada:\n\tTipo:", tok.type,"Valor:", tok.value)
        print("Pila: ",x,  getNonTerminalName(x),  "\n")

        stmt = getNonTerminalName(x)
        if stmt ==  "STMT" or stmt == "FUNC" or stmt == "FOR_STMT" or stmt == "WHILE_STMT" or stmt == "STMTS" or stmt == "DECL":
            print("=================Creacion de contexto==============================")

            print("Contexto Abierto New  node:   ",getNonTerminalName(x))
            try:
                print("con padre", context_stack[-1].type)
            except IndexError:
                print("con padre: ", "None")
            context_stack.append(NewNode(getNonTerminalName(x), value=getNonTerminalName(x)))
            current_node = context_stack[-1]
            
        elif x ==  'fin_instruccion' or (x == 'fin_bloque' and context_stack[-1].type == "WHILE_STMT") :
            print("===================Enlace de nodos============================")
            
            if context_stack[-1].type == "WHILE_STMT" and x == 'fin_bloque' :
                print_ast(current_node)
                print("---------------")
                print("Contexto Cerrado:   ", context_stack[-2].type, current_node.type)
                context_stack[-2].children.append(current_node)
                print_ast(context_stack[-2])
                
                print("---------------")
                current_node = context_stack.pop()
                print(len(context_stack))
                
                print("---------------")
                context_stack[-2].children.append(current_node)
                print_ast(context_stack[-2])
                context_stack.pop()
                current_node = context_stack[-1]

            elif context_stack[-1].type == "DECL":
                print(context_stack[-2].type,"<--", current_node.type)
                context_stack[-2].children.append(current_node)
                context_stack.pop()
                current_node = context_stack.pop()
                print_ast(current_node)
                print_ast(context_stack[-1])
                context_stack[-1].children.append(current_node)
                print_ast(context_stack[-1])
                print(len(context_stack))
                current_node = context_stack[-1]

            else:
                print(context_stack[-2].type,"<--", current_node.type)
                # print_ast(context_stack[-2])
                
                context_stack[-2].children.append(current_node)
                # ats.children.append( context_stack.pop())
                
                context_stack.pop()
                current_node = context_stack[-1]
                print_ast(context_stack[-1])
                print(len(context_stack))
        flag = True
        if x == tok.type and x == "eof":
            
            ats.children.append(context_stack[0])
            # print(context_stack[0].type)
            if error:
                print("\t[ El proceso ha finalizado con errores ]")
            else:
                print("\t[ Fin del proceso ]")
            return raiz

        
        # if getNonTerminalName(x) != None:
        #     print("No terminal :", getNonTerminalName(x))
        
        if x == tok.type and x != "eof":
            # print("=============================================================")
            
            # print(current_node.type)
            auxNextToken = lexer.token()

            # Almacena el tipo de dato de la variable auxiliar por si en la siguiente interacion es requerida.
            if tok.type == "int" or tok.type == "float" or tok.type == "char":
                prevDataType = tok.type


            # Var assignment.
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






            # print("Agregando a la pila el nodo: ", current_node.type, " con valor: ", tok.value)
            context_stack[-1].children.append(NewNode(tok.type, leaf=tok.value))
            # if tok.type == "id" or tok.type == "int" or tok.type == "float" or tok.type == "char":
            #     current_node.children.append(NewNode(tok.type, leaf=tok.value))
            


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

            
            lexer.skip(0)
            tok = lexer.token()
            stack.pop()
            try:
                x = stack[-1]
            except IndexError:
                print("Error en línea: {}".format(tok.lineno))
                return
            error = True
            flag=False

        if x not in tokens and flag:  # es no terminal
            
            celda = buscar_en_tabla(x, tok.type)
            if celda is None:
                if tok.type != "error":

                    print("\nERROR en línea: ", tok.lineno, ", NO SE ESPERABA token de tipo ", tok.type,
                            "  se esperaba  ", x, "  en", tok.value, "\n")


                lexer.skip(0)
                tok = lexer.token()
                stack.pop()

                x = stack[-1]
                


 

            else:              
                # print("Simbolo no terminal ")
                # print("Pila: ", stack, "\n", "Entrada:\n\tTipo:", tok.type,"Valor:", tok.value)
                if getNonTerminalName(x) != None and False:
                    # print("No terminal :", getNonTerminalName(x))
                    if getNonTerminalName(x) == "FUNC" or getNonTerminalName(x) == "DECL" or getNonTerminalName(x) == "STMTS":
                        print("Agregando a la pila el nodo: ", current_node.type, " con valor: ", getNonTerminalName(x))
                        # print("Ultimo elemento del stack es : ", stack , "and : ", x)
                        current_node.children.append(NewNode(getNonTerminalName(x), value=getNonTerminalName(x)))

                        context_stack.append(current_node)
                        print("Nodo agregado a contexto",current_node.type,"context actual",context_stack[-1].type, "Con longitud: ", len(context_stack))
                        current_node = current_node.children[-1]
                        print("===============================================")

                if getNonTerminalName(x) == "STMTS" or getNonTerminalName(x) == "STMT"  :
                    print(">>>>>>>>>>>>>>>>>>>>",getNonTerminalName(x))

                    
                stack.pop()
                agregar_pila(celda)
                x = stack[-1]            
                # print("x::", getNonTerminalName(x))
                # print(stack)
                # print("Celda::", celda)
                        # current_node = context_stack.pop()

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

class NodoDerivacion:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)




class NewNode:
    def __init__(self, type, children=None, value=None, leaf=None):
        self.type = type
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf


class UnexpectedTokenError(Exception):
    pass



def print_ast(node, indent=""):
    print(f"{indent}{node.type}:", end="")
    if node.leaf:
        print(f"leaf: {node.leaf}")
    else:
        print()
    for child in node.children:
        print_ast(child, indent + "  ")

def imprimir_arbol(nodo, space = ""):
    
    print(f"{space}{nodo.tipo}: {nodo.valor} : {getNonTerminalName(nodo.valor)} Hijos: {len(nodo.hijos)}")
    for hijo in nodo.hijos:
        imprimir_arbol(hijo, space + " ")


def main():
    ats = NewNode("Raiz")

    arbol_derivacion = miParser(ats)
    # imprimir_tabla_simbolos()
    # imprimir_tabla_resumen()
    # imprimir_arbol(arbol_derivacion)
    print("AST: =======================================================")
    print_ast(ats)


if __name__ == "__main__":
    main()


