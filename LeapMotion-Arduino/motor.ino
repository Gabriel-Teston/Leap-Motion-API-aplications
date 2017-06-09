#include <Servo.h>
#include <stdio.h>
 
#define SERVO1 6
#define SERVO2 7

Servo s1,s2;
String number,recieved;
boolean motor;
int angulo1,angulo2;


void setup() {
  s1.attach(SERVO1);
  s2.attach(SERVO2);
  Serial.begin(9600);
  s1.write(0);
  s2.write(0);
}

void loop() {
  while (Serial.available() > 0) {
    angulo1 = Serial.parseInt();
    angulo2 = Serial.parseInt();
    if (Serial.read() == '\n') {  
      s1.write(angulo1);
      s2.write(angulo2);
    }
  }
}
