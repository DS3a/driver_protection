#include <Arduino.h>
#include <Servo.h>
#include <string.h>

using namespace std;

// parameters regarding sensor
#define TIME_DELAY 9
#define SOUND_SPEED 330 // meters per second
#define MAX_DIST 3 // meters

// pins on the arduino NANO
#define SERVO_PIN 3
#define TRIG_PIN 13
#define ECHO_PIN 12
#define LED_PIN 7


Servo servo;
void setup() {
  Serial.begin(9600);

  // Initializing the servo
  servo.attach(SERVO_PIN);

  //setting the pins values
  pinMode(LED_PIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

float get_distance() {
  float duration, distance;
  digitalWrite(TRIG_PIN, LOW);  // Added this line
  delayMicroseconds(2); // Added this line
  digitalWrite(TRIG_PIN, HIGH);
//  delayMicroseconds(1000); - Removed this line
  delayMicroseconds(10); // Added this line
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN, HIGH);
  duration /= 932156.1338; // converting the pulse duration to seconds. The value was determined experimentally
  distance = duration * SOUND_SPEED / 2;

  return distance;
}

void send_vals(int angle, float distance) {
  Serial.print("{");
  Serial.print(angle);
  Serial.print(",");
  Serial.print(distance);
  Serial.println("}");
}


void loop() {
  for (int angle=0; angle<=180; angle++) {
    servo.write(angle);
    double distance = get_distance();
//    double distance = get_dur();
    delay(TIME_DELAY);
    if (Serial.read())
      send_vals(angle, distance);
    if (distance <= 0.5) {  // This is where the LED On/Off happens
      digitalWrite(LED_PIN, HIGH); // When the Red condition is met, the Green LED should turn off
      continue;
    }else {
      digitalWrite(LED_PIN, LOW);
      continue;
    }

  }
  for (int angle=180; angle>=0; angle--) {
    servo.write(angle);
    double distance = get_distance();
//      double distance = get_dur();
    delay(TIME_DELAY);
    if (Serial.read())
      send_vals(angle, distance);
    if (distance <= 0.5)  {// This is where the LED On/Off happens
      digitalWrite(LED_PIN, HIGH); // When the Red condition is met, the Green LED should turn off
      continue;
    }else {
      digitalWrite(LED_PIN, LOW);
      continue;
    }
  }
}