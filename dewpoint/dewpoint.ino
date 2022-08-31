#include "DHT.h"
#include <Wire.h>
#include "Adafruit_MCP9808.h"
#include "BluetoothSerial.h"
#include "esp_bt_device.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define DHTPIN 25  
#define DHTTYPE DHT22
#define RELE 14

DHT dht(DHTPIN, DHTTYPE);
Adafruit_MCP9808 tempsensor = Adafruit_MCP9808();
   
char buf[50];
int len = 0;
   
BluetoothSerial SerialBT;
char MANUAL;
int fan;
char lv;
void printDeviceAddress() {
 
  const uint8_t* point = esp_bt_dev_get_address();
 
  for (int i = 0; i < 6; i++) {
 
    char str[3];
 
    sprintf(str, "%02X", (int)point[i]);
    Serial.print(str);
 
    if (i < 5){
      Serial.print(":");
    }
 
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println(F("Fai Sensor"));
  
  pinMode(RELE, OUTPUT);
  digitalWrite(RELE, HIGH);
  
  dht.begin();

  if (!tempsensor.begin(0x18)) {
    Serial.println("Couldn't find MCP9808! Check your connections and verify the address is correct.");
    while (1);
  }

    tempsensor.setResolution(3); // sets the resolution mode of reading, the modes are defined in the table bellow:
  // Mode Resolution SampleTime
  //  0    0.5°C       30 ms
  //  1    0.25°C      65 ms
  //  2    0.125°C     130 ms
  //  3    0.0625°C    250 ms

  Serial.println("\n---Start---");
  SerialBT.begin("DewPointController"); //Bluetooth device name
  
  Serial.println("The device started, now you can pair it with bluetooth!");
  Serial.println("Device Name: ESP32test");
  Serial.print("BT MAC: ");
  printDeviceAddress();
  Serial.println();
}
int dewPoint(float T,float Ur){

  float Es,E=0.0f;
  float a= 7.5;
  float b= 237.7f;
  float c=430.22f;
  float d= 19.08f;
  

  Es=6.11*pow(10,(a*T)/(b+T));
  E=(Ur*Es)/100;
  return (-c+b*log(E))/(-log(E)+d);
  
}
void loop() {
  //digitalWrite(RELE, !digitalRead(RELE));
  delay(2000);

  float hdht = dht.readHumidity();
  float tdht = dht.readTemperature();
  
  tempsensor.wake(); 
  float c = tempsensor.readTempC();

  tempsensor.shutdown_wake(1);
  
  if (isnan(hdht) || isnan(tdht)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  
  Serial.println("DHT:");
  Serial.print(F("Humidity: "));
  Serial.print(hdht);
  Serial.print(F("%  Temperature: "));
  Serial.println(tdht);

 
  Serial.println("MCP:");
  Serial.print(c, 4); 
  Serial.print("*C\n"); 
  Serial.println("DEW POINT:"); 
  float Td;
  Td=dewPoint(c,hdht);
  
  Serial.print(Td,4); 
  if (MANUAL!='Y'){
    if(Td > tdht){
      digitalWrite(RELE, HIGH);
      Serial.println("\nFan On");
      fan=1;
    }
    else{
      digitalWrite(RELE, LOW);
      Serial.println("\nFan Off");
      fan=0;
    }
  }else if(MANUAL=='Y'){
    digitalWrite(RELE, HIGH);
    Serial.println("\nManual Fan On");
    fan=2;
  }
  else
    fan=0;

   len = sprintf(buf,"%06.2f;%06.2f;%06.2f;%06.2f;%d\n",hdht,tdht,c,Td,fan);

  //if (Serial.available()) {
  //if (MANUAL == 'G')
  for(int i = 0 ; i < len;i++)
    SerialBT.write(buf[i]);
  //}
  
  while(SerialBT.available()) {

      MANUAL=SerialBT.read();
      if (lv == 'Y' && MANUAL != 'N'){
        MANUAL ='Y';
      }
      else if (MANUAL == 'Y'){
        MANUAL ='Y';
      }
      else{
        MANUAL = 'N';
      }
      lv = MANUAL;
      Serial.println("RECEIVED MEX FROM BT");
  }

}
