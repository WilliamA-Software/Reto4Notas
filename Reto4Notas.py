"""
Created on Thu Oct 15 17:33:33 2020

@author: otato
"""

"""
Retorne una tupla en la que el primer elemento es un diccionario cuyas
claves sean los nombres de las facultades, ordenados alfabéticamente, y los valores sean el promedio ponderado de las
materias correspondientes. El segundo elemento de la tupla debe ser una lista con los correos institucionales de todos
los estudiantes utilizados para el cálculo del promedio.

"""

#RETO 4 - SOFTWARE UNIVERSITARIO

#tupla del resultado
#tuplaResultado = tuple()
#correos
listaCorreos = []

#facultades
facultades = set()

#diccionario para calculo de notas
diccionarioNotaXFacultad = dict()
#diccionario para calculo de creditos
diccionarioCreditoXFacultad = dict()

#diccionario de los restulados. Clave (facultad) : Valor (promedio ponderado)
diccionarioResultado = dict()

def promedio_facultades(info:dict, contando_externos: bool = True) -> tuple:
    mivariable = info.items()
    
    #ciclo por codigo del estudiante
    try:
        for key, value in mivariable:
            
            #datos generales de cada estudiante
            nombre = value['nombres']                           #nombres
            apellido = value['apellidos']                       #apellidos
            numeroDocumento = str(value['documento'])           #numero de documento
            programaEstudiante = value['programa']              #codigo del programa del estudiante
            materias = value['materias']                        #datos de las materias (global)
            
            if(len(materias) == 0):
                #no tiene ninguna materia
                continue
            
            i = 0
            creacionCorreo = False
            
            while i < len(materias):
                #acceder a los datos de cada materia
                cadaFacultadMateria = materias[i]['facultad']       #nombre de la facultad de la materia
                cadaCodigoMateria = materias[i]['codigo']           #codigo de la materia
                cadaNotaMateria = materias[i]['nota']               #nota en esa materia
                cadaCreditosMateria = materias[i]['creditos']       #creditos de esa materia
                cadaRetiradaMateria = materias[i]['retirada']       #se retiro la materia (Si/No)
    
                if(cadaCreditosMateria == 0 or cadaNotaMateria == 0 or cadaRetiradaMateria == "Si"):
                    #esta materia no cuenta por nota, credito o retirada
                    i = i + 1
                    continue
    
                else:
                    
                    #ahora comprobar si se puede sumar los externos
                    if(contando_externos == True):
                        #aqui toca contar de todo ya que cuenta locales y externos
                        #-----------------------------
                        
                        #añado la facultad del estudiante en un conjunto
                        facultadAdicionada = adicionarFacultad(cadaFacultadMateria)
                        
                        #vamos a proceder a calcular el promedio notas con sus creditos
                        NotasXCreditos(cadaNotaMateria, cadaCreditosMateria, cadaFacultadMateria) 
                        
                        
                        
                        if(creacionCorreo == False):
                            #calcular el correo por estudiante
                            miCorreo = sacarCorreo(nombre,apellido,numeroDocumento)
                        
                            #añadir el correo a una lista
                            listaCorreos.append(miCorreo)
                            
                            creacionCorreo = True
                        
                    else:
                        #no vamos a contar los externos
                        #hallando el codigo de externos
                        #codigoExterno = str(key)
                        codigoDeExterno = str(key)
                        #codigoExterno = codigoDeExterno[4:6]
                        
                        #hallando que sea su materia de la misma carrera del estudiante
                        #mira si esa materia pertenece a su programa
                        materiaDeSuPrograma = materiaEsDePrograma(programaEstudiante, cadaCodigoMateria, cadaFacultadMateria)
                        if(materiaDeSuPrograma == False or codigoDeExterno == "05" or codigoDeExterno == "03"):
                            #no cuenta para sumarse ya que es externo y no los vamos a tener en cuenta
                            i = i + 1
                            continue
                        
                        else:
                            #si cuenta para sumarse
                            #aqui toca contar de todo ya que cuenta locales y externos
                            #-----------------------------
                            
                            #añado la facultad del estudiante en un conjunto
                            facultadAdicionada = adicionarFacultad(cadaFacultadMateria)
                            
                            #vamos a proceder a calcular el promedio notas con sus creditos
                            NotasXCreditos(cadaNotaMateria, cadaCreditosMateria, cadaFacultadMateria) 
                        
                            
                            
                            if(creacionCorreo == False):
                                #calcular el correo por estudiante
                                miCorreo = sacarCorreo(nombre,apellido,numeroDocumento)
                            
                                #añadir el correo a una lista
                                listaCorreos.append(miCorreo)
                                
                                creacionCorreo = True
                            
                        
                        #print(codigoExterno)
    
                i = i + 1
    
        
            
        for n in facultadAdicionada:
            #capturar el resultado de cada facultad
            notaDeDiccionario = diccionarioNotaXFacultad[n]
            creditoDeDiccionario = diccionarioCreditoXFacultad[n]
            
            #hacer el calculo de nota / credito
            calculoSinRedondear = notaDeDiccionario / creditoDeDiccionario
            
            #redondear el resultado del calculo
            calculo = round(calculoSinRedondear,2)
            diccionarioResultado[n] = calculo
    
        
        #ordenar mi diccionario de manera alfabetica    
        diccionarioResultadoOrdenado = dict(sorted(diccionarioResultado.items()))
        
        #ordenar los correos de manera alfabetica
        listaCorreosOrdenada = sorted(listaCorreos)
        
        nuevalista = []
        nuevalista.append(diccionarioResultadoOrdenado)
        nuevalista.append(listaCorreosOrdenada)
        
        tuplaResultado = tuple(nuevalista)
        return tuplaResultado
    except:
        return "Error numérico."

    
    

