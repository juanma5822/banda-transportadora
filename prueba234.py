import pandas as pd
from flask import Flask, redirect, url_for, request, json, render_template
import psycopg2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from time import sleep
from matplotlib import cm
from matplotlib import colors

app = Flask(__name__)
conexion=psycopg2.connect(user='xxbafeigeplqzf',
                          password='292103424cc1246aebe3a724ba93b366f7bcb06ae9d2c700b1cfd305b03e6d80',
                          host='ec2-34-227-120-79.compute-1.amazonaws.com',
                          port=5432,
                          database='d4reu6rdlo91uc')

cursor=conexion.cursor()


@app.route("/",methods=("POST","GET"))
def index():
    cursor
    sql=("SELECT * from datosrecibidos ")
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data,columns=["id",'cajas_p','cajas_g'])
    df['cajas_p']=df['cajas_p'].astype('int64')
    df['cajas_g']=df['cajas_g'].astype('int64')
    print(df.info())
    suma_p=df['cajas_p'].sum()
    suma_g=df['cajas_g'].sum()
    datos=[suma_p,suma_g]
    ejex=['cajas pequeñas','cajas grandes']
    #fig, ax = plt.subplots(1,2)
    normdata= colors.Normalize(0, max(datos))
    colormap = cm.get_cmap("Blues")
    colores =colormap(normdata(datos))
    colores_list=['Red','Orange']
    graph=plt.bar(ejex,datos,color=colores_list)
    i = 0
    for p in graph:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text(x+width/2,
                y+height*1.01,
                str(datos[i]),
                ha='center',
                weight='bold')
        i+=1
    plt.savefig("static/Ejemplo3.jpg")
    plt.close()
    desfase = (0.2, 0.1)
    plt.pie(datos,labels=ejex,autopct="%0.1f %%",colors=colores,explode=desfase)
    plt.savefig("static/Ejemplo4.jpg")
    plt.close()
    return render_template('index.html')    

@app.route("/contacto",methods=("POST","GET"))
def contactos():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=5432)
    app.run(debug=True)