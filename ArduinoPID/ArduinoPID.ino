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
char input=0;
/*PIN DI DATI VERSO GLI SHIFT REGISTER**/
const int pinData = 2;
const int pinClk = 3;

/*PIN DI ENABLE DEI DISPLAY*/
const int display1 = 4;
const int display2 = 5;
const int display3 = 6;

/*PIN DI OUT PER IL CONTROLLO DEI BOTTONI*/
const int TPIU  = 7;
const int PRG   = 8;
const int SEL   = 9;
const int TMENO = 10;

const int IN1  = 11;
const int IN3  = 12;
const int IN2  = 13;


int counter = 0;
int millisec = 0; 
int fallingperperiod = 0;
int dataBCD[8] = {0,0,0,0,0,0,0,0};
int screennr = 0;
char result[4];
int dsp1,dsp2,dsp3;
int selected=0;
#define TIME    1500
#define TIMEon  700
#define TIMEoff 200
bool flag= false;

void handleInterrupt() {

 flag = true;

}

void setup() 
{
  Serial.begin(115200);
  Serial.print("Hello");
  
  pinMode( pinData, INPUT);
  pinMode( pinClk, INPUT);
   
  pinMode( display1, INPUT);
  pinMode( display2, INPUT);
  pinMode( display3, INPUT);

  pinMode( PRG,   OUTPUT);
  pinMode( SEL,   OUTPUT);
  pinMode( TPIU,  OUTPUT);
  pinMode( TMENO, OUTPUT);

  pinMode( IN1,  OUTPUT);
  pinMode( IN3,  OUTPUT);
  pinMode( IN2,  OUTPUT);
  
  digitalWrite(IN1  ,HIGH);
  digitalWrite(IN3  ,HIGH);
  digitalWrite(IN2  ,HIGH);

  
  attachInterrupt(digitalPinToInterrupt(pinClk), handleInterrupt, FALLING);

  millisec = micros();
}

void loop() 
{


  if (flag) {
    int millycarlucci = micros();
    
    if(millycarlucci-millisec < 200){
      
      fallingperperiod++;
      delayMicroseconds(10);
      dataBCD[fallingperperiod] = digitalRead(pinData);

      if (fallingperperiod == 7 ){
        delayMicroseconds(60);
        

        dsp1 = digitalRead(display1);
        dsp2 = digitalRead(display2);
        dsp3 = digitalRead(display3);
        
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

          input = Serial.read();
          char buff[6];
          sprintf(buff,"%c%c%c%c\n",result[0],result[1],result[2],result[3]);
          Serial.println(buff);
      }
      
      delayMicroseconds(10);
      dataBCD[fallingperperiod] = digitalRead(pinData);
    }

    millisec = micros();
    flag = false;
     
  } 
  //input = Serial.read();
  if (input=='e'){
    digitalWrite(PRG,LOW);
    delay(TIME);
  }else if (input=='d'){
    digitalWrite(SEL,LOW);
    delay(TIME);
  }else if (input=='r'){
    digitalWrite(TPIU,LOW);
    delay(TIME);
  }else if (input=='f'){
    digitalWrite(TMENO,LOW);
    delay(TIME);   
  }else if (input=='t'){
    digitalWrite(TMENO,LOW);
    delay(TIMEon);
    digitalWrite(TMENO,HIGH);
    delay(TIMEoff);
  }else if (input=='q'){    
    digitalWrite(IN1,LOW);
    delay(100);
  }else if( input=='a'){
    digitalWrite(IN3,LOW);
    delay(100);
  }else if (input=='z'){
    digitalWrite(IN2,LOW);
    delay(100);
  }else if (input=='w'){
    digitalWrite(IN1,HIGH);
    delay(100);
  }else if( input=='s'){
    digitalWrite(IN3,HIGH);
    delay(100);
  }else if (input=='x'){
    digitalWrite(IN2,HIGH);
    delay(100);
  }
  digitalWrite(TMENO,HIGH);
  digitalWrite(TPIU ,HIGH);
  digitalWrite(SEL  ,HIGH);
  digitalWrite(PRG  ,HIGH);
  

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
