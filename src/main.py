import pygame, sys, time, random
from pygame.locals import *
import csv, serial, json
import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
#CLIENT METHODS
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, msg):
	msg = f"messages: {msg}"
	result = client.publish(topic, msg)
	# result: [0, 1]
	status = result[0]
	if status == 0:
		print(f"Send `{msg}` to topic `{topic}`")
	else:
		print(f"Failed to send message to topic {topic}")
        

def on_connect(client, userdata, flags, rc):
    if not rc:
        client.is_connected = True
        print('Connection established. Working')
    else:
        print('Connection Faild', rc)
        client.loop_stop()

def on_disconnect(client, userdata, rc):
    if(rc == 0):
        print("Client disconneted OK")
    else:
        print("System disconnected via code: ", rc)

def on_log(client, userdata, level, buf):
   print(buf) 

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)


#SETUP
broker = 'broker.emqx.io'
port = 1883
topic = "carrito"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

client = connect_mqtt()

#SETUP
client2 = mqtt.Client('B928611')
client2.on_connect    = on_connect
client2.on_disconnect = on_disconnect
client2.on_publish    = on_publish 
client2.on_log        = on_log
client2.is_connected  = False
port        =   1883
broker      =   "iot.eie.ucr.ac.cr"
topic2       =   "v1/devices/me/telemetry" 
username    =   'C08592/B92861'
password    =   'brjxmov6h994bpdea2fr'
client2.username_pw_set(password)
client2.connect(broker, port)
client2.setKeepAlive(15)
while not client2.is_connected: 
    client2.loop()
    time.sleep(0.5)

# Parametros
ANCHO = 800
ALTURA = 600
NOMBRE_VENTANA = "Interfaz"
FONT_SIZE = 25
# INICIAMOS PYGAME
pygame.init()
# Fotogramas por segundo
clock = pygame.time.Clock()
# Nombre de nuestra ventana
pygame.display.set_caption(NOMBRE_VENTANA)
# Dimensiones de la ventana
screen = pygame.display.set_mode((ANCHO, ALTURA), pygame.RESIZABLE)
#Fuente de las letras
FONT = pygame.font.SysFont(None, FONT_SIZE)


# Metodo escribir texto en ventana
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    
#funcion para crear botones
def dibujar_boton(nombre, coor_x, coor_y, constante):
    boton = pygame.image.load(nombre).convert()
    boton.set_colorkey([255, 255, 255])
    boton = pygame.transform.scale(boton,
                                   (220 + constante // 2, 85 + constante // 2))
    screen.blit(boton, [(ANCHO / 2 - coor_x - constante // 4),
                        (ALTURA / 2 - coor_y - constante // 4)])

#funcion para dibujar en pantalla
def dibujar_pant(screen, color, objeto, optional=0):
    pygame.draw.rect(screen, color, objeto, optional)


# funcion animar boton
def evento_boton(boton, mx, my, msg, new_msg):
	if boton.collidepoint((mx, my)):
		dibujar_pant(screen, (255, 255, 0), boton)
		return new_msg
	else:
		dibujar_pant(screen, (255, 0, 0), boton)
	return msg
def main():
	click = False
	msg = ""
	start_time = time.localtime(time.time()).tm_sec
	# Creamos los botones
	botton_up = pygame.Rect(float(ANCHO / 2 - 50),
                           	float(ALTURA / 2 - 200),
                           	100, 100)
	botton_dwn = pygame.Rect(float(ANCHO / 2 - 50),
                        	float(ALTURA / 2 + 100),
                        	100, 100)
	botton_left = pygame.Rect(float(ANCHO / 2 + 100),
                        	float(ALTURA / 2 - 50),
                        	100, 100)
	botton_right = pygame.Rect(float(ANCHO / 2 - 200),
                        	float(ALTURA / 2 - 50),
                        	100, 100)
	botton_bt = pygame.Rect(float(ANCHO / 2 - 300),
                        	float(ALTURA / 2 + 100),
                        	100, 100)
	while True:
		screen.fill(pygame.Color("black"))
    # Dibujar en la ventana
		draw_text('Menu', FONT, (255,255,255), screen, 412, 50)
		draw_text(msg, FONT, (255,255,255), screen, ANCHO/2, ALTURA/2)
		draw_text(str(time.localtime(time.time()).tm_sec), FONT, (255,100,100), screen, 50, 50)
		# Logica de clicks
		mx, my = pygame.mouse.get_pos()
		if click:	
			msg_ant = msg
			msg = evento_boton(botton_up   	, mx, my, msg, "ARRIBA")
			msg = evento_boton(botton_dwn  	, mx, my, msg, "ABAJO")
			msg = evento_boton(botton_left 	, mx, my, msg, "IZQUIERDA")
			msg = evento_boton(botton_right	, mx, my, msg, "DERECHA")
			msg = evento_boton(botton_bt	, mx, my, msg, "STOP")
			if (msg!=msg_ant):
				publish(client, msg)
				client2.publish(topic2, json.dumps({"mensaje": msg}))
    
			if botton_bt.collidepoint((mx, my)):
				dibujar_pant(screen, (255, 255, 0), botton_bt)
				#conectar_disp(target_addr)
			else:
				dibujar_pant(screen, (255, 0, 0), botton_bt)
		else:
			dibujar_pant(screen, (255, 0, 0), botton_up		)
			dibujar_pant(screen, (255, 0, 0), botton_dwn	)
			dibujar_pant(screen, (255, 0, 0), botton_left	)
			dibujar_pant(screen, (255, 0, 0), botton_right	)
			dibujar_pant(screen, (255, 0, 0), botton_bt		)

			#publish(client, "STOP")
			click = False
  
		# Eventos
		for event in pygame.event.get():
			# Si es una tecla y es Esc
			# cierre todo
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			# Si es un click del mouse izquierdo
			# click se vuelve true
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == MOUSEBUTTONUP:
					click = False
					msg = ""
			# Ventana dinamica
			if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
				surface = pygame.display.set_mode((event.w, event.h),
                                              	pygame.RESIZABLE)
		pygame.display.update()
		clock.tick(30)
		#client.loop()
main()
