from flask import Flask, redirect, url_for, request, json, render_template
import psycopg2
import RPi.GPIO as GPIO
from time import sleep


#Entradas
sensor1 = 23
sensor2 = 24
GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
#Salidas 
motor_banda = 18
servo1 = 5
servo2 = 6
motor_caja_grande = 22
motor_caja_pequena = 27
GPIO.setup(motor_banda, GPIO.OUT)
GPIO.setup(motor_caja_grande, GPIO.OUT)
GPIO.setup(motor_caja_pequena, GPIO.OUT)
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
#Configuracion de alertar y modo
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

serv1 = GPIO.PWM(servo1, 50) # GPIO 17 for PWM with 50Hz
serv2 = GPIO.PWM(servo2, 50) # GPIO 17 for PWM with 50Hz
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


caja_grande_contador = 0
caja_pequena_contador = 0


while(True):

    caja_grande = 0
    caja_pequena = 0
    # Se inicia Banda Transportadora
    GPIO.output(motor_banda,True)
    #Cajas Grandes
    if GPIO.input(sensor1) and GPIO.input(sensor2):
        
        serv1.start(2.5)
        serv1.ChangeDutyCycle(5)
        caja_grande = 1
        caja_grande_contador +=1
    #Cajas pequeñas    
    elif  GPIO.input(sensor1) and GPIO.input(sensor2) ==False:
        serv1.stop()
        serv2.ChangeDutyCycle(12.5)
        caja_pequena = 1
        caja_pequena_contador +=1
    else:
        serv1.stop()
        serv2.stop()

    #Contar cajas grandes y comprimirlas
    if caja_grande_contador == 5:
        GPIO.output(motor_caja_grande, True)
        sleep(5)
        GPIO.output(motor_caja_grande, True)
        sleep(5)
        caja_grande_contador = 0
    #Contar cajas pequenas y comprimirlas    
    elif caja_pequena_contador == 5:
        GPIO.output(motor_caja_pequena, True)
        sleep(5)
        GPIO.output(motor_caja_pequena, True)
        sleep(5)
        caja_pequena_contador = 0
    else:
        GPIO.output(motor_caja_grande, False)
        GPIO.output(motor_caja_pequena, False)


    datos=(caja_grande,caja_pequena)

    cursor.execute(sql,datos)

    #guardar registro
    conexion.commit()

    #registro insertado
    registros=cursor.rowcount

    #mostra mensaje
    print(f'registro insertado: {registros}')