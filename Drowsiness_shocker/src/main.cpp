#include <Arduino.h>

#define RELAY_PIN 13
#define SHOCK_TIME 20


void setup() {
  Serial.begin(9600);

  pinMode(RELAY_PIN, OUTPUT);
}

void shock() {
  for (int i=0; i<2; i++) {
    digitalWrite(RELAY_PIN, LOW);
    delay(SHOCK_TIME);
    digitalWrite(RELAY_PIN, HIGH);
    delay(SHOCK_TIME);
  }
}


void loop() {
  char msg = Serial.read();

  if (msg) {
    if (msg == '1') {
      shock();
    }
    else {
    }
  }
}