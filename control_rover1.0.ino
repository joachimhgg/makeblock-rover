
#include <SoftwareSerial.h>
#include "MeMegaPiPro.h"


MeSmartServo mysmartservo(PORT5);   //UART2 is on port 5 

//materials declarations
MeMegaPiDCMotor motor1(PORT1B); //right front wheel
MeMegaPiDCMotor motor2(PORT2B); // right back wheel
MeMegaPiDCMotor motor3(PORT3B); // left front wheel
MeMegaPiDCMotor motor4(PORT4B); // left back wheel
MeRGBLed led(PORT_9);

//prototypes
//void serialEvent();
//int Mouvement(int, uint8_t);
//String getValue(String data, char separator, int index);
//void Sending(int ValueToSend[]);
//void Received();

//global variables
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

// the following variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long lastDebounceTime = 50;  // the last time the output pin was toggled
long debounceDelay = 50;    // the debounce time; increase if the output flickers

String lastState="";
boolean chflag = false;

void setup() {
  
  TCCR1A = _BV(WGM10);//timer1 will be set to 490hz in setup function
  TCCR1B = _BV(CS11) | _BV(CS10) | _BV(WGM12);//970hz

  Serial.begin(115200);
  mysmartservo.begin(115200);
  delay(5);
  mysmartservo.assignDevIdRequest();
  delay(50);

  // reserve 200 bytes for the inputString:
  inputString.reserve(20);

  mysmartservo.moveTo(1,-70,50);   //device ID, angle, speed;  absolute angle move;
  mysmartservo.moveTo(2,20,50);
  led.setColorAt(0, 0, 64, 0);
  led.show();

}

void loop() {
 
   // for less latency better to use a hardware interrupt

   //add here as many value as you want to send
  long int ValueToSend[] = {mysmartservo.getAngleRequest(1), mysmartservo.getAngleRequest(2)};
  
  Sending(ValueToSend,sizeof(ValueToSend)/sizeof(ValueToSend[0]));
  Received(); 

}

void Received(){ //function to receive value from python FORMAT : S,1,50,50. <=> servo, servo1, angle=50, speed=50 and M,F,100 <=> motor,forward,speed=100

  // print the string when a newline arrives:
  if (stringComplete) {
    String material = getValue(inputString, ',', 0) ; //S = servo, M = motors
    if (material == "S"){
      int ID = getValue(inputString, ',', 1).toInt(); // servo 1 or 2
      int angle = getValue(inputString, ',', 2).toInt(); // between 0 - 360
      int motorSpeed = getValue(inputString, ',', 3).toInt(); //  between 0 - 255 
      
      mysmartservo.moveTo(ID,angle,motorSpeed);
    }
    else if (material == "M"){
      char action = getValue(inputString, ',', 1)[0] ;// F, R, L, B, S
      uint8_t motorSpeed = getValue(inputString, ',', 2).toInt();//  between 0 - 255 

      Mouvement(action, motorSpeed);
    }
    else if(material == "L"){ //L,ID,red,green,blue.
      int ID = getValue(inputString, ',', 1).toInt(); 
      int red = getValue(inputString, ',', 2).toInt(); // between 0 - 64
      int green = getValue(inputString, ',', 3).toInt(); //  
      int blue = getValue(inputString, ',', 4).toInt();
      led.setColorAt(ID, red, green, blue);
      led.show();
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
  
  }
void Sending(long int *ValueToSend, int lenArray){ //function to send value to python
  
  String reading = String(ValueToSend[0]);
  for (int i=1; i< lenArray ; i++){ 
    reading = reading + "," + String(ValueToSend[i]);
  }

  if ((reading != lastState)) { //we send in a serial only in case of a new state
    lastDebounceTime = millis();
    chflag = true;
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (chflag) {
      chflag = false; 
      Serial.print(reading + String("."));
    }
  }
  lastState = reading;

    
}
int Mouvement(char action, uint8_t motorSpeed){

  if (action == 'F'){ //forward
    motor1.run(motorSpeed); /* value: between -255 and 255. */
    motor2.run(motorSpeed);
    motor3.run(-motorSpeed); 
    motor4.run(-motorSpeed);
  }
  else if (action == 'L'){ //left
    motor1.run(motorSpeed); /* value: between -255 and 255. */
    motor2.run(motorSpeed);
    motor3.run(motorSpeed); 
    motor4.run(motorSpeed);
  }
  else if (action == 'R'){ //right
    motor1.run(-motorSpeed); /* value: between -255 and 255. */
    motor2.run(-motorSpeed);
    motor3.run(-motorSpeed); 
    motor4.run(-motorSpeed);
  }
  else if (action == 'B'){ //back
    motor1.run(-motorSpeed); /* value: between -255 and 255. */
    motor2.run(-motorSpeed);
    motor3.run(motorSpeed); 
    motor4.run(motorSpeed);
  }
  else{
    motor1.stop();
    motor2.stop();
    motor3.stop();
    motor4.stop(); 
  }
 
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '.') {
      stringComplete = true;
    } 
  }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
