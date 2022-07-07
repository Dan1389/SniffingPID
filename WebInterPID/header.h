#ifndef HEADER
#define HEADER

#include "wifi_esp32.h"
#include <WebServer.h>
#include "SPIFFS.h"
/*********************PIN TO RESET FLASH**************************/
const int flashPin = 14;

/*************************************WIFI************************/
wifi_conf wifi_settings;
int retry = 20;
bool connection_state = "false";
WebServer server(80);

#endif //HEADER
