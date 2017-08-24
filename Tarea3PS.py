import nltk
import numpy as np
import math    
from nltk.stem.porter import *
import plotly
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout
import plotly.plotly as py
import plotly.graph_objs as go
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words.add(".")
ps = PorterStemmer()    

def similitud_cos(matriz, query):
    doc_iguales=[]
    longitud = matriz.shape
    sum_doc=0
    for i in range(0,longitud[1]):
        sum_doc= float(sum_doc) + pow(query[i],2)
    for i in range(0, longitud[0]):
        sum=0
        sum2=0
        for j in range(0, longitud[1]):
            sum= float(sum) + matriz[i,j]*query[j]
            sum2= float(sum2) + pow(matriz[i,j],2)
        if math.sqrt(sum2) > 0:
            coseno = sum/float(math.sqrt(sum2*sum_doc))
            #print str(i) + "     = " + str(coseno)
        if coseno > 0:    
            doc_iguales.append([i+1, coseno])
    doc_iguales = sorted(doc_iguales, key=lambda frec:frec[1], reverse=True)
    return doc_iguales
    
def cargar_consultas():
    doc_consultas = nltk.Text(nltk.regexp_tokenize(open("/Users/gabriel/Documents/INAOE/2do Cuatrimestre/Recuperacion/corpus/cacm/query.text","r").read().lower(), "[a-z'.]+"))
    consultas=[]
    consulta=[]
    flag = 0
    for word in doc_consultas:
        if word == ".w":
            flag = 1
        if (word == ".n" and flag == 1) or (word == ".a" and flag == 1):
            flag = 0
            consultas.append(consulta)
            consulta=[]
        if flag == 1 and word != ".w":
            consulta.append(ps.stem(word).encode("ascii"))
    return consultas

def crear_vector_consulta(consulta, vocabulario, array_idf):
    matriz_vector_consulta = np.zeros((3, len(vocabulario)))
    j=0
    for word in vocabulario:
        if len(consulta) > 0:
            matriz_vector_consulta[0,j]=consulta.count(word) #/ float(len(titulo))
            if consulta.count(word) > 0:
                print vocabulario[j]
                matriz_vector_consulta[0,j]=1
        j=j+1
    for i in range(0, array_idf.size):
        matriz_vector_consulta[2,i]=matriz_vector_consulta[1,i]*array_idf[i]
    return matriz_vector_consulta    

def procesar_qrels():
    qrels = {}
    archivo = open("/Users/gabriel/Documents/INAOE/2do Cuatrimestre/Recuperacion/corpus/cacm/qrels.text", "r")
    for linea in archivo.readlines():
        linea_split = linea.split(" ");
        query = int(linea_split[0])
        if query not in qrels.keys():
            qrels[query] = []
        qrels[query] += [int(linea_split[1])]
    qrels = qrels.items()
    qrels.sort(key=lambda x: len(x[1]), reverse = True)
    
    aux=[] 
    for i in range(0,5):
       aux.append(qrels[i])
    for i in range(len(qrels)-5,len(qrels)):
       aux.append(qrels[i])
    qrels=aux
    print len(qrels)
    return qrels

def procesar_consultas(binaria): 
    consultas = cargar_consultas();
    qrels = procesar_qrels()
    valores_final=[]   
    for i in range(0,len(qrels)):
        consulta_vectores= crear_vector_consulta(consultas[qrels[i][0]-1], vocabulario,array_idf)
        documentos_relevantes = similitud_cos(binaria, consulta_vectores[0,])
        print len(documentos_relevantes) 
        pres = 0
        rec = 0
        cont =0 
        recuerdo=[]
        presicion=[]
        q_rel = qrels[i]
        for j in range(0,len(documentos_relevantes)):
            doc_rel = documentos_relevantes[j]
            if q_rel[1].count(doc_rel[0]) > 0:
                rec = rec +  1/float(len(q_rel[1]))
                recuerdo.append(rec)
                cont = cont +1
                pres = cont/float(j+1) 
                presicion.append(pres)
                print cont, "   doc ", doc_rel[0], "   ", rec, "   ,   ", pres 
        valores=[]
        valores.append(recuerdo)
        valores.append(presicion)
        valores.append(len(documentos_relevantes))
        valores_final.append(valores)
    return valores_final

#--------------------------------------------------------------------------------            
def graficar(datos_binario, datos_tf,datos_tf_idf, qrels, indice):
    recuerdo_bin=datos_binario[0]
    presicion_bin=datos_binario[1]
    recuerdo_tf=datos_tf[0]
    presicion_tf=datos_tf[1]
    recuerdo_tf_idf=datos_tf_idf[0]
    presicion_tf_idf=datos_tf_idf[1]

    trace0 = go.Scatter(
    x = recuerdo_bin,
    y = presicion_bin,
    name = 'Binario',
    line = dict(
        #color = ('rgb(205, 12, 24)'),
        width = 1),
        mode = 'lines+markers'
    )     
    trace1 = go.Scatter(
    x = recuerdo_tf,
    y = presicion_tf,
    name = 'TF',
    line = dict(
        #color = ('rgb(22, 96, 167)'),
        width = 1),
        mode = 'lines+markers'
    ) 
    trace2 = go.Scatter(
    x = recuerdo_tf_idf,
    y = presicion_tf_idf,
    name = 'TF-IDF',
    line = dict(
        #color = ('rgb(200, 150, 89)'),
        width = 1),
        mode = 'lines+markers'
    ) 
    data = [trace0, trace1, trace2]

    name = "Consulta " + str(qrels[0])
    # Edit the layout
    layout = dict(title = name,
        xaxis = dict(title = 'Recuerdo'),
        yaxis = dict(title = 'Presicion'),
        )
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.08,
                                  xanchor='center', yanchor='top',
                                  text="        Documentos Recuperados: " + str(datos_binario[2]) + "     Documentos Relevantes: " + str(len(datos_binario[1])) + "/" + str(len(qrels[1])),
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(50,50,50)'),
                                  showarrow=False))
    
    layout['annotations'] = annotations
    fig = dict(data=data, layout=layout)
    name = name + ".html"
    plot(fig, filename=name)
#------------------------------------------------------------------ 
doc = nltk.Text(nltk.regexp_tokenize(open("/Users/gabriel/Documents/INAOE/2do Cuatrimestre/Recuperacion/corpus/cacm/cacm.all","r").read().lower(),"[a-z'.]+"))
palabras=[]
titulos=[]
titulo=[]
flag = 0
for word in doc:
    if word == ".t":
        flag = 1
    if (word == ".b" and flag == 1) or (word == ".w" and flag == 1) or (word == ".a" and flag == 1):
        flag = 0
        titulos.append(titulo)
        titulo=[]
    if flag == 1 and word != ".t" and word != "aed" and word not in stop_words:
        palabras.append(ps.stem(word).encode("ascii"))
        titulo.append(ps.stem(word).encode("ascii"))
from nltk import FreqDist
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

datos_binario = procesar_consultas(binaria)
datos_tf = procesar_consultas(matriz_tf)
datos_tf_idf = procesar_consultas(matriz_idf)
qrels = procesar_qrels()
for i in range(0,len(datos_binario)):
    graficar(datos_binario[i], datos_tf[i],datos_tf_idf[i],qrels[i],i)






