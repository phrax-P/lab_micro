#include <PCD8544.h>

static PCD8544 lcd;
float vCH1, vCH2, vCH3, vCH4 = {0.000};
const float referenceVoltage = 24.00;

void setup() {
    pinMode(8, OUTPUT);
    pinMode(9, OUTPUT);
    pinMode(10, OUTPUT);
    pinMode(11, OUTPUT);
    lcd.begin(84, 48);

    lcd.clear();
    lcd.setCursor(1,0);
    lcd.print("Welcome to");
    lcd.setCursor(1,1);
    lcd.print("4 Channel");
    lcd.setCursor(1,2);
    lcd.print("Voltimeter!");
    delay(5000);    
}

float get_RMS(int PIN){
  const int samples = 1000;
  float tmax = 0.00;
  float one_sqrt = 0.7071;

  for(int i = 0; i < samples; i++){
    float t = analogRead(PIN);
    if(t > tmax) tmax = t;
    }
    float t_rms = ((tmax - 512)*(referenceVoltage / 512));

    return t_rms * one_sqrt;
  }

void AC_mode(){
    lcd.clear(); // Borrar la pantalla
    lcd.setCursor(0, 0);
    lcd.print("MODO AC");
    lcd.print("(V)");

    // Calcular la tensión RMS para cada canal
    vCH1 = get_RMS(A0);
    vCH2 = get_RMS(A1);
    vCH3 = get_RMS(A2);
    vCH4 = get_RMS(A3);

    high_v_warming(
      vCH1 * 1.41,
      vCH2 * 1.41,
      vCH3 * 1.41,
      vCH4 * 1.41);

    // Mostrar los valores en la pantalla
    lcd.setCursor(0, 1);
    lcd.print("CH1 RMS: ");
    lcd.print(vCH1);

    lcd.setCursor(0, 2);
    lcd.print("CH2 RMS: ");
    lcd.print(vCH2);

    lcd.setCursor(0, 3);
    lcd.print("CH3 RMS: ");
    lcd.print(vCH3);

    lcd.setCursor(0, 4);
    lcd.print("CH4 RMS: ");
    lcd.print(vCH4);
  }

// Function to read and display DC mode
void DC_mode() {
    lcd.clear(); // Clear the LCD
    lcd.setCursor(0, 0);
    lcd.print("MODO DC");

    // Read the analog values from pins A0 to A3
    vCH1 = (analogRead(A0) - 512) * (referenceVoltage / 512.0);
    vCH2 = (analogRead(A1) - 512) * (referenceVoltage / 512.0);
    vCH3 = (analogRead(A2) - 512) * (referenceVoltage / 512.0);
    vCH4 = (analogRead(A3) - 512) * (referenceVoltage / 512.0);

    high_v_warming(
      vCH1,
      vCH2,
      vCH3,
      vCH4);

    // Display the values on the LCD
    lcd.setCursor(0, 1);
    lcd.print("CH1: ");
    lcd.print(vCH1);

    lcd.setCursor(0, 2);
    lcd.print("CH2: ");
    lcd.print(vCH2);

    lcd.setCursor(0, 3);
    lcd.print("CH3: ");
    lcd.print(vCH3);

    lcd.setCursor(0, 4);
    lcd.print("CH4: ");
    lcd.print(vCH4);
}

void Switch_mode(){
  float button = analogRead(A5);

  if(button < 512){
    AC_mode();
  } else DC_mode();
}

void high_v_warming(float vCH1,
                    float vCH2,
                    float vCH3,
                    float vCH4){
  if(vCH1 > 20.00 || vCH1 < -20.00) digitalWrite(8, HIGH);
  else digitalWrite(8, LOW);

  if(vCH2 > 20.00 || vCH2 < -20.00) digitalWrite(9, HIGH);
  else digitalWrite(9, LOW);

  if(vCH3 > 20.00 || vCH3 < -20.00) digitalWrite(10, HIGH);
  else digitalWrite(10, LOW);

  if(vCH4 > 20.00 || vCH4 < -20.00) digitalWrite(11, HIGH);
  else digitalWrite(11, LOW);
  }

void loop() {
    Switch_mode();
    delay(2000); 
}
