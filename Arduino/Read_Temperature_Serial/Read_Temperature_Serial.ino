#include "max6675.h"
#include "SPI.h"

int ktcSO = 50;
int ktcCLK = 52;
int nSensors = 8;

//int counter;

//MAX6675 ktc[] = {MAX6675(ktcCLK, 44, ktcSO)};//1

MAX6675 ktc[] = {//MAX6675(ktcCLK, 48, ktcSO),//1
                 MAX6675(ktcCLK, 46, ktcSO),//1
                 MAX6675(ktcCLK, 44, ktcSO),//2
                 MAX6675(ktcCLK, 42, ktcSO),//3
                 MAX6675(ktcCLK, 40, ktcSO),//4
                 MAX6675(ktcCLK, 38, ktcSO),//5
                 MAX6675(ktcCLK, 36, ktcSO),//6
                 MAX6675(ktcCLK, 34, ktcSO),//7
                 MAX6675(ktcCLK, 32, ktcSO)};//8
                 
                 

void setup() {
  Serial.begin(9600);
  //establishContact();
  //counter = 0;
  // give the MAX a little time to settle
  delay(800);
}

void loop() {
  
 // basic readout test
 //if (Serial.available() > 0){
 //Serial.print("Temp1: "); 
 
 Serial.print(" ");
 String data_str = "";
 for (int i = 0 ; i < nSensors ; i++){
  data_str+=ktc[i].readCelsius();
  if (i != nSensors - 1){
   data_str+=",";
  }
 }
  Serial.println(data_str);
  delay(2200);
}

void establishContact() {
  while (Serial.available() <= 0) {
  Serial.println(nSensors);   // send a capital A
  delay(300);
  }
}

