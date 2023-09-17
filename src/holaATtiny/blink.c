#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

// parametros de tiempo
#define DELAY 1000

// Estados
#define veh_only  1
#define veh_adv   2
#define veh_stop  3
#define pers_only 4
#define pers_adv  5
#define pers_stop 6

// Funciones
void delay(int);
void setup();
// Variables de estado
int estado, sig_estado;
int tiempo  = 0;
int boton   = 0;
// Variables interrupciones
int en_delay = 0;
int times = 0;

// Interrupcion boton B0/B1
ISR (PCINT_B_vect) {
  boton  = 1;
  PCMSK  &= 0x00; 
}


// Interrupcion overflow Timer0
ISR (TIMER0_OVF_vect) {
  // Si se usa la funcion
  // delay se aumenta times
  // para contar el tiempo
  if (en_delay) times = times + 1;
  // Se desactiva la interrupcion
  // luego
  TIMSK  &= 0x00;
}


void setup() {
  // Pines B
  DDRB   = 0x38; //Configuracion del puerto
  // Pines D
  DDRD   = 0x1c;
  GIMSK  |= (1 << PCIE0);
  PCMSK  |= 0x03; 
  // Configuracion del timer
  TCCR0A |= 0x00; // modo normal
  TCCR0B |= 0b011; // prescala con 64
  TCNT0  &= 0x00; // Iniciar contador interno Timer0
  sei();
}

void delay(int overflows) {
  // se activa el delay de interrupcion
  en_delay = 1;
  // Loop hasta que transcurra overflows
  while (times<overflows) {
    // Se activa la interrupcion
    TIMSK |= 0x02;
  }
  // Se reinicia las variables
  en_delay = 0;
  times = 0;
}


int main(void)
{
  setup();
  //Parpadear
  sig_estado = veh_only;
  while (1) {
    // siguientes estados
    estado = sig_estado;


    switch (estado)
    {
      // # PRIMER ESTADO-------------
      // estado vehiculos solo
    case veh_only:
      // Se apagan todos las luces
      // excepto las del estado
      // si es que fueron prendidas
      PORTB &= 0x08;
      PORTD &= 0x04;
      // Si el tiempo pasado es menor a diez y el boton 
      // no ha sido presionado no se cambia de estado
      if (tiempo>=10 && boton==1) {
        sig_estado = veh_adv;
        tiempo = 0;
        boton  = 0;
        PCMSK  |= 0x03; 
      } 
      // Se prende luz roja y se va haciendo
      // delays de 1s hasta llegar a 10
      else
      {
        PORTB |= 0x08; 
        PORTD |= 0x04;
        delay(DELAY);
        tiempo++;
      }
      break;
      // # PRIMER ESTADO-------------


      // # SEGUNDO ESTADO-------------
      // estado vehiculo transicion
    case veh_adv:
      // Apagar luces que no
      // sean del estado
      PORTB &= 0x10;
      // Si el tiempo transcurrido fue de 3s
      // se va al siguiente estado
      if (tiempo>=3) {
        sig_estado = veh_stop;
        tiempo = 0;
      } 
      else
      {
        PORTB |= 0x10; 
        delay(DELAY/2);
        PORTB &= ~0x10;
        delay(DELAY/2);
        tiempo++;
      }
      break;
    // # SEGUNDO ESTADO-------------

    // # TERCER ESTADO--------------
    case veh_stop:
      // Se apagan todas las luces
      PORTB &= 0x00;
      // Se prende la señal de stop
      // para los vehiculos
      PORTB |= 0x20;
      // por un tiempo de 1 s
      delay(2 * DELAY);
      // se va directamente al
      // siguiente estado
      sig_estado = pers_only;
      break;
    // # TERCER ESTADO--------------

    // # CUARTO ESTADO--------------
    case pers_only:
      // Se apagan todas las luces
      // de peatones
      PORTD &= 0x00;
      // La verde para los
      // peatones
      PORTD |= 0x10;
      // por un tiempo de 10 s
      delay(10 * DELAY);
      sig_estado = pers_adv;

      break;


    // # CUARTO ESTADO--------------

    // # QUINTO ESTADO--------------
    case pers_adv:
      // Se apagan todas las luces
      // de peatones
      PORTD &= 0x00;

      // tiempo debe ser 3s
      if (tiempo>=3) {
        sig_estado = pers_stop;
        tiempo = 0;
      } 
      else {
        // Luz amarilla
        PORTD |= 0x08;
        delay(DELAY/2);
        PORTD &= ~0x08;
        delay(DELAY/2);
        tiempo++;
      }
      break;
    // # QUINTO ESTADO--------------

    // # SEXTO ESTADO--------------
    case pers_stop:
      // Se apagan todas las luces
      // de peatones
      PORTD &= 0x00;

      // Se prende rojo
      PORTD |= 0x04;
      // Se espera 1 segundo
      delay(2 * DELAY);
      // Estado se reinicia al inicio
      sig_estado = veh_only;
      break;
    // # SEXTO ESTADO--------------
    default:
      sig_estado = veh_only;
      break;
    }
  }
}
