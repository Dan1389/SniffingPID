/******************SEQUENZA BCD + led finale**************
disp off=FF 
disp on=00
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
F=E8
green led=F7
red led=FB  
/*****************************************/

/*PIN DI DATI VERSO GLI SHIFT REGISTER**/
const int pinData = 16;
const int pinClk = 4;

/*PIN DI ENABLE DEI DISPLAY*/
const int display1 = 5;
const int display2 = 18;
const int display3 = 19;

/*PIN DI OUT PER IL CONTROLLO DEI BOTTONI*/
const int button1 = 22;
const int button2 = 23;
const int button3 = 2;
const int button4 = 15;

int counter = 0;
int millisec = 0; 
int fallingperperiod = 0;
int dataBCD[8] = {0,0,0,0,0,0,0,0};
int screennr = 0;
char result[4];
int dsp1,dsp2,dsp3;
int selected=0;

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
   
  pinMode( display1, INPUT);
  pinMode( display2, INPUT);
  pinMode( display3, INPUT);

  pinMode( button1, OUTPUT);
  pinMode( button2, OUTPUT);
  pinMode( button3, OUTPUT);
  pinMode( button4, OUTPUT);
  
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

      if (fallingperperiod == 7 ){
        delayMicroseconds(60);
        digitalWrite(button1,HIGH);

        dsp1 = digitalRead(display1);
        dsp2 = digitalRead(display2);
        dsp3 = digitalRead(display3);
        digitalWrite(button1,LOW);
        if(dsp1 == 0 && dsp2 == 0 && dsp3 == 0){
          selected = 3;
        }else if (dsp1 == 1 && dsp2 == 0 && dsp3 == 0){
          selected = 0;
        }else if (dsp1 == 0 && dsp2 == 1 && dsp3 == 0){
          selected = 1;
        }else if (dsp1 == 0 && dsp2 == 0 && dsp3 == 1){
          selected = 2;
        }       
      }

    }else{
     
      fallingperperiod =0;
      int value = 0;
      for(byte i=0; i<8; i++){
         value *= 2;
         value += dataBCD[i] ;
      }
      result[selected] = decodedisplay (value);
  
        if(selected == 3){
          Serial.printf("%c%c%c%c\n",result[0],result[1],result[2],result[3]);
        }
      
      delayMicroseconds(10);
      dataBCD[fallingperperiod] = digitalRead(pinData);
    }

    millisec = micros();

  } 
  
}

char decodedisplay(int someNumber) {
  switch (someNumber) {
    case 0x7B:
      return '1';
    case 0xC1:
      return '2';
    case 0x51:
      return '3';
    case 0x72:
      return '4';
    case 0x054:
      return '5';
    case 0x44:
      return '6';
    case 0x79:
      return '7';
    case 0x40:
      return '8';
    case 0x50:
      return '9';
    case 0x48:
      return '0';
    case 0xE0:
      return 'P'; 
    case 0x4C:
      return 'G'; 
    case 0x43:
      return 'd'; 
    case 0xE4:
      return 'F'; 
    case 0xC8:
      return 'E'; 
    case 0xF7:
      return 'g'; 
    case 0xFB:
      return 'r'; 
    case 0xFF:
      return ' ';
    case 0x00:
      return 'A';
    default:
      return 'e';
  }
}
