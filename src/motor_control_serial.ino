// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!

#include <AFMotor.h>
char direccion;

AF_DCMotor motor(1);
AF_DCMotor motor2(4);


void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("READY to Drive");


  motor.run(RELEASE);
  motor2.run(RELEASE);
}

void loop() {
  
  if(Serial.available() > 0){
    direccion = Serial.read();
    if(direccion == 'F'){
      Stop();
      forward();
      }
    else if(direccion == 'B'){
      Stop();
      back();
      }
    else if(direccion == 'L'){
      Stop();
      left();
      }
    else if(direccion == 'R'){
      Stop();
      right();  
    }
    else if(direccion == 'S'){
      Stop();
    }
    }
  }


 void forward()
{
  motor.setSpeed(255); 
  motor.run(FORWARD); 
  motor2.setSpeed(255);
  motor2.run(FORWARD);
}

void back()
{
  motor.setSpeed(255); 
  motor.run(BACKWARD); 
  motor2.setSpeed(255); 
  motor2.run(BACKWARD); 
}

void left()
{
  motor2.setSpeed(255); 
  motor2.run(FORWARD); 
}

void right()
{
  motor.setSpeed(255); 
  motor.run(FORWARD); 
}

void Stop()
{
  motor.setSpeed(0); 
  motor.run(RELEASE); 
  motor2.setSpeed(0); 
  motor2.run(RELEASE); 
}
