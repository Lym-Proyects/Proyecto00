"""
LyM Proyecto 0

Integrantes:

    Cristian Caro - c.caro
    John Suarez - j.serratos
"""
import re
import string
def comprobar(datos):
    print("Bienvenido al programa\n")
    print("Si el programa dice que un elemento no pertence / no es correcto / no existe, hay error en la sintaxis\n")
    letras = list(list(string.ascii_lowercase)+list(string.ascii_uppercase))
    numeros = ["0","1","2","3","4","5","6","7","8","9"]
    letNum = letras+numeros
    x = 0

    action=["walk","jump","jumpTo","veer","look","drop","grab","get","free","pop"]    
    condition=["isfacing","isValid","canWalk","not"]
    directions = ["north", "south", "east", "west"]
    direction2 = [ "right", "left", "front",  "back" ]
    isfac = ["walk", "jump", "grab", "pop", "pick", "free","drop"]
    variablesProg = []
    corchetes = 0
    corcheteUnico = 0

    def verificarVariables(variable:str,lista:list):
        if variable[0] in letras:
            errores = 0
            for caracteres in variable:
                if caracteres not in letNum:             
                    errores += 1
            if errores != 0: return ("no pertenece")
            else:lista.append(variable)
    def verificarParametros(variable:str):
        if variable[0] in letras:
            errores = 0
            for caracteres in variable:
                if caracteres not in letNum:             
                    errores += 1
            if errores != 0: return ("no pertenece")
            
    def revisarCodicionales(condicional,var1,var2):
        if condicional == "isfacing":
            if var1 not in directions:
                print(condicional+" no pertenece")
            else:
                print(condicional+" correcto")
        elif condicional == "isValid":
            if var1 not in isfac:
                print(condicional+" no pertenece")
            else:
                print(condicional+" correcto")
                if var2 not in numeros:
                   verificarParametros(var2)  
        elif condicional == "canWalk":
            if var1 not in directions+direction2:
                print(condicional+" no pertenece")
            else:
                if var2 not in numeros:
                   verificarParametros(var2) 
                print(condicional+" correcto")
        elif condicional == "not":
            if lin[0] not in condition:
                print(condicional+" no pertenece")
        else:
            print(condicional+" no pertenece")

    with open(datos,"r+") as f:
        text = f.readlines()
        for indice, line in enumerate(text):
            x +=1
            if x == 1:
                if line.startswith("PROG"): print("Comienza por PROG")
                else: print("El programa no pertenece debido a que no empieza por: 'PROG' \n")
            if x==indice:
                if line.startswith("GORP"): print("Terminación por GORP")
                else: print("El programa no pertenece al no terminar por 'GORP' \n")

            line = re.sub("\t","",line) #quita \t, es como .replace
            linea = line.splitlines() #separa por lista si hay un \n
            lin="".join(linea)
            lin=lin.replace(" ","")
            #print(lin) #putCB(2,1)
            # verifica var
            if "var" in lin:
                lin = lin.replace("var","") ###confirmado var, lo elimina
                if ";" in lin[len(lin)-1]:   ### verifica que exista ;
                    lin = lin.replace(";","")
                else: print("No pertenece") 
                lin = lin.split(",")        ### divide las variables por las ,
                for variable in lin:       ### verifica que los nombres esten bien declarados
                    verificarVariables(variable,variablesProg)
                #print(variablesProg)

            if "PROC" in lin:
                corchetes += 1
                lin = lin.replace("PROC","")
                if "()" in lin:
                    lin = lin.replace("()","")
                    verificarVariables(lin,action)
                    #print(action)
                elif ")" in lin:
                    lin = lin.replace(")","")
                    lin = lin.split("(")
                    verificarVariables(lin[0],action)
                    lin[1] = lin[1].split(",")
                    for var in lin[1]:
                        verificarVariables(var,variablesProg)
                    #print(variablesProg)
            if lin == "{": 
                corchetes+=1
                if corchetes ==1: corcheteUnico += 1
            if lin == "}": 
                if corchetes==2: corchetes-=2
                else: corchetes -= 1
                if corcheteUnico==1:corcheteUnico-=1
            if corchetes == 2:
                if "while" in lin:
                    lin = lin.replace("while","")
                    if "od" in lin:
                        lin = lin.replace("od","")
                        if "do" in lin:
                            lin = lin.split("do")
                            lin[0]=lin[0][1:]
                            lin[0]=lin[0][:-1]
                            lin[1]=lin[1][1:]
                            lin[1]=lin[1][:-1]
                            for condit in condition:
                                if condit in lin[0]:
                                    lin[0]=lin[0].replace(condit,"")
                                    lin[0]=lin[0][1:]
                                    lin[0]=lin[0][:-1]
                                    lin[0] =lin[0].split(",")
                                    revisarCodicionales(condit,lin[0][0],lin[0][1])
                            for process in action:
                                if process in lin[1]:
                                    lin[1]=lin[1].replace(process,"")
                                    lin[1]=lin[1][1:]
                                    lin[1]=lin[1][:-1]
                                    if "," in lin:
                                        lin[1] = lin[1].split(",")
                                        for cada in lin[1]:
                                            if cada not in numeros+directions:
                                                verificarParametros(cada)       
                                    else:
                                        if lin[1] not in numeros+directions: 
                                            verificarParametros(lin[1])
                        else: print("no pertenece")    
                    else: print("no pertenece")

                elif "if" in lin:
                    lin=lin.replace("if","")
                    if "fi" in lin:
                        lin=lin.replace("fi","")
                        lin=lin.split("{")
                        lin[0]=lin[0][1:]
                        lin[0]=lin[0][:-1]
                        #print(lin[0]) #canWalk(west,1)
                        if "}" in lin[1]:
                            lin[1]=lin[1].replace("}","") #walk(west,1)
                            #print(lin[1])
                        else: print("no pertenece")
                        for condit in condition:
                                if condit in lin[0]:
                                    lin[0]=lin[0].replace(condit,"")
                                    lin[0]=lin[0][1:]
                                    lin[0]=lin[0][:-1]
                                    lin[0] =lin[0].split(",")
                                    revisarCodicionales(condit,lin[0][0],lin[0][1])
                        for process in action:
                                if process in lin[1]:
                                    lin[1]=lin[1].replace(process,"")
                                    lin[1]=lin[1][1:]
                                    lin[1]=lin[1][:-1]
                                    if "," in lin:
                                        lin[1] = lin[1].split(",")
                                        for cada in lin[1]:
                                            if cada not in numeros+directions:
                                                verificarParametros(cada)       
                                    else:
                                        if lin[1] not in numeros+directions: 
                                            verificarParametros(lin[1])
                    else: print("no pertenece")
                else:
                    for proceso in action:
                        if proceso in lin:
                            lin = lin.replace(proceso,"")
                            if ";" in lin: lin = lin.replace(";","")
                            if "(" in lin and ")" in lin:
                                lin = lin.replace("(","")
                                lin = lin.replace(")","")
                                if "," in lin:
                                    lin.split(",")
                                    for var in lin:
                                        if var not in variablesProg:
                                            print("no pertenece")
                                else:
                                    if lin in variablesProg: print("Pertenece")
                                    else: print("No pertenece")
                                print(lin)
            if corcheteUnico == 1:
                for act in action:
                    if act in line:
                        lin=lin.replace(act,"")
                        lin=lin[1:]
                        lin = lin[:-1]
                        if "," in lin:
                            lin = lin.split(",")
                            for cada in lin:
                                if cada not in numeros+directions:
                                    verificarParametros(cada)
                                    print(cada)
                        else:
                            if lin not in numeros+directions: 
                                verificarParametros(lin)
                if "=" in lin:
                    lin=lin.replace(";","")
                    lin=lin.split("=")
                    verificarVariables(lin[0],variablesProg)
                    if lin[1] not in numeros:
                        print("no pertenece")
        print("Número líneas: "+str(x))
print(comprobar("prueba.txt"))