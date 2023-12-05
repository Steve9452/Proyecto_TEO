from collections import defaultdict

import ply.lex as lex

from lexer import *
from symbols import symbols
from newTable2 import tabla, getNonTerminalName


string_file = ""

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
    while True:

        # print("Pila: ",x,  getNonTerminalName(x),  "\n")

        stmt = getNonTerminalName(x)
        if stmt ==  "STMT" or stmt == "FUNC" or stmt == "FOR_STMT" or stmt == "WHILE_STMT" or stmt == "STMTS" or stmt == "DECL":
            # print("=================Creacion de contexto==============================")

            # print("Contexto Abierto New  node:   ",getNonTerminalName(x))
            # try:
            #     print("con padre", context_stack[-1].type)
            # except IndexError:
            #     print("con padre: ", "None")
            context_stack.append(NewNode(getNonTerminalName(x), value=getNonTerminalName(x), line=tok.lineno, column=tok.lexpos))
            current_node = context_stack[-1]
            
        elif x ==  'fin_instruccion' or (x == 'fin_bloque' and context_stack[-1].type == "WHILE_STMT") :
            # print("===================Enlace de nodos============================")
            
            if context_stack[-1].type == "WHILE_STMT" and x == 'fin_bloque' :
                # print_ast(current_node)
                # print("---------------")
                # print("Contexto Cerrado:   ", context_stack[-2].type, current_node.type)
                context_stack[-2].children.append(current_node)
                # print_ast(context_stack[-2])
                
                # print("---------------")
                current_node = context_stack.pop()
                # print(len(context_stack))
                
                # print("---------------")
                context_stack[-2].children.append(current_node)
                # print_ast(context_stack[-2])
                context_stack.pop()
                current_node = context_stack[-1]

            elif context_stack[-1].type == "DECL":
                # print(context_stack[-2].type,"<--", current_node.type)
                context_stack[-2].children.append(current_node)
                context_stack.pop()
                current_node = context_stack.pop()
                # print_ast(current_node)
                # print_ast(context_stack[-1])
                context_stack[-1].children.append(current_node)
                # print_ast(context_stack[-1])
                # print(len(context_stack))
                current_node = context_stack[-1]

            else:
                # print(context_stack[-2].type,"<--", current_node.type)
                # print_ast(context_stack[-2])
    
                context_stack[-2].children.append(current_node)
                # ats.children.append( context_stack.pop())
                
                context_stack.pop()
                current_node = context_stack[-1]
                # print_ast(context_stack[-1])
                # print(len(context_stack))
        flag = True
        if x == tok.type and x == "eof":
            
            ats.children.append(context_stack[0])
            if error:
                print("\t[ El proceso ha finalizado con errores ]")
            else:
                print("\t[ Fin del proceso ]")
            return raiz


        
        if x == tok.type and x != "eof":
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

            context_stack[-1].children.append(NewNode(tok.type, leaf=tok.value, line=tok.lineno, column=tok.lexpos))

        

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
                
                # if getNonTerminalName(x) == "STMTS" or getNonTerminalName(x) == "STMT"  :
                #     print(">>>>>>>>>>>>>>>>>>>>",getNonTerminalName(x))

                    
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

class NodoDerivacion:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)




class NewNode:
    def __init__(self, type, children=None, value=None, leaf=None, line=None, column=None):
        self.type = type
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf
        self.line = line
        self.column = column

class UnexpectedTokenError(Exception):
    pass



def print_ast(node, indent=""):
    print(f"{indent}|{node.type}:", end="")
    if node.leaf:
        print(f"Valor: {node.leaf}")
    else:
        print()
    for child in node.children:
        print_ast(child, indent + "  ")




def imprimir_arbol(nodo, space = ""):
    
    print(f"{space}{nodo.tipo}: {nodo.valor} : {getNonTerminalName(nodo.valor)} Hijos: {len(nodo.hijos)}")
    for hijo in nodo.hijos:
        imprimir_arbol(hijo, space + " ")


def print_children(node, indent=""):
    print(f"{indent}|{node.type}:", end="")
# Analisis semántico

def analizador_semantico(nodo):
    if nodo.type == 'FUNC':
        # print("Analizando función")
        analizar_funcion(nodo)
        
    if nodo.type == 'DECL':
        # print("Analizando declaración")
        analizar_declaracion(nodo)
    # if nodo.type == 'FOR_STMT':
    #     print("Analizando for")
    # if nodo.type == 'WHILE_STMT':
    #     print("Analizando while")
    if nodo.type == 'STMT':
        # print("Analizando statement")
        analizar_statement(nodo)
    
    for child in nodo.children:
        analizador_semantico(child)



def analizar_statement(nodo):
    if nodo.children[0].type == 'DECL':
        return
    childrens = []
    for child in nodo.children:
        # print(child.type)
        childrens.append(child)
    
    if childrens[0].type == 'id' and childrens[1].type == 'asignacion':
        if childrens[2].type == 'const_int':
            pass
        elif childrens[2].type == 'const_float':
            pass
        elif childrens[2].type == 'const_char':
            pass
        elif childrens[2].type == 'id':
            pass
        else:
            print("El valor de la variable en la línea: ", childrens[0].line, " no es válido: ")
            # print(functionInit.type, functionReturnValue.type)


