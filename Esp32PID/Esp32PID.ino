const int pinData = 16;
const int pinClk = 4;
int counter = 0;
int millisec = 0; 
int fallingperperiod = 0;
int nextconv = 0;
int dataBCD[8] = {0,0,0,0,0,0,0,0};
int screennr = 0;
String test;

volatile SemaphoreHandle_t clockSemaphore;
portMUX_TYPE clockMux = portMUX_INITIALIZER_UNLOCKED;

void IRAM_ATTR handleInterrupt() {

  portENTER_CRITICAL_ISR(&clockMux);
  counter++;
  portEXIT_CRITICAL_ISR(&clockMux);

  xSemaphoreGiveFromISR(clockSemaphore, NULL);

}

void setup() 
{
  Serial.begin(500000);
  Serial.print("Hello");
  
  pinMode( pinData, INPUT);
  pinMode( pinClk, INPUT);

  attachInterrupt(pinClk, handleInterrupt, FALLING);
  clockSemaphore = xSemaphoreCreateBinary();

  millisec = micros();
}

void loop() 
{


  if (xSemaphoreTake(clockSemaphore, 0) == pdTRUE) {
    int millycarlucci = micros();
 
    uint32_t isrCount = 0;
    portENTER_CRITICAL(&clockMux);
    isrCount = counter;
    portEXIT_CRITICAL(&clockMux);
    
    if(millycarlucci-millisec < 200){
      
      fallingperperiod++;
      delayMicroseconds(10);
      dataBCD[fallingperperiod] = digitalRead(pinData);

    }else{
     
      fallingperperiod =0;
      //Serial.printf("%d%d%d%d%d%d%d%d\n",dataBCD[0],dataBCD[1],dataBCD[2],dataBCD[3],dataBCD[4],dataBCD[5],dataBCD[6],dataBCD[7]);
      int value = 0;
      for (byte i=0; i<8; i++)
      {
      value *= 2;
      value += dataBCD[i] ;
      }
      //Serial.println(value,HEX);

      //test[screennr++] = decodedisplay (value);
      test = decodedisplay (value);
      Serial.print(test);
//      if(screennr == 4){
//        Serial.print(test[0]);
//        Serial.print(test[1]);
//        Serial.print(test[2]);
//        Serial.println(test[3]);
//        screennr = 0;
//      }
      delayMicroseconds(10);
      dataBCD[fallingperperiod] = digitalRead(pinData);
//      if (test[0] == "r" || test[0] == "g"){
//        screennr = 0;
//      }
    }
    millisec = micros();

  } 
  
}


  /* tutto spento=FF 
   *  tutto acceso=00
      1=7B
      2=C1
      3=51
      4=72
      5=54
      6=44
      7=79
      8=40
      9=50
      0=48
      P=E0
      G=4c
      d=43
      F=
      led verde=F7
      led rosso=FB  
 */ 
String decodedisplay(int someNumber) {
  switch (someNumber) {
    case 0x7B:
      return "1";
    case 0xC1:
      return "2";
    case 0x51:
      return "3";
    case 0x72:
      return "4";
    case 0x054:
      return "5";
    case 0x44:
      return "6";
    case 0x79:
      return "7";
    case 0x40:
      return "8";
    case 0x50:
      return "9";
    case 0x48:
      return "0";
    case 0xE0:
      return "P"; // Hexidecimal A
    case 0x4C:
      return "G"; // Hexidecimal B
    case 0x43:
      return "d"; // Hexidecimal C
    case 0xE8:
      return "F"; // Hexidecimal D
    case 0xF7:
      return "g"; // Hexidecimal E
    case 0xFB:
      return "r"; // Hexidecimal F 
    case 0xFF:
      return " ";
    case 0x00:
      return "A";
    default:
      return "e"; // Error condition, displays three vertical bars 
  }
}
