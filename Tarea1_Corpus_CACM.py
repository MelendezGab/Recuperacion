# PRIMERA TAREA
# Fecha de entrega: viernes 27 de enero; ANTES de las 12:00.
# mandar código por email, así como impresión de salida.
#
# Para dos colecciones (las que quieran, aunque CACM me gustaría) hagan lo siguiente:
#
# - obtengan su vocabulario (es decir, conjunto de palabras diferentes)
# - para cada palabra midan las siguientes dos cosas:
# a) frecuencia - número de veces que ocurre en colección
# b) frecuencia de documento - número de documentos en los que aparece.
# - imprimir el 10% de palabras más frecuentes (caso a) )
#
# Hacer todos los puntos anteriores usando las palabras como aparecen y otra haciendo normalización (trasformar a minúsculas, quitar acentos, y hacer stemming).
import nltk
doc = nltk.Text(nltk.regexp_tokenize(open("/Users/gabriel/Documents/corpus/cacm/cacm.all","r").read(),"[A-Za-z'.]+"))
palabras=[]
titulos=[]
titulo=""
flag = 0
for word in doc:
    if word == ".T":
        flag = 1
    if (word == ".B" and flag == 1) or (word == ".W" and flag == 1):
        flag = 0
 #       print titulo
        titulos.append(titulo)
        titulo=""
    if flag == 1 and word != ".T":
        palabras.append(word)
        titulo = titulo + " " + word
vocabulario = set(palabras)
print "Numero de documentos: " + str(len(titulos))
print "El numero total de palabras es: " + str(len(palabras))
print "El vocabulario contiene: " + str(len(vocabulario)) + " palabras"
frecuencias=[]
for word in vocabulario:
    cont=0 
    cont_doc=0
    aux=[]
    for cadena in titulos:
        aux=cadena.split(" ")
        cont = cont + aux.count(word)
        if aux.count(word) > 0:
            cont_doc = cont_doc + 1
    frecuencias.append([word, cont, cont_doc])    
cont = 0
for fr in frecuencias:
    cont = cont + fr[1]
    
frecuencias = sorted(frecuencias, key=lambda frec:frec[1], reverse=True)

print "El 10% de las palabras del vocabulario son las siguientes " + str(round(len(frecuencias)*0.1)) + ":"
print "(Palabra, Frecuencia en Corpus, Numero de documentos en los que aparece)" 

for i in range(0, int(round(len(frecuencias)*0.1))):
    print frecuencias[i]

#-------------------------------------------------------------
print "Preprocesado"
from nltk.stem.lancaster import LancasterStemmer
ps = LancasterStemmer()

doc = nltk.Text(nltk.regexp_tokenize(open("/Users/gabriel/Documents/corpus/cacm/cacm.all","r").read().lower(),"[a-z'.]+"))

print doc.count(".t")
palabras=[]
titulos=[]
titulo=""
flag = 0
for word in doc:
    if word==".t":
        flag = 1
    if (word == ".b" and flag == 1) or (word==".w" and flag == 1):
        flag = 0
 #       print titulo
        titulos.append(titulo)
        titulo=""
    if flag == 1 and word != ".t":
        palabras.append(ps.stem(word).encode("ascii"))
        titulo = titulo + " " + ps.stem(word).encode("ascii")
    
vocabulario = set(palabras)
print "Numero de documentos: " + str(len(titulos))
print "El numero total de palabras es: " + str(len(palabras))
print "El vocabulario contiene: " + str(len(vocabulario)) + " palabras"
frecuencias=[]
for word in vocabulario:
    cont=0 
    cont_doc=0
    aux=[]
    for cadena in titulos:
        aux=cadena.split(" ")
        cont = cont + aux.count(word)
        if aux.count(word) > 0:
            cont_doc = cont_doc + 1
    frecuencias.append([word, cont, cont_doc])    
cont = 0
for fr in frecuencias:
    cont = cont + fr[1]
    
frecuencias = sorted(frecuencias, key=lambda frec:frec[1], reverse=True)

print "El 10% de las palabras del vocabulario son las siguientes " + str(round(len(frecuencias)*0.1)) + ":"
print "(Palabra, Frecuencia en Corpus, Numero de documentos en los que aparece)" 

for i in range(0, int(round(len(frecuencias)*0.1))):
    print frecuencias[i]
print(round(len(frecuencias)*0.1))
    