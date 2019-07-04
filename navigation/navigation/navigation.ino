#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

const uint8_t servoGripper = 0;
const uint8_t servoValve = 3;

const uint8_t servoFL = 12;
const uint8_t servoFR = 13;
const uint8_t servoBL = 14;
const uint8_t servoBR = 15;

/*
   Front left
   Min: 2 (backward)
   Mid: 372 (371-373)
   Max: ~1200 (forward)

   Front right
   Min: 2 (forward)
   Mid: 370 (368-371)
   Max: ~1500 (backward)

   Back left
   Min: 2 (backward)
   Mid: 376 (375-378)
   Max: ~1600 (forward)

   Back right
   Min: 2 (forward)
   Mid: 371 (369-373)
   Max: ~1700 (backward)
*/

const int midPointFL = 372;
const int midPointFR = 370;
const int midPointBL = 376;
const int midPointBR = 371;

String message = " ";
char initial = ' ';
int testedValue = 0;
int neutralSpeed = 150;

/*
   with neutralSpeed=150
   linearSpeed ~ 25 cm/s
   angularSpeed ~ 126 °/s
*/

float linearSpeed = 25.0;
float angularSpeed = 126.0;

void setup() {
  Serial.begin(9600);

  pwm.begin();
  pwm.setPWMFreq(60);

  pwm.setPWM(servoFL, 0, 0);
  pwm.setPWM(servoFR, 0, 0);
  pwm.setPWM(servoBL, 0, 0);
  pwm.setPWM(servoBR, 0, 0);
}

void loop() {
  if (Serial.available() > 0) {
    message = Serial.readString();
    initial = message.charAt(0);
    Serial.println(message);
    switch (initial) {
      case 'w':
        moveForward(getNumber(message));
        break;
      case 's':
        moveBackward(getNumber(message));
        break;
      case 'a':
        rotateCounterclockwise(getNumber(message));
        break;
      case 'd':
        rotateClockwise(getNumber(message));
        break;
      case 'e':
        stopAll();
        break;
    }
    initial = ' ';
    delay(10);
  }
}

int getNumber(String someString) {
  String numberString = someString.substring(1, someString.length());
  int number = numberString.toInt();
  return number;
}

void moveForward(int distanceToMove) {
  float correctedDistance;
  if(distanceToMove>3){
    correctedDistance = (float(distanceToMove)-3.8)/1.048;
  }
  else{
    correctedDistance=float(distanceToMove);
  } 
  int requiredTime = int(1000 * correctedDistance / linearSpeed);
  Serial.println(requiredTime);
  pwm.setPWM(servoFR, 0, midPointFR - neutralSpeed);
  pwm.setPWM(servoBR, 0, midPointBR - neutralSpeed);
  pwm.setPWM(servoBL, 0, midPointBL + neutralSpeed);
  pwm.setPWM(servoFL, 0, midPointFL + neutralSpeed);
  delay(requiredTime);
  stopAll();
}

void moveBackward(int distanceToMove) {
  float correctedDistance;
  if(distanceToMove>3){
    correctedDistance = (float(distanceToMove)-3.8)/1.048;
  }
  else{
    correctedDistance=float(distanceToMove);
  }
  int requiredTime = int(1000 * correctedDistance / linearSpeed);
  Serial.println(requiredTime);  stopAll();
  pwm.setPWM(servoFR, 0, midPointFR + neutralSpeed);
  pwm.setPWM(servoBR, 0, midPointBR + neutralSpeed);
  pwm.setPWM(servoBL, 0, midPointBL - neutralSpeed);
  pwm.setPWM(servoFL, 0, midPointFL - neutralSpeed);
  delay(requiredTime);
  stopAll();
}

void rotateClockwise(int degreesToRotate) {
  float correctedDistance;
  if(degreesToRotate>20){
    correctedDistance = (float(degreesToRotate)-20.52)/0.9691;
  }
  else{
    correctedDistance=float(degreesToRotate);
  }
  int requiredTime = int(1000 * correctedDistance / angularSpeed);
  Serial.println(requiredTime);
  pwm.setPWM(servoFR, 0, midPointFR + neutralSpeed);
  pwm.setPWM(servoBR, 0, midPointBR + neutralSpeed);
  pwm.setPWM(servoBL, 0, midPointBL + neutralSpeed);
  pwm.setPWM(servoFL, 0, midPointFL + neutralSpeed);
  delay(requiredTime);
  stopAll();
}

//For some reason, it moves faster counterclockwise
void rotateCounterclockwise(int degreesToRotate) {
  float correctedDistance;
  if(degreesToRotate>20){
    correctedDistance = float(degreesToRotate)-20.52;
  }
  else{
    correctedDistance=float(degreesToRotate);
  }
  int requiredTime = int(1000 * correctedDistance / angularSpeed);
  Serial.println(requiredTime);
  pwm.setPWM(servoFR, 0, midPointFR - neutralSpeed);
  pwm.setPWM(servoBR, 0, midPointBR - neutralSpeed);
  pwm.setPWM(servoBL, 0, midPointBL - neutralSpeed);
  pwm.setPWM(servoFL, 0, midPointFL - neutralSpeed);
  delay(requiredTime);
  stopAll();
}

void stopAll() {
  pwm.setPWM(servoFR, 0, 0);
  pwm.setPWM(servoBR, 0, 0);
  pwm.setPWM(servoBL, 0, 0);
  pwm.setPWM(servoFL, 0, 0);
  delay(10);
}
