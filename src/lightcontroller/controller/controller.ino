/*
# Controller.ino
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
#
# Code on the arduino to receive commands from the monitor to turn on
# the strobe light.
*/

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
}

void loop() {
  while (Serial.available() > 0) {
    char incomingCharacter = Serial.read();
    switch (incomingCharacter) {
      case '+':
        Serial.println("ON");
        digitalWrite(2, HIGH);
        break;
      case '-':
        Serial.println("OFF");
        digitalWrite(2, LOW);
          break;
    }
  }
}
