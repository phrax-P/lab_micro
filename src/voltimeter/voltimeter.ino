#include <PCD8544.h>

static PCD8544 lcd;
float vCH1, vCH2, vCH3, vCH4 = {0.000};
const float referenceVoltage = 24.00;
#define converter 511.5

void setup() {
    Serial.begin(9600);
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
    
    attachInterrupt(digitalPinToInterrupt(2), clear_display, CHANGE);
    
    delay(2000);    
    
}

void clear_display() {
  lcd.clear();  
}

void serial_display(const char *MODO,
                    float vCH1,
                    float vCH2,
                    float vCH3,
                    float vCH4){
   float serial_en = analogRead(A4);
   
   if(serial_en > converter){
    Serial.println(MODO);
    Serial.println(vCH1);
    Serial.println(vCH2);
    Serial.println(vCH3);
    Serial.println(vCH4);}
  }

void lcd_display(const char *MODO,
                 float vCH1,
                 float vCH2,
                 float vCH3,
                 float vCH4) {
    lcd.setCursor(0, 0);
    lcd.print(MODO);
    
    lcd.setCursor(0, 1);
    lcd.print("CH1: ");
    lcd.print(vCH1);
    lcd.print("  ");

    lcd.setCursor(0, 2);
    lcd.print("CH2: ");
    lcd.print(vCH2);
    lcd.print("  ");
    
    lcd.setCursor(0, 3);
    lcd.print("CH3: ");
    lcd.print(vCH3);
    lcd.print("  ");

    lcd.setCursor(0, 4);
    lcd.print("CH4: ");
    lcd.print(vCH4);
    lcd.print("  ");
    
}


float get_RMS(int PIN){
  const int samples = 1000;
  float tmax = 0.00;
  float one_sqrt = 0.7071;

  for(int i = 0; i < samples; i++){
    float t = analogRead(PIN);
    if(t > tmax) tmax = t;
    }
    float t_rms = ((tmax - converter)*(referenceVoltage / converter));

    return t_rms * one_sqrt;
  }

void AC_mode(){
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
    lcd_display("MODO AC", vCH1, vCH2, vCH3, vCH4);
    
    serial_display("MODO AC",vCH1,vCH2,vCH3,vCH4);
  }

// Function to read and display DC mode
void DC_mode() {
    // Read the analog values from pins A0 to A3
    vCH1 = (analogRead(A0) - converter) * (referenceVoltage / converter);
    vCH2 = (analogRead(A1) - converter) * (referenceVoltage / converter);
    vCH3 = (analogRead(A2) - converter) * (referenceVoltage / converter);
    vCH4 = (analogRead(A3) - converter) * (referenceVoltage / converter);

    high_v_warming(
      vCH1,
      vCH2,
      vCH3,
      vCH4);

    lcd_display("MODO DC", vCH1, vCH2, vCH3, vCH4);

    serial_display("MODO DC",vCH1,vCH2,vCH3,vCH4);
}

void Switch_mode(){
  float button = analogRead(A5);

  if(button < converter){
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
}
