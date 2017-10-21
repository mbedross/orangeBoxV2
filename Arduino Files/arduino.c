#include"arduinoHeader.h"

void setup() {

    // Begin serial comm. and establish digital outputs
    Serial.begin(9600);
  
    // Define all appropriate digital pins as input/output
    pinMode(tempPower, OUTPUT);
    pinMode(relayPump, OUTPUT);
    pinMode(relayV1, OUTPUT);
    pinMode(relayV2, OUTPUT);
    pinMode(relayV3, OUTPUT);
    pinMode(LED5, OUTPUT);
    pinMode(LED6, OUTPUT);
    pinMode(LED7, OUTPUT);
    pinMode(LED8, OUTPUT);
    pinMode(LED9, OUTPUT);
    
    // Make sure everything is off
    digitalWrite(tempPower, LOW);
    digitalWrite(relayPump, LOW);
    digitalWrite(relayV1, LOW);
    digitalWrite(relayV2, LOW);
    digitalWrite(relayV3, LOW);
    digitalWrite(LED5, LOW);
    digitalWrite(LED6, LOW);
    digitalWrite(LED7, LOW);
    digitalWrite(LED8, LOW);
    digitalWrite(LED9, LOW);
  
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
            case '2':
                // Call to turn pump on
                PUMP();
                break;
            case '3':
                // Call to turn valve 1 on/off
                digitalWrite(relayV1, !digitalRead(relayV1));
                break;
            case '4':
                // Call to turn valve 2 on/off
                digitalWrite(relayV2, !digitalRead(relayV2));
                break;
            case '5':
                // Call to turn valve 3 on/off
                digitalWrite(relayV3, !digitalRead(relayV3));
                break;
            case '6':
                // Call to turn LED5 on/off
                digitalWrite(LED5, !digitalRead(LED5));
                break;
            case '7':
                // Call to turn LED6 on/off
                digitalWrite(LED6, !digitalRead(LED6));
                break;
            case '8':
                // Call to turn LED7 on/off
                digitalWrite(LED7, !digitalRead(LED7));
                break;
            case '9':
                // Call to turn LED8 on/off
                digitalWrite(LED8, !digitalRead(LED8));
                break;
            case '10':
                // Call to turn LED9 on/off
                digitalWrite(LED9, !digitalRead(LED9));
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

void PUMP() {
    // Begin running pump while checking the serial port. If command to stop pump
    // is received, end while loop
    lock = 1;
    while (lock) {
        if (Serial.available() >0) {
            input = Serial.read();
            Serial.read();
            if (input = 'off') {
                lock = 0;
            }
        }
        digitalWrite(relayPump, HIGH);
        delay(100);
        digitalWrite(relayPump,LOW);
        delay(100)
    }
}