// This is a header file to be included when compiling the arduino code for holOS
//
// A separate arduino code is needed because the IMX6 processor on the UDOO x86
// doesn't directly communicate to the Arduino pins on the UDOO, but relies on a
// separate Intel Curie processor to run the Arduino pins

int temp5 = 0;
int temp4 = 1;
int temp3 = 2;
int temp2 = 3;
int temp1 = 4;
int diodeC = 5;
int tempPower = 2;
int relayPump = 3;
int relayV1 = 4;
int relayV2 = 5;
int relayV3 = 6;
int LED5 = 7;
int LED6 = 8;
int LED7 = 9;
int LED8 = 10;
int LED9 = 11;
#define seriesRes 10000
#define thermNom 10000
#define BCOEFFICIENT 3740
#define ambientTemp 25
