#include <pic14/pic12f675.h>
 
//To compile:
//sdcc -mpic14 -p16f675 blink.c
 
//To program the chip using picp:
//Assuming /dev/ttyUSB0 is the serial port.
 
//Erase the chip:
//picp /dev/ttyUSB0 16f887 -ef
 
//Write the program:
//picp /dev/ttyUSB0 16f887 -wp blink.hex
 
//Write the configuration words (optional):
//picp /dev/ttyUSB0 16f887 -wc 0x2ff4 0x3fff
 
//Doing it all at once: erasing, programming, and reading back config words:
//picp /dev/ttyUSB0 16f887 -ef -wp blink.hex -rc
 
//To program the chip using pk2cmd:
//pk2cmd -M -PPIC16f887 -Fblink.hex
 
// Declarando valores del dado
int value[] = {0x1, 0x2, 0x3, 0x5, 0x7, 0x15};
int *ptr = value;
void delay (unsigned int tiempo);


void main(void)
{

    TRISIO = 0b00001000; //Poner todos los pines como salidas
	GPIO = 0x00; //Poner pines en bajo
 
    unsigned int time = 100;
    int random = 1;
    //Loop forever
    while ( 1 )
    {		

		if (!GP3) 
		{
			// Escribimos en los pines 
			//GPIO |= value[random-1];
			switch (random) 
			{
				case 1:
					GPIO |= value[0];
					break;
				case 2:
					GPIO |= value[1];
					break;
				case 3:
					GPIO |= value[2];
					break;
				case 4:
					GPIO |= value[3];
					break;
				case 5:
					GPIO |= value[4];
					break;
				case 6:
					GPIO |= value[5];
					break;
				default:
					GPIO &= 0x00;
			}	
			// delay para ver el valor
			delay(time);
			// Reiniciar pines
			GPIO &= 0x00;
		} 
		else {
		// Si random mayor a 6, se reinicia
		// de lo contrario de suma uno
		
		random = (random>6) ? 0 : random;
		random++;
		
		}
	}
	
}

void delay(unsigned int tiempo)
{
	unsigned int i;
	unsigned int j;

	for(i=0;i<tiempo;i++)
	  for(j=0;j<1275;j++);
}




