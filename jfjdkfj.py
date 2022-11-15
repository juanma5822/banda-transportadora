import pandas as pd
from flask import Flask, redirect, url_for, request, json, render_template
import psycopg2
import matplotlib.pyplot as plt 
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
fig, ax = plt.subplots(1,2)
normdata= colors.Normalize(0, max(datos))
colormap = cm.get_cmap("Blues")
colores =colormap(normdata(datos))
ax[0].bar(ejex,datos)
ax[1].pie(datos,labels=ejex,autopct="%0.1f %%",colors=colores)
plt.savefig("static/Ejemplo2.jpg")