#funcion para almacenar las notas y los creditos
def NotasXCreditos(nota, credito, facultad):
    
    producto = nota * credito
        
    if(facultad in diccionarioNotaXFacultad or facultad in diccionarioCreditoXFacultad):
        
        diccionarioNotaXFacultad[facultad] = producto + diccionarioNotaXFacultad[facultad]
        diccionarioCreditoXFacultad[facultad] = credito + diccionarioCreditoXFacultad[facultad]
        
    else:
        diccionarioNotaXFacultad[facultad] = producto
        diccionarioCreditoXFacultad[facultad] = credito

#funcion para adicionar la facultad en el conjunto
def adicionarFacultad(cadaFacultadMateria):
    facultades.add(cadaFacultadMateria)
    #convertir el conjunto en una lista
    listaFacultades = list(facultades)
    
    #organizar las facultades por orden alfabetico
    listaFacultadesOrganizadas = sorted(listaFacultades)
    return listaFacultadesOrganizadas

#funcion para verificar si esta materia es del programa del estudiante
def materiaEsDePrograma(programaEstudiante, cadaCodigoMateria,cadaFacultadMateria) -> bool:
    #valida si esta materia es de su programa
    if programaEstudiante[0:2] in cadaCodigoMateria:
        
        #la materia si es de su programa
        materiaDeSuPrograma = True
    else:
        
        #la materia no es de su programa
        materiaDeSuPrograma = False
    return materiaDeSuPrograma

#funcion para crear los correos
def sacarCorreo(x,y,doc):
    #x es nombre
    #y es apellido
    #doc es documento
    
    #armar un array con primer y segundo dato separados
    trozo = x.split()
    trozoApellido = y.split()
    
    if(len(trozo) == 2):
        
        #capturar los nombres
        primerNombre = trozo[0]
        segundoNombre = trozo[1]
        
        #capturar la primera letra de los nombres
        primerCaracter = primerNombre[0]
        segundoCaracter = segundoNombre[0]
        
        #capturar primer apellido
        primerApellido = trozoApellido[1]
        
        #capturar ultimos 2 digitos del documento
        ultimosNumeroDoc = doc[len(doc)-2:len(doc):]
    
        #armar nuestro correo
        correo = primerCaracter + segundoCaracter + "." + primerApellido + ultimosNumeroDoc
    
    elif(len(trozo) == 1):
        
        #capturar el nombre y el primer caracter
        primerNombre = trozo[0]
        primerCaracter = primerNombre[0]
        
        #capturar primer apellido y el primer caracter
        primerApellido = trozoApellido[1]
        primerCaracterApellido = primerApellido[0]
        
        #capturar el segundo apellido
        original = trozoApellido[0]
        segundoApellido = original.replace(",", "")
        
        #capturar ultimos 2 digitos del documento
        ultimosNumeroDoc = doc[len(doc)-2:len(doc):]
        
        #armar nuestro correo
        correo = primerCaracter + primerCaracterApellido + "." + segundoApellido + ultimosNumeroDoc
        
    else:
        print("error, tiene mas de 2 nombres o tiene 0 nombres") 
    
    #convertir nuestro correo a minusculas
    correo = correo.lower()
    
    #quitar tildes y eñes
    for letra in correo:
        if ("á" == letra):
            correo = correo.replace("á", "a")
        elif ("é" == letra):
            correo = correo.replace("é", "e")
        elif ("í" == letra):
            correo = correo.replace("í", "i")
        elif ("ó" == letra):
            correo = correo.replace("ó", "o")
        elif ("ú" == letra):
            correo = correo.replace("ú", "u")
        elif ("ñ" == letra):
            correo = correo.replace("ñ", "n")

    return correo

