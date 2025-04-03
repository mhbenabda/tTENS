#include "DFRobot_GP8403.h"
DFRobot_GP8403 dac(&Wire,0x58);
const int TRIGGER = 8;
// TTL pins 
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
    String command = Serial.readStringUntil('\n');
    String cmd_name;
    unsigned int param1, param2;
    parse_command(command, cmd_name, param1, param2);

    if (cmd_name == "triggerD"){
      // param1 -> freq
      // param2 -> duration
      // Generates a square wave
      tone(TRIGGER, param1, param2);
      delay(param2);
    }
    else if (cmd_name == "triggerN"){
      // param1 -> freq
      // param2 -> num_triggers
      float T_half = ((1000 / param1)) / 2; // half period in ms
      Serial.println("done");
      for (unsigned int i = 0; i < param2; i++){
        digitalWrite(TRIGGER, HIGH);
        delay(T_half);
        digitalWrite(TRIGGER, LOW);
        delay(T_half);
      }
    }
    else {
      digitalWrite(TRIGGER, LOW);
      noTone(TRIGGER);
      //Serial.println("stopped");
    }
  }
}

void parse_command(String cmd, String &cmd_name, unsigned int &param1, unsigned int &param2){
  // Split the command
  int first_colon = cmd.indexOf(':');
  int second_colon = cmd.indexOf(':', first_colon + 1);

  cmd_name = cmd.substring(0, first_colon);
  param1 = cmd.substring(first_colon + 1, second_colon).toInt();
  param2 = cmd.substring(second_colon + 1).toInt();
}


























