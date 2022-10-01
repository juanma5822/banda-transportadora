from flask import Flask, redirect, url_for, request, json, render_template
import psycopg2
import RPi.GPIO as GPIO
from time import sleep



boton=4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


GPIO.setup(boton, GPIO.IN)

app = Flask(__name__)

try:
#conexion base de datos
 conexion=psycopg2.connect(user='xxbafeigeplqzf',
                          password='292103424cc1246aebe3a724ba93b366f7bcb06ae9d2c700b1cfd305b03e6d80',
                          host='ec2-34-227-120-79.compute-1.amazonaws.com',
                          port=5432,
                          database='d4reu6rdlo91uc')


 cursor=conexion.cursor()

 sql='INSERT INTO datosrecibidos (caja_grande,caja_pequeña) VALUES (%s,%s)'
 print('base conectada')
except:
 print('no se conecto')


@app.route("/")
def Home():
    return 'desplegado'


@app.route("/get")
def index():
    cursor
    sql1=("SELECT * FROM datosrecibidos ") 
    cursor.execute(sql1)
    data = cursor.fetchall()
    response = data
    return(json.dumps(response))

if __name__ == '__main__':
    app.run(port=5432)

while(True):

    datos=(caja_grande,caja_pequeña)

    cursor.execute(sql,datos)

    #guardar registro
    conexion.commit()

    #registro insertado
    registros=cursor.rowcount

    #mostra mensaje
    print(f'registro insertado: {registros}')