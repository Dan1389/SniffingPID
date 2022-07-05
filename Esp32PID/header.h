#ifndef HEADER
#define HEADER

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include "SPIFFS.h"
#include <PubSubClient.h>
#include "wifi_esp32.h"
#include <SparkFun_ADXL345.h>
#include <SPI.h>
#include <WebServer.h>

#define WIFI_ATTEMPT  20
#define MQTT_ATTEMPT  3
#define VERBOSE 1
#define PRINT_INFO 0
#define SERIAL_PRINT 0

/**********************************************/
#define ADXL345_RATE_3200     3200.0
#define ADXL345_RATE_1600     1600.0
#define ADXL345_RATE_800      800.0
#define ADXL345_RATE_400      400.0
#define ADXL345_RATE_200      200.0
#define ADXL345_RATE_100      100.0
#define ADXL345_RATE_50       50.0
#define ADXL345_RATE_25        25.0
#define ADXL345_RATE_12_5     12.5
#define ADXL345_RATE_6_25     6.25
#define ADXL345_RATE_3_13     3.13
#define ADXL345_RATE_1_56     1.56
#define ADXL345_RATE_0_78     0.78
#define ADXL345_RATE_0_39     0.39
#define ADXL345_RATE_0_20     0.2
#define ADXL345_RATE_0_10     0.1
/*******************************************************/

#define MSG_BUFFER_SIZE  256
#define SAMPLE_BUFFER_SIZE  6400*3 //((6400 per second [3200 samples * 2 byte])*3 second)
#define MEAS_PER_TRANSMISSION 96
#define N_PACKET (SAMPLE_BUFFER_SIZE/(MEAS_PER_TRANSMISSION*2))
#define LEN_HEADER 4

typedef struct mqtt_datas_s{
  byte unix[LEN_HEADER];
  byte ms[LEN_HEADER];
  byte fc[LEN_HEADER];
  byte num_pkt[LEN_HEADER];
  byte datas[MEAS_PER_TRANSMISSION*2];
}mqtt_datas;

#define TOTAL_LEN_HEADER (sizeof(mqtt_datas) - (MEAS_PER_TRANSMISSION*2))
#define LEN_PACKET (MEAS_PER_TRANSMISSION * 2) + TOTAL_LEN_HEADER

volatile SemaphoreHandle_t timerSemaphore;
volatile SemaphoreHandle_t memorySemaphore;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;
portMUX_TYPE memoryMux = portMUX_INITIALIZER_UNLOCKED;

/*************************************WIFI************************/
wifi_conf wifi_settings;
bool connection_state = "false";
WebServer server(80);

/***************************MQTT VARIABLE**********************************/
#define TIME_FOR_NEXT_PUBLISH 1000
#define MQTT_TOPIC_DRILL_DATA  "trimmer/%ll012X/xyz"
#define MSG_BUFFER_SIZE  75
/**************/
WiFiClient espClient;
char nametopicdata[MSG_BUFFER_SIZE];
PubSubClient client(espClient);
unsigned long lastMsg = 0;

char msg[MSG_BUFFER_SIZE];
int numChar = 0;
int value = 0;
uint32_t unixTime = 0;
unsigned long startmillis = 0;
unsigned long nowmillis = 0;
unsigned long miss=0;
unsigned long elapsed = 0;
bool status_mqtt = false;

volatile uint32_t isrCounter = 0;
volatile uint32_t memCounter = 0;
volatile uint32_t lastIsrAt = 0;

mqtt_datas bcountXYZ[N_PACKET*3];

int number_trans=0;

ADXL345 adxl = ADXL345(5);
uint32_t sampleCounter = 0;
uint32_t packetCounter=0;
int retry = 0;
char nametopicaccxyz[32];

const int interruptPin = 27;
const int clearFlashBtn = 16;
const int Led1 = 4;
const int Led2 = 0;

int x, y, z;
float dt=0.0;
float dtlv=0.0;

int countfailx=0;
int countfaily=0;
int countfailz=0;

void IRAM_ATTR handleInterrupt();

#endif //HEADER
