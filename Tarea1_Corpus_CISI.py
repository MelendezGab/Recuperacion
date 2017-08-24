import nltk
doc = nltk.Text(nltk.regexp_tokenize(open("/Users/gabriel/Documents/corpus/cisi/CISI.ALL","r").read(),"[A-Za-z'.]+"))
palabras=[]
titulos=[]
titulo=""
flag = 0
for word in doc:
    if word == ".T":
        flag = 1
    if (word == ".A" and flag == 1) or (word == ".W" and flag == 1):
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

from nltk.stem.porter import *
ps = PorterStemmer()

doc = nltk.Text(nltk.regexp_tokenize(open("/Users/gabriel/Documents/corpus/cisi/CISI.ALL","r").read().lower(),"[a-z'.]+"))

print doc.count(".t")
palabras=[]
titulos=[]
titulo=""
flag = 0
for word in doc:
    if word==".t":
        flag = 1
    if (word == ".a" and flag == 1) or (word==".w" and flag == 1):
        flag = 0
 #       print titulo
        titulos.append(titulo)
        titulo=""
    if flag == 1 and word != ".t" and word != ".i":
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
    