#PRUEBA 5 DE IMASTER
# Prueba 2:
print(promedio_facultades({
					20170116008:{
								"nombres" : "Sofia Natalia",
								"apellidos" : "Martinez, Alvarez",
								"documento" : 86056697,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-3145",
												"nota" : 3.79,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1882",
												"nota" : 3.02,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-4916",
												"nota" : 3.99,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9576",
												"nota" : 3.2,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-7401",
												"nota" : 4.08,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20180181912:{
								"nombres" : "Julian Andres",
								"apellidos" : "Fernández, Gómez",
								"documento" : 38203099,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-4822",
												"nota" : 3.99,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6559",
												"nota" : 3.09,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20170131506:{
								"nombres" : "Laura Camila",
								"apellidos" : "Cuellar, Pérez",
								"documento" : 15755411,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-7857",
												"nota" : 3.19,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1857",
												"nota" : 2.62,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1415",
												"nota" : 2.83,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1720",
												"nota" : 2.58,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100240601:{
								"nombres" : "Andres Julian",
								"apellidos" : "Ochoa, Romero",
								"documento" : 81959788,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-7472",
												"nota" : 3.6,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-5465",
												"nota" : 2.58,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8357",
												"nota" : 4.69,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9511",
												"nota" : 2.51,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3379",
												"nota" : 4.31,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20160386484:{
								"nombres" : "Julio",
								"apellidos" : "Sánchez, Fernández",
								"documento" : 95423746,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 2.83,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 2.53,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2620",
												"nota" : 4.06,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20190365550:{
								"nombres" : "Catalina Valentina",
								"apellidos" : "García, López",
								"documento" : 88933669,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5278",
												"nota" : 3.45,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1857",
												"nota" : 4.56,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9835",
												"nota" : 3.93,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 4.46,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20150173830:{
								"nombres" : "Catalina Valentina",
								"apellidos" : "Fernández, Guitiérrez",
								"documento" : 36216549,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-3520",
												"nota" : 2.71,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5596",
												"nota" : 4.7,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6981",
												"nota" : 2.79,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5596",
												"nota" : 2.51,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5161",
												"nota" : 2.36,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100383099:{
								"nombres" : "Juan Pablo",
								"apellidos" : "Moreno, Cordoba",
								"documento" : 17911136,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-9115",
												"nota" : 4.18,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6074",
												"nota" : 3.73,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20090198116:{
								"nombres" : "Sofia Gabriela",
								"apellidos" : "Diaz, Moreno",
								"documento" : 62587112,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-1157",
												"nota" : 2.45,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-7915",
												"nota" : 4.17,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-5962",
												"nota" : 4.49,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190262931:{
								"nombres" : "Paula Natalia",
								"apellidos" : "Torres, Jiménez",
								"documento" : 18534577,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2081",
												"nota" : 4.43,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8458",
												"nota" : 4.77,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-1258",
												"nota" : 3.15,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190299456:{
								"nombres" : "Natalia Paula",
								"apellidos" : "Moreno, Alvarez",
								"documento" : 89771722,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7322",
												"nota" : 4.27,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-5808",
												"nota" : 3.19,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4470",
												"nota" : 2.26,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7972",
												"nota" : 3.66,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20150172603:{
								"nombres" : "Catalina Paula",
								"apellidos" : "Pérez, Diaz",
								"documento" : 59641117,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8636",
												"nota" : 4.65,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-1999",
												"nota" : 2.52,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3063",
												"nota" : 2.95,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20160197253:{
								"nombres" : "Julian Mateo",
								"apellidos" : "Jiménez, Fernández",
								"documento" : 41016120,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9348",
												"nota" : 4.55,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9306",
												"nota" : 2.77,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-1836",
												"nota" : 3.66,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20160174103:{
								"nombres" : "Mateo Julio",
								"apellidos" : "Diaz, López",
								"documento" : 88132707,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-2104",
												"nota" : 4.55,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3425",
												"nota" : 3.98,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4686",
												"nota" : 4.97,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-9455",
												"nota" : 2.43,
												"creditos" : 0,
												"retirada" : "Si",
												},
											]
								},
					20150384070:{
								"nombres" : "Carolina Natalia",
								"apellidos" : "López, Gómez",
								"documento" : 33424549,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7322",
												"nota" : 2.49,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-4101",
												"nota" : 3.14,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-8021",
												"nota" : 2.97,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7470",
												"nota" : 4.77,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					}, False ))
# Expected return:
# ({'Arquitectura': 3.84, 'Diseño': 3.37, 'Historia del Arte': 3.66, 'Ingenieria': 3.88, 'Medicina': 3.45}, ['aj.romero88', 'cn.gomez49', 'cp.diaz17', 'cv.guitierrez49', 'cv.lopez69', 'jf.sanchez46', 'jm.fernandez20', 'jp.cordoba36', 'lc.perez11', 'mj.lopez07', 'np.alvarez22', 'pn.jimenez77', 'sg.moreno12', 'sn.alvarez97'])
