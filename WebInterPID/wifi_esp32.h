#ifndef WIFI_ESP32
#define WIFI_ESP32

#include <WiFi.h>
#include "memory_foam.h"
#include <time.h>
#include <string.h>

#define VERBOSE_WIFI 0
#define FLASH_SIZE 512
#define ADDRESS_SSID_SIZE 0
#define CFG_ADDRESS 0
#define SIZE_LEN 1 //uint8_t
#define BUFFER_SIZE 25
#define find_endof_mqttcredentials( a ) find_endof_wificredentials( a )

struct wifi_conf
{
  char bname[20];
  char ssid[20];
  char ssidpwd[20];
  char mqttaddr[20];
  char mqttport[20];
  char mqttuser[20];
  char mqttpwd[20];
  char ntpserver[30];
  char ip[20];
  char subnet[20];
  char gw[20];
  char fullscale[10];
};

class WiFi_Init
{
  public:
    String get_MACid();
    bool scan_wifi_network();
    void print_info_wifi(char * ssid, char * password, char * mqtt_server, char * mqtt_port, char * mqtt_usr , char * mqtt_pwd, char * ntpserver  );
    bool configure_static_wifi(IPAddress local_IP,IPAddress gateway,IPAddress subnet);
    bool initialize_credential(char * ssid, char * password, char * mqtt_server, int * mqtt_port);
    
    bool initialize_credential_secure(char * ssid, char * password, char * mqtt_server, int * mqtt_port, char * mqtt_user, char * mqtt_pwd);
    bool initialize_credential_mqtt_secure(char * mqtt_user, char * mqtt_pwd, int startAddress);

    bool initialize_credential_fromWebpage(wifi_conf * cfg);
    bool check_credential(wifi_conf * cfg);
    bool conf_static_settings(char * ip, char *gw, char *subnet);
    
    bool initialize_credential_wifi(char * ssid, char * password);
    bool initialize_credential_mqtt(char * mqtt_server, int * mqtt_port, int startAddress);
    
    bool set_wifi_ap (char* ssid,char* password);
    bool clear_credential();
    bool setup_wifi(char * ssid, char * password, int Retry_max);
    bool retrieve_NTP(char * ssid, char * password, int Retry_max, uint32_t * unix, char * ntpServer);

    void sleep_wifi();
  private:
  
    int save_prm(int start_addr, uint8_t len , uint8_t * prm);
    int load_prm(int start_addr, uint8_t * prm);
    const char* ntpServerconst = "it.pool.ntp.org";
    int find_endof_wificredentials(int start_addr);
    const IPAddress apIP = IPAddress(192, 168, 4, 1);

    const long  gmtOffset_sec = 3600;
    const int   daylightOffset_sec = 3600;
    uint32_t printLocalTime();
};

#if !defined(NO_GLOBAL_INSTANCES) && !defined(NO_GLOBAL_EEPROM)
extern WiFi_Init Wifi_custom;
#endif

#endif //WIFI_ESP32
