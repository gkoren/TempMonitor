#include "max6675.h"
#include "SPI.h"
#include "ESP8266.h"


ESP8266 wifi(Serial2);
#define HOST_NAME   "10.100.102.11"
#define HOST_PORT   (4005)

int ktcSO = 51;
int ktcCLK = 53;
int nSensors = 2;

//MAX6675 ktc[] = {MAX6675(ktcCLK, 49, ktcSO)};//1

MAX6675 ktc[] = {MAX6675(ktcCLK, 49, ktcSO),//1
                 //MAX6675(ktcCLK, 32, ktcSO),//9
                 //MAX6675(ktcCLK, 34, ktcSO),//8
                 //MAX6675(ktcCLK, 36, ktcSO),//7
                 //MAX6675(ktcCLK, 42, ktcSO),//4
                 //MAX6675(ktcCLK, 40, ktcSO),//5
                 //MAX6675(ktcCLK, 38, ktcSO),//6
                 //MAX6675(ktcCLK, 44, ktcSO),//3
                 MAX6675(ktcCLK, 45, ktcSO)};//2


void setup() {
  Serial2.begin(115200);
  Serial.begin(115200);
  wifi.restart();
  
  //establishContact();
  //counter = 0;
  // give the MAX a little time to settle
  delay(800);
}

void loop() {
  // basic readout test
 
 Serial.print(" ");
 String data_str = "";
 for (int i = 0 ; i < nSensors ; i++){
  data_str+=ktc[i].readCelsius();
  if (i != nSensors -1){
   data_str+=",";
  }
 }
 //if (i != nSensors - 1){
   // Serial.print(ktc[i].readCelsius());
   // Serial.print(',');
  //}
  //else {
    //Serial.print(ktc[i].readCelsius());
    //Serial.println();
  //}
 
if (wifi.registerUDP(HOST_NAME, HOST_PORT)) {
    const char *data = data_str.c_str();
    wifi.send((const uint8_t*)data, strlen(data));
    Serial.print("sent: ");
    Serial.println(data);
} else {
    Serial.print("register udp err\r\n");
}

  delay(2000);
}

void establishContact() {
  while (Serial.available() <= 0) {
  Serial.println(nSensors);   // send a capital A
  delay(300);
  }
}
