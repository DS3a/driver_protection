#include <Arduino.h>
#include <Servo.h>

// parameters regarding sensor
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

double get_distance() {
  double duration, distance;
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


void loop() {
  for (int angle=0; angle<=180; angle++) {
    servo.write(angle);
    double distance = get_distance();
//    double distance = get_dur();
    if (Serial.read()) {
      Serial.print("{");
      Serial.print(180-angle);
      Serial.print(":");
      Serial.print(distance);
      Serial.println("}");
    }
    delay(9);
    if (distance <= 0.5)  // This is where the LED On/Off happens
      digitalWrite(LED_PIN, HIGH); // When the Red condition is met, the Green LED should turn off
    else
      digitalWrite(LED_PIN, LOW);
      

  }
  for (int angle=180; angle>=0; angle--) {
    servo.write(angle);
    double distance = get_distance();
//      double distance = get_dur();
    if (Serial.read()) {
      Serial.print("{");
      Serial.print(180-angle);
      Serial.print(":");
      Serial.print(distance);
      Serial.println("}");
    }
    delay(9);
    if (distance <= 0.5)  // This is where the LED On/Off happens
      digitalWrite(LED_PIN, HIGH); // When the Red condition is met, the Green LED should turn off
    else
      digitalWrite(LED_PIN, LOW); 
  }
}