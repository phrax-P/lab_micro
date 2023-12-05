import pygame, sys, time
from pygame.locals import *
#import bluetooth as bt
import csv, serial
#Bluetooth
target_name = "My app"
target_address = None
port = 1




#def buscar_disp():
#	disp = bt.discover_devices()
#	for bdaddr in disp:
#		print(bdaddr)
#	return disp
#def conectar_disp(target_address):
#	for bdaddr in buscar_disp():
#		if target_name == bt.lookup_name( bdaddr ): 
#			target_address = bdaddr
#			break
#
#	if target_address is not None:
#		print ("found target bluetooth device with address ", target_address)
#		sock = bt.BluetoothSocket(bt.RFCOMM)
#		sock.connect((target_address, port))
#		sock.send("Conexion Exitosa!")
#	else:
#		print ("could not find target bluetooth device nearby")


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
	font = pygame.font.Font(None, 32)
	click = False
	msg = ""
	active = False
	txt = ""
	done = False
	color_inactive = pygame.Color('lightskyblue3')
	color_active = pygame.Color('dodgerblue2')
	color = color_inactive
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
	# input box
	input_box = pygame.Rect(float(ANCHO / 2 + 250),
                        	float(ALTURA / 2 - 100),
                        	100, 100)
	while True:
		screen.fill(pygame.Color("black"))
		txt_surface = font.render(txt, True, color)
		width = max(200, txt_surface.get_width()+10)
		input_box.w = width
		screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
		dibujar_pant(screen, color, input_box, 2)
    # Dibujar en la ventana
		draw_text('Menu', FONT, (255,255,255), screen, 412, 50)
		draw_text(msg, FONT, (255,255,255), screen, ANCHO/2, ALTURA/2)
		draw_text(str(time.localtime(time.time()).tm_sec), FONT, (255,100,100), screen, 50, 50)
		# Logica de clicks
		mx, my = pygame.mouse.get_pos()
		if click:
			msg = evento_boton(botton_up   	, mx, my, msg, "ARRIBA")
			msg = evento_boton(botton_dwn  	, mx, my, msg, "ABAJO")
			msg = evento_boton(botton_left 	, mx, my, msg, "IZQUIERDA")
			msg = evento_boton(botton_right	, mx, my, msg, "DERECHA")
			msg = evento_boton(botton_bt	, mx, my, msg, "BLUETOOTH")
			
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
				if input_box.collidepoint(event.pos):
					active = not active
				else:
					active = False
				color = color_active if active else color_inactive
			if event.type == MOUSEBUTTONUP:	
					click = False
			if event.type == pygame.KEYDOWN:
				if active:
					if event.key == pygame.K_RETURN:
						print(txt)
						txt = ''
					elif event.key == pygame.K_BACKSPACE:
						txt = txt[:-1]
					else:
						txt += event.unicode
			# Ventana dinamica
			if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
				surface = pygame.display.set_mode((event.w, event.h),
                                              	pygame.RESIZABLE)
		pygame.display.update()
		clock.tick(30)
    
main()
