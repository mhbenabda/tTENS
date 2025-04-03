#include "DFRobot_GP8403.h"
DFRobot_GP8403 dac(&Wire,0x58);
const int TRIGGER = 8;
const int pin1 = 10;
const int pin2 = 11;
const int pin3 = 12;
const int pin4 = 13;
const int pin5 = 7; 
unsigned int counter = 0;

void setup() {
  Serial.begin(115200);

  while(dac.begin()!=0){
    Serial.println("init error");
    delay(1000);
   }
  Serial.println("init succeed");
  //Set DAC output range
  dac.setDACOutRange(dac.eOutputRange10V);

  dac.setDACOutVoltage(5000, 0);
  delay(1000);

  pinMode(TRIGGER, OUTPUT);
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  pinMode(pin5, OUTPUT);
  
}

void loop() {
  if (Serial.available()){
    String triggerCmd = Serial.readStringUntil('\n');
    if (triggerCmd.substring(0,5) == "start"){
      unsigned int freq = triggerCmd.substring(5).toInt();
      tone(TRIGGER, freq);
      
      //digitalWrite(TRIGGER, HIGH);
      Serial.println(freq);
    }
    else if (triggerCmd.substring(0,4) == "stop"){
      noTone(TRIGGER);
      Serial.println("stopped");
    }
    else if (triggerCmd.substring(0,3) == "amp"){
      unsigned int voltage = triggerCmd.substring(3).toInt();
      dac.setDACOutVoltage(voltage, 0);
      //delay(1000);
    }
    else if (triggerCmd.substring(0,7) == "channel"){
      unsigned int channel = triggerCmd.substring(7).toInt();
      setChannel(channel);
      Serial.println(triggerCmd);
    }
  }
/*
  for(int i = 0; i < 100; i++){
    setChannel(counter);
    Serial.print("led ");
    Serial.println(counter);
    delay(1000);
    if (counter == 8){counter = 0;}
    counter++;
  }
*/
}

void setChannel(unsigned int channel){
  switch(channel){
    case 0:
      digitalWrite(pin1, LOW);
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      delay(1); // [ms] temporary to be reduced
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    case 1:
      digitalWrite(pin1, HIGH);
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    case 2:
      digitalWrite(pin1, LOW);
      digitalWrite(pin2, HIGH);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    case 3:
      digitalWrite(pin1, HIGH);
      digitalWrite(pin2, HIGH);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    case 4:
      digitalWrite(pin1, LOW);
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, HIGH);
      digitalWrite(pin4, LOW);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    case 5:
      digitalWrite(pin1, HIGH);
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, HIGH);
      digitalWrite(pin4, LOW);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    case 6:
      digitalWrite(pin1, LOW);
      digitalWrite(pin2, HIGH);
      digitalWrite(pin3, HIGH);
      digitalWrite(pin4, LOW);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    case 7:
      digitalWrite(pin3, HIGH);
      digitalWrite(pin1, HIGH);
      digitalWrite(pin2, HIGH);
      digitalWrite(pin4, LOW);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    case 8:
      digitalWrite(pin1, LOW);
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, HIGH);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
    default:
      digitalWrite(pin1, LOW);
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      delay(1);
      digitalWrite(pin5, HIGH);
      delay(1);
      digitalWrite(pin5, LOW);
      break;
  }
}
