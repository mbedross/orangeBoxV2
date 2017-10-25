#include"arduinoHeader.h"

void setup() {

    // Begin serial comm. and establish digital outputs
    Serial.begin(9600);
  
    // Define all appropriate digital pins as input/output
    pinMode(tempPower, OUTPUT);
    
    // Make sure everything is off
    digitalWrite(tempPower, LOW);
  
    float Temps[5];
    int Res[5];
    float steinhart;
    
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
                // Call to read temp sensors
                TEMP();
                break;
            default:
                break;
        }
    input = 0;
    }
}

void TEMP() {
    digitalWrite(tempPower, HIGH);
    delay(500)                     // Wait 500 ms for voltage to stabilize
    Res[0] = analogRead(temp1);
    Res[1] = analogRead(temp2);
    Res[2] = analogRead(temp3);
    Res[3] = analogRead(temp4);
    Res[4] = analogRead(temp5);
    digitalWrite(tempPower, LOW);
    
    // Calculate temperatures
    for (int i=0; i <= 4; i++){
        // Convert analog reading to resistance value
        res = (1023 / Res[i]) - 1;
        res = seriesRes / res;
        // Calculate temperature from res value
        steinhart = res / thermNom;     // (R/Ro)
        steinhart = log(steinhart);                  // ln(R/Ro)
        steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
        steinhart += 1.0 / (ambientTemp + 273.15); // + (1/To)
        steinhart = 1.0 / steinhart;                 // Invert
        steinhart -= 273.15; 
        Temps[i] = steinhart;
    }
    Serial.print(Temps); 
}