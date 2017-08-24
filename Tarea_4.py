import nltk
from nltk import word_tokenize
from nltk import FreqDist
import numpy as np
import math
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def similitud_cos(matriz, documento, titulos, bigramas):
    doc_iguales=[]
    longitud = matriz.shape
    sum_doc=0
    for i in range(0,longitud[1]):
        sum_doc= float(sum_doc) + pow(matriz[documento,i],2)
    for i in range(0, longitud[0]):
        sum=0
        sum2=0
        for j in range(0, longitud[1]):
            sum= float(sum) + matriz[i,j]*matriz[documento,j]
            sum2= float(sum2) + pow(matriz[i,j],2)
        if math.sqrt(sum2) > 0:
            coseno = sum/float(math.sqrt(sum2*sum_doc))
            #print str(i) + "     = " + str(coseno)
        doc_iguales.append([coseno, i])
    doc_iguales = sorted(doc_iguales, key=lambda frec:frec[0], reverse=True)
    for i in range(1,6):
        indice = doc_iguales[i][1]
        titulo=""
        for word in titulos[indice]:
            if bigramas == "SI":
                if isinstance(word,str):
                    titulo = titulo + " " + word
            else:
                titulo = titulo + " " + word[0]
        print str(doc_iguales[i]) + "\t" + titulo
        
def ver_titulos(matriz,titulos, peso, bigramas):
    print "-----------------------------------------------------------------------------------------------------------"
    print "Peso de los terminos: " + peso
    for i in range(0,3):
        titulo=""
        for word in titulos[i]:
            if bigramas == "SI":
                if isinstance(word,str):
                    titulo = titulo + " " + word
            else:
                titulo = titulo + " " + word[0]
        print "-----------------------------------------------------------------------------------------------------------"
        print "Documentos similares a: " + str(i+1) + " - " + titulo 
        similitud_cos(matriz,i, titulos,bigramas)
        
bigramas = "SI"        
doc = nltk.Text(nltk.regexp_tokenize(open("/Users/gabriel/Documents/INAOE/2do Cuatrimestre/Recuperacion/corpus/cacm/cacm.all","r").read().lower(),"[a-z'.]+"))
palabras=[]
titulos=[]
titulo=[]
titulo_txt=""
flag = 0
for word in doc:
    if word == ".t":
        flag = 1
    if (word == ".b" and flag == 1) or (word == ".w" and flag == 1) or (word == ".a" and flag == 1):
        flag = 0
        text = word_tokenize(titulo_txt)
        if bigramas == "SI":
            titulo=text
            titulo = titulo + list(nltk.bigrams(text))
            titulos.append(titulo)
        else:
            titulos.append(nltk.pos_tag(text))
        if word not in stop_words:
            if bigramas == "SI":
                palabras = palabras + text;
                palabras = palabras + list(nltk.bigrams(text))
            else:
                palabras = palabras + nltk.pos_tag(text)
        titulo_txt = ""
        titulo=[]
    if flag == 1 and word != ".t":
        titulo_txt = titulo_txt + word + " "

fdist=FreqDist(palabras)
vocabulario = fdist.keys()
frec=fdist.values()
frecuencias=[]
matriz_tf = np.zeros((len(titulos), len(vocabulario)))
binaria = np.zeros((len(titulos), len(vocabulario)))
matriz_idf = np.zeros((len(titulos), len(vocabulario)))
array_idf = np.zeros((len(vocabulario)))
i=0
for titulo in titulos:
    j=0
    for word in vocabulario:
        if len(titulo) > 0:
            matriz_tf[i,j]=titulo.count(word) #/ float(len(titulo))
            if titulo.count(word) > 0:
                binaria[i,j]=1
                array_idf[j] = array_idf[j] + 1
        j=j+1
    i=i+1
for i in range(0, array_idf.size):
    array_idf[i] = math.log(len(titulos)/float(array_idf[i]))
    for j in range(0, len(titulos)):
        matriz_idf[j,i]=matriz_tf[j,i]*array_idf[i]
    
print "Numero de documentos: " + str(len(titulos))
print "El numero total de palabras es: " + str(len(palabras))
print "El vocabulario contiene: " + str(len(vocabulario)) + " palabras"
ver_titulos(binaria,titulos, " * BINARIO *", bigramas)
ver_titulos(matriz_tf,titulos, " * TF *",bigramas)
ver_titulos(matriz_idf,titulos, " * TF-IDF *",bigramas)