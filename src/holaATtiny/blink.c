#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define DELAY 3000

void delay(int);


int en_delay = 0;
int times = 0;


ISR (PCINT_B_vect) {
  PORTB |= 0x08; _delay_ms(DELAY);
  PORTB &= ~0x08; _delay_ms(DELAY);
}

ISR (TIMER0_OVF_vect) {
  if (en_delay) times = times + 1;
  TIMSK  &= 0x00;
}


void setup() {
  DDRB   = 0x38; //Configuracion del puerto
  GIMSK  |= (1 << PCIE0);
  PCMSK  |= 0x01; 
  // Configuracion del timer
  TCCR0A |= 0x00; // modo normal
  TCCR0B |= 0b011; // prescala con 64
  TCNT0  &= 0x00; // Iniciar contador interno Timer0
  sei();
}

void delay(int overflows) {
  en_delay = 1;
  while (times<overflows) {
    TIMSK |= 0x02;
  }
  en_delay = 0;
  times = 0;
}


int main(void)
{
  setup();
  //Parpadear
  while (1) {
    PORTB |= 0x10; 
    delay(1000);
    PORTB &= ~0x10;
    delay(1000);
  }
}
