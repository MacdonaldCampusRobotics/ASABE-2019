#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

const uint8_t servoGripper = 3;
const uint8_t servoValve = 0;

uint8_t servoFL = 12;
uint8_t servoFR = 13;
uint8_t servoBL = 14;
uint8_t servoBR = 15;

/*
 * Front left
 * Min: 2 (backward)
 * Mid: 372 (371-373)
 * Max: ~1200 (forward)
 * 
 * Front right
 * Min: 2 (forward)
 * Mid: 370 (368-371)
 * Max: ~1500 (backward)
 * 
 * Back left
 * Min: 2 (backward)
 * Mid: 376 (375-378)
 * Max: ~1600 (forward)
 * 
 * Back right
 * Min: 2 (forward)
 * Mid: 371 (369-373)
 * Max: ~1700 (backward)
 */

const int midPointFL = 372;
const int midPointFR = 370;
const int midPointBL = 376;
const int midPointBR = 371;
const int opengripper = 130;
const int closegripper = 190;
const int openball = 260;
const int closeball= 470;

const char MOVE_FORWARD = 'w';
const char MOVE_BACK = 's';
const char MOVE_LEFT = 'a';
const char MOVE_RIGHT = 'd';
const char FULL_STOP = 'e';
const char OPEN_GRIPPER = 'b';
const char CLOSE_GRIPPER = 'c';
const char OPEN_BALL = 'f';
const char CLOSE_BALL = 'h';

String message = " ";
char initial = ' ';
int testedValue = 0;
int neutralSpeed = 150;

/*
 * with neutralSpeed=150
 * linearSpeed ~ 25 cm/s
 * angularSpeed ~ 126 °/s
 */

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

      // press w to move forward
      case MOVE_FORWARD:
        pwm.setPWM(servoFR, 0, midPointFR-neutralSpeed);
        pwm.setPWM(servoBR, 0, midPointBR-neutralSpeed);
        pwm.setPWM(servoBL, 0, midPointBL+neutralSpeed);
        pwm.setPWM(servoFL, 0, midPointFL+neutralSpeed);
        Serial.println("move forward");
        break;
      // press s to move backward
      case MOVE_BACK:
        pwm.setPWM(servoFR, 0, midPointFR+neutralSpeed);
        pwm.setPWM(servoBR, 0, midPointBR+neutralSpeed);
        pwm.setPWM(servoBL, 0, midPointBL-neutralSpeed);
        pwm.setPWM(servoFL, 0, midPointFL-neutralSpeed);
        Serial.println("move back");
        break;
      // press a to turn left
      case MOVE_LEFT:
        pwm.setPWM(servoFR, 0, midPointFR-neutralSpeed);
        pwm.setPWM(servoBR, 0, midPointBR-neutralSpeed);
        pwm.setPWM(servoBL, 0, midPointBL-neutralSpeed);
        pwm.setPWM(servoFL, 0, midPointFL-neutralSpeed);
        Serial.println("move left");
        break;
      // press d to turn right
      case MOVE_RIGHT:
        pwm.setPWM(servoFR, 0, midPointFR+neutralSpeed);
        pwm.setPWM(servoBR, 0, midPointBR+neutralSpeed);
        pwm.setPWM(servoBL, 0, midPointBL+neutralSpeed);
        pwm.setPWM(servoFL, 0, midPointFL+neutralSpeed);
        Serial.println("move right");
        break;
      //press b to open gripper
      case OPEN_GRIPPER: 
        pwm.setPWM(servoGripper, 0, opengripper);
        Serial.println("open gripper");
        break;
      //press c to close gripper 
      case CLOSE_GRIPPER:
        pwm.setPWM(servoGripper, 0, closegripper);
        Serial.println("close gripper");
        break;
      //press f to open ball 
      case OPEN_BALL:      
        pwm.setPWM(servoValve, 0, openball);
        Serial.println("open ball");
        break;
      //press b to close ball
      case CLOSE_BALL:
        pwm.setPWM(servoValve, 0, closeball);
        Serial.println("close ball");
        break; 
      // press e to default stop
      case FULL_STOP:
        stopAll();
        Serial.println("full stop");
        break;
      // press t to test just front left motor
      case 't':
        testedValue = getNumber(message);
        pwm.setPWM(servoFL, 0, testedValue);
        Serial.println("tried " + String(testedValue));
        break;
      // press u to test just the front right motor
      case 'u':
        testedValue = getNumber(message);
        pwm.setPWM(servoFR, 0, testedValue);
        Serial.println("tried " + String(testedValue));
        break;
      // press g to test just the back left motor
      case 'g':
        testedValue = getNumber(message);
        pwm.setPWM(servoBL, 0, testedValue);
        Serial.println("tried " + String(testedValue));
        break;
      // press j to test the back right motor
      case 'j':
        testedValue = getNumber(message);
        pwm.setPWM(servoBR, 0, testedValue);
        Serial.println("tried " + String(testedValue));
        break;
      // press p to stop all
      case 'p':
        stopAll();
        Serial.println("finished");
        Serial.end();
    }
  }
  initial = ' ';
  delay(10);
}

int getNumber(String someString) {
  String numberString = someString.substring(1, someString.length());
  int number = numberString.toInt();
  return number;
}

void stopAll() {
  pwm.setPWM(servoFR, 0, 0);
  pwm.setPWM(servoBR, 0, 0);
  pwm.setPWM(servoBL, 0, 0);
  pwm.setPWM(servoFL, 0, 0);
}
