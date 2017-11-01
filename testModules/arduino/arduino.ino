#include"arduinoHeader.h"

void setup() {

    // Begin serial comm. and establish digital outputs
    Serial.begin(19200);

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

    int x;

    // Send a '0' over serial so computer knows arduino is ready
    Serial.println('0');

}

void loop() {
    String content = "";
    char character;
    int x = 1;
    int input;
    int action;
    while (x) {

        while(Serial.available()) {
            character = Serial.read();
            content.concat(character);
        }
        input = content.toInt();
        content = "";

        if (input == 20) {
            // Call to read temp sensors
            TEMP();
        }

        if (input >= 30 && input < 40) {
            action = input - 30;
            if (action == 1) {
                // Call to turn pump on
                PUMP();
            }
            if (action == 2) {
                Serial.println(digitalRead(relayPump));
            }
        }

        if (input >= 40 && input < 50) {
            action = input - 40;
            if (action == 0) {
                // Call to turn valve 1 off (OPEN)
                digitalWrite(relayV1, LOW));
                Serial.println(input);
            }
            if (action == 1) {
                // Call to turn valve 1 on (CLOSE)
                digitalWrite(relayV1, HIGH));
                Serial.println(input);
            }
            if (action == 2) {
                Serial.println(digitalRead(relayV1));
            }
        }

        if (input >= 50 && input < 60) {
            action = input - 50;
            if (action == 0) {
                // Call to turn valve 2 off (OPEN)
                digitalWrite(relayV2, LOW));
                Serial.println(input);
            }
            if (action == 1) {
                // Call to turn valve 2 on (CLOSE)
                digitalWrite(relayV2, HIGH));
                Serial.println(input);
            }
            if (action == 2) {
                Serial.println(digitalRead(relayV2));
            }
        }

        if (input >= 60 && input < 70) {
            action = input - 60;
            if (action == 0) {
                // Call to turn valve 3 off (OPEN)
                digitalWrite(relayV3, LOW));
                Serial.println(input);
            }
            if (action == 1) {
                // Call to turn valve 3 on (CLOSE)
                digitalWrite(relayV3, HIGH));
                Serial.println(input);
            }
            if (action == 2) {
                Serial.println(digitalRead(relayV3));
            }
        }

        if (input >= 70 && input < 80) {
            action = input - 70;
            if (action == 0) {
                // Call to turn LED5 off
                digitalWrite(LED5, LOW);
                Serial.println(input);
            }
            if (action == 1) {
                // Call to turn LED5 on
                digitalWrite(LED5, HIGH);
                Serial.println(input);
            }
            if (action == 2) {
                Serial.println(digitalRead(LED5));
            }
        }

        if (input >= 80 && input < 90) {
            action = input - 80;
            if (action == 0) {
                // Call to turn LED6 off
                digitalWrite(LED6, LOW);
                Serial.println(input);
            }
            if (action == 1) {
                // Call to turn LED6 on
                digitalWrite(LED6, HIGH);
                Serial.println(input);
            }
            if (action == 2) {
                Serial.println(digitalRead(LED6));
            }
        }

        if (input >= 90 && input < 100) {
            action = input - 90;
            if (action == 0) {
                // Call to turn LED7 off
                digitalWrite(LED7, LOW);
                Serial.println(input);
            }
            if (action == 1) {
                // Call to turn LED7 on
                digitalWrite(LED7, HIGH);
                Serial.println(input);
            }
            if (action == 2) {
                Serial.println(digitalRead(LED7));
            }
        }

        if (input >= 100 && input < 110) {
            action = input - 100;
            if (action == 0) {
                // Call to turn LED8 off
                digitalWrite(LED8, LOW);
                Serial.println(input);
            }
            if (action == 1) {
                // Call to turn LED8 on
                digitalWrite(LED8, HIGH);
                Serial.println(input);
            }
            if (action == 2) {
                Serial.println(digitalRead(LED8));
            }
        }

        if (input >= 110 && input < 120) {
            action = input - 110;
            if (action == 0) {
                // Call to turn LED9 off
                digitalWrite(LED9, LOW);
                Serial.println(input);
            }
            if (action == 1) {
                // Call to turn LED9 on
                digitalWrite(LED9, HIGH);
                Serial.println(input);
            }
            if (action == 2) {
                Serial.println(digitalRead(LED9));
            }
        }

        if (input == 1) {
            // Call to turn all digital pins off
            for (byte i = 0; i < pinCount; i++) {
                digitalWrite(pin[i], LOW);
            }
        }
        input = 0;
    }
}

void TEMP() {
    float Temps[5];
    float steinhart;
    float Res[5];
    float res;
    digitalWrite(tempPower, HIGH);
    delay(500);                     // Wait 500 ms for voltage to stabilize
    Res[0] = analogRead(temp1);
    Res[1] = analogRead(temp2);
    Res[2] = analogRead(temp3);
    Res[3] = analogRead(temp4);
    Res[4] = analogRead(temp5);
    digitalWrite(tempPower, LOW);

    // Calculate temperatures
    for (int i=0; i <= 4; i++) {
        // Convert analog reading to resistance value
        res = (1023 / Res[i]) - 1;
        res = seriesRes * res;
        // Calculate temperature from res value
        steinhart = res / thermNom;                    // (R/Ro)
        steinhart = log(steinhart);                    // ln(R/Ro)
        steinhart /= BCOEFFICIENT;                     // 1/B * ln(R/Ro)
        steinhart += 1.0 / (ambientTemp + 273.15);     // + (1/To)
        steinhart = 1.0 / steinhart;                   // Invert
        steinhart -= 273.15;
        Temps[i] = steinhart;
    }

    for (int i = 0; i <= 4; i++) {
        Serial.println(Temps[i]);
    }
}

void PUMP() {
    // Begin running pump while checking the serial port. If command to stop pump
    // is received, end while loop
    // Remember valve 1 and 2 states before pumping
    int v1;
    int v2;
    v1 = digitalRead(relayV1);
    v2 = digitalRead(relayV2);
    // Make sure Valves 1 and 2 are open
    digitalWrite(relayV1, LOW);
    digitalWrite(relayV2, LOW);
    delay(500);
    Serial.println("Pump is on");
    String content = "";
    char character;
    int lock = 1;
    int input;
    while (lock) {
        while(Serial.available()) {
            character = Serial.read();
            content.concat(character);
        }
        input = content.toInt();
        content = "";
        if (input == 2) {
            break;
        }
        delay(100);
        digitalWrite(relayPump, HIGH);
        delay(100);
        digitalWrite(relayPump,LOW);
    }
    Serial.println("Pump is off");
    delay(500);
    // Revert valves back to original state before pumping
    digitalWrite(relayV1, v1);
    digitalWrite(relayV2, v2);
}