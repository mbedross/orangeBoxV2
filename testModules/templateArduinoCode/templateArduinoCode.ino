  #include <elapsedMillis.h>    // Import timekeeping library

  elapsedMillis timeElapsed;
  const int Pota = 2;           // Pumps 1 & 3 A
  const int Potb = 3;           // Pumps 1 & 3 B
  const int tWo = 7;            // 2-Way Valve 1
  boolean x = 0;                // While loop statement    
  char input = 0;               // Variable for Serial.read()
  

void setup() {

  // Begin serial comm. and establish digital outputs
  Serial.begin(9600);
  pinMode(Pota, OUTPUT);
  pinMode(Potb, OUTPUT);
  pinMode(tWo, OUTPUT);
  
  // Make sure everything is off
  digitalWrite(Pota,HIGH);
  digitalWrite(Potb,HIGH);
  digitalWrite(tWo,LOW);
  
  // Send a '0' over serial so computer knows arduino is ready
  Serial.println('0');

}

void loop() {
  
  x=1;
  while (x) {
    if (Serial.available() >0) {
      input = Serial.read();
      Serial.read();
    }
    switch (input) {
      case '1':
      pump();
      break;
      case '3':
      // Quit loop
      x = !x;
      break;
      case '2':
      stopp();
      break;
      default:
      break;
    }
    input = 0;
  }
}

void pump() {

    // Open two valve and turn on pumps
      analogWrite(tWo,179);
      timeElapsed = 0;
      digitalWrite(Pota,LOW);
      digitalWrite(Potb,LOW);
    // Tell computer the pump is on 'P'
      Serial.println("P");
 }

 void stopp() {

    // Tell computer how long pump was on
      // Serial.println(timeElapsed);
    // Close two way valve
      digitalWrite(tWo,LOW);
      digitalWrite(Pota,HIGH);
      digitalWrite(Potb,HIGH);
      delay(1000);
    // Tell computer it is ready for imaging 'S'
      Serial.println("S");
 }