def analizar_funcion(nodo):
    childrens = []
    for child in nodo.children:
        # print(child.type)
        childrens.append(child)

    functionReturn = childrens[-3]
    functionInit = childrens[0]
    functionReturnValue = functionReturn.children[1]
    

    if existe_variable(functionInit.leaf):
        print("La variable en la línea: ", functionInit.line, " ya existe")
        return

    # print(functionReturnValue.type, functionInit.type)
    if functionInit.type == 'int' and functionReturnValue.type == 'const_int':
        insertar_variable(functionInit.type, functionInit.leaf, functionReturnValue.leaf, functionInit.line, functionInit.column)
    elif functionInit.type == 'float' and functionReturnValue.type == 'const_float':
        insertar_variable(functionInit.type, functionInit.leaf, functionReturnValue.leaf, functionInit.line, functionInit.column)
    elif functionInit.type == 'char' and functionReturnValue.type == 'const_char':
        insertar_variable(functionInit.type, functionInit.leaf, functionReturnValue.leaf, functionInit.line, functionInit.column)
    else:
        print("El valor de retorno de la funcion en la línea: ", functionReturnValue.line, " no es válido: ")
        # print(functionInit.type, functionReturnValue.type)


def analizar_declaracion(nodo):
    childrens = []
    for child in nodo.children:
        # print(child.type)
        childrens.append(child)
    varType = childrens[0]
    varName = childrens[1]
    valueType = childrens[3]

    if existe_variable(varName.leaf):
        print("La variable en la línea: ", varName.line, " ya existe")
        return
    
    # print(varType.type, varName.type, valueType.type)
    if varType.type == 'int' and valueType.type == 'const_int':
        insertar_variable(varType.type, varName.leaf, valueType.leaf, varName.line, varName.column)
    elif varType.type == 'float' and valueType.type == 'const_float':
        insertar_variable(varType.type, varName.leaf, valueType.leaf, varName.line, varName.column)
    elif varType.type == 'char' and valueType.type == 'const_char':
        insertar_variable(varType.type, varName.leaf, valueType.leaf, varName.line, varName.column)
    else:
        print("El valor de la variable en la línea: ", varName.line, " no es de tipo: ", varType.type)
        # print(functionInit.type, functionReturnValue.type)

tabla_variables = defaultdict(list)

def insertar_variable(tipo, nombre, valor, linea, columna):
    tabla_variables[nombre].append([tipo, valor, linea, columna])

def existe_variable(nombre):
    return nombre in tabla_variables


def print_ast(node, indent=""):
    print(f"{indent}|{node.type}:", end="")
    if node.leaf:
        print(f"Valor: {node.leaf}")
    else:
        print()
    for child in node.children:
        print_ast(child, indent + "  ")



def generate_p_code(node):
    if node.type == 'FUNC':

        generate_p_code_func(node)

    if node.type == 'DECL':

        generate_p_code_decl(node)
    # if nodo.type == 'FOR_STMT':
    #     print("Analizando for")
    # if nodo.type == 'WHILE_STMT':
    #     print("Analizando while")
    if node.type == 'STMT':

        generate_p_code_stmt(node)
    
    for child in node.children:
        generate_p_code(child)


def generate_p_code_func(node):
    
    p_code = ""
    childrens = []
    for child in node.children:

        childrens.append(child)

    functionInit = childrens[1]

    global string_file 
    p_code += "\nFUNCTION\t" + functionInit.leaf + "\n"
    
    p_code += "BEGIN\n"
    for child in childrens :
        # print("Analisis" + child.type)
        if child.type == 'STMT':
            generate_p_code_stmt(child)
    
    p_code += "END_FUNCTION\n"
    
    # add to file
    string_file += p_code



def generate_p_code_decl(node):
    p_code = ""
    childrens = []
    for child in node.children:
        childrens.append(child)

    global string_file 

    varType = childrens[0]
    varName = childrens[1]
    valueType = childrens[3]

    p_code += "DECLARE_"+varType.type.upper()+"\t"+varName.leaf+"\n\tLOAD_VALUE\t"+str( valueType.leaf)+"\n"

    # add to file
    string_file += p_code


def generate_p_code_stmt(node):
    if node.children[0].type == 'DECL':
        return
    p_code = ""
    childrens = []
    for child in node.children:
        # print(child.type)
        childrens.append(child)
    
    global string_file 

    if childrens[0].type == 'id' and childrens[1].type == 'asignacion':

        p_code += "\tLOAD_VALUE\t"+str(childrens[2].leaf)+"\n"
        p_code += "\tSTORE_VALUE\t"+childrens[0].leaf+"\n"
        

    # add to file
    string_file += p_code



def main():
    ats = NewNode("Raiz")

    arbol_derivacion = miParser(ats)
    # imprimir_tabla_simbolos()
    # imprimir_tabla_resumen()
    # imprimir_arbol(arbol_derivacion)

    
    # print("======================== Arbol de análisis sintáctico ========================")
    # print_ast(ats)

    
    analizador_semantico(ats)
    
    # clean file
    file = open("p_code.txt", "w")
    file.write("")
    file.close()

    generate_p_code(ats)
    # print("======================== Código P ========================")
    # print(string_file)

    # write to file
    file = open("p_code.txt", "w")
    file.write(string_file)
    file.close()

if __name__ == "__main__":
    main()


