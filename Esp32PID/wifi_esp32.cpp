#include "wifi_esp32.h"

/******************************************************************/
/*Library implementing some wifi functions on esp32.
  Function list:
  scan_wifi_network(); scan wifi networks
  print_info_wifi(...); print from flash memory network settings
  initialize_credential(...); save in flash or read from flash the
  credential, if not present ask to the user the new datas
  initialize_credential_wifi(...); used in initialize_credential
  can be used alone too
  initialize_credential_mqtt(...); used in initialize_credential
  can be used alone too
  setup_wifi(...); activate wifi
  sleep_wifi(); shut down the wifi
*/
/******************************************************************/

bool WiFi_Init::scan_wifi_network() {

  int numberOfNetworks = WiFi.scanNetworks();
  Serial.println("\n");
  for (int i = 0; i < numberOfNetworks; i++) {
    Serial.print(i);
    Serial.print(": ");
    Serial.print("Network name: ");
    Serial.println(WiFi.SSID(i));
    Serial.print("Signal strength: ");
    Serial.println(WiFi.RSSI(i));
    Serial.println("-----------------------");

  }
}
bool WiFi_Init::configure_static_wifi(IPAddress local_IP,IPAddress gateway,IPAddress subnet) {

    if (!WiFi.config(local_IP, gateway, subnet)) {
      return false;
    }
   
   return true;
    
}

void WiFi_Init::print_info_wifi(char * ssid, char * password, char * mqtt_server, char * mqtt_port, char * mqtt_usr , char * mqtt_pwd, char * ntpserver  ) {
  Serial.println("-------------------------------------------");
  Serial.println("---------------NETWORK INFO----------------");
  Serial.print  ("||SSID:               ");
  Serial.print  (ssid);
  Serial.println("||");
  Serial.print  ("||Password:           ");
  Serial.print  (password);
  Serial.println("||");
  Serial.print  ("||mqtt server:        ");
  Serial.print  (mqtt_server);
  Serial.println("||");
  Serial.print  ("||port:               ");
  Serial.print  (mqtt_port);
  Serial.println("||");
  Serial.print  ("||mqtt user:               ");
  Serial.print  (mqtt_usr);
  Serial.println("||");
  Serial.print  ("||mqtt password:               ");
  Serial.print  (mqtt_pwd);
  Serial.println("||");
  Serial.print  ("||ntp server:               ");
  Serial.print  (ntpserver);
  Serial.println("||");
  Serial.println("-------------------------------------------");
}

int WiFi_Init::find_endof_wificredentials(int start_addr) {

  int size_pwd = 0;
  int size_ssid = 0;

  MF.read_memory(start_addr , (uint8_t *) &size_ssid, sizeof(size_ssid));

  if (size_ssid > 0) {
    MF.read_memory(start_addr + sizeof(size_ssid) + size_ssid , (uint8_t *) &size_pwd, sizeof(size_pwd));

    return (size_pwd + size_ssid + sizeof(int) * 2);

  } else return -1;
}

bool  WiFi_Init::initialize_credential(char * ssid, char * password, char * mqtt_server, int * mqtt_port) {

  int stAddr = -1;

  MF.start_memory(FLASH_SIZE);
  initialize_credential_wifi(ssid, password);
  stAddr = find_endof_wificredentials(ADDRESS_SSID_SIZE);
  if (stAddr > 0)
    initialize_credential_mqtt(mqtt_server, mqtt_port, stAddr);
  MF.stop_memory();
  return true;
}

bool WiFi_Init::initialize_credential_secure(char * ssid, char * password, char * mqtt_server, int * mqtt_port, char * mqtt_user, char * mqtt_pwd) {

  int stAddr = -1;

  MF.start_memory(FLASH_SIZE);
  initialize_credential_wifi(ssid, password);
  stAddr = find_endof_wificredentials(ADDRESS_SSID_SIZE);
  if (stAddr > 0)
    initialize_credential_mqtt(mqtt_server, mqtt_port, stAddr);

  stAddr += find_endof_mqttcredentials(stAddr);
  if (stAddr > 0)
    initialize_credential_mqtt_secure(mqtt_user, mqtt_pwd, stAddr);
  MF.stop_memory();
  return true;
}
bool WiFi_Init::initialize_credential_fromWebpage(wifi_conf * cfg){
  int next =0;
  MF.start_memory(FLASH_SIZE);
  next = save_prm(CFG_ADDRESS , sizeof(wifi_conf), (uint8_t *)     cfg); 
  MF.committ();
  MF.stop_memory();
  
  return true;
  
}
bool WiFi_Init::check_credential(wifi_conf * cfg){
  int next =0;
  MF.start_memory(FLASH_SIZE);
  next = load_prm(CFG_ADDRESS, (uint8_t *) cfg);
  if (next != -1){
    return true;
  }
  MF.stop_memory();
  return false;
}

bool WiFi_Init::conf_static_settings(char * ip, char *gw, char *subnet){
   
    uint8_t ip_t[4];
    uint8_t sub_t[4];
    uint8_t gw_t[4];

    sscanf(ip, "%u.%u.%u.%u", &ip_t[0], &ip_t[1], &ip_t[2], &ip_t[3]);
    sscanf(gw, "%u.%u.%u.%u", &gw_t[0], &gw_t[1], &gw_t[2], &gw_t[3]);
    sscanf(subnet, "%u.%u.%u.%u", &sub_t[0], &sub_t[1], &sub_t[2], &sub_t[3]);

    IPAddress local_IP(ip_t[0],ip_t[1],ip_t[2],ip_t[3]);
    IPAddress gateway(gw_t[0],gw_t[1],gw_t[2],gw_t[3]);
    IPAddress subnet_mask(sub_t[0],sub_t[1],sub_t[2],sub_t[3]);

    Wifi_custom.configure_static_wifi(local_IP, gateway, subnet_mask);
  
}

int WiFi_Init::save_prm(int start_addr, uint8_t len , uint8_t * prm) {
  
  int total = 0; 
  
  MF.write_memory_wo_committ(start_addr , &len, sizeof(len));
  MF.write_memory_wo_committ(start_addr + sizeof(len) , (uint8_t *) prm, len );

  total = start_addr + SIZE_LEN + len;
  
  return total;
  }
  
int WiFi_Init::load_prm(int start_addr, uint8_t * prm){
  
  uint8_t size_prm = 0;
  int total = -1;
  MF.read_memory(start_addr , (uint8_t *) &size_prm, sizeof(size_prm));
  if (size_prm > 0 && size_prm != 0xFF) {
    MF.read_memory(start_addr + sizeof(size_prm) , (uint8_t *) prm, size_prm );
    total = start_addr + size_prm + SIZE_LEN;
    return total;
  } else {
    return total;
  }
}

bool WiFi_Init::initialize_credential_mqtt(char * mqtt_server, int * mqtt_port, int startAddress) {

  int size_mqttserver = 0;
  int size_mqttport = 0;
  String mqtt_server_buff;
  String mqtt_port_buff;

  MF.read_memory(startAddress , (uint8_t *) &size_mqttserver, sizeof(size_mqttserver));

  if (size_mqttserver > 0) {
    MF.read_memory(startAddress + sizeof(size_mqttserver) , (uint8_t *) mqtt_server, size_mqttserver );
    MF.read_memory(startAddress + sizeof(size_mqttserver) + size_mqttserver , (uint8_t *) &size_mqttport, sizeof(size_mqttport));
    MF.read_memory(startAddress + sizeof(size_mqttserver) + size_mqttserver  + sizeof(size_mqttport) , (uint8_t *) mqtt_port, size_mqttport );
    return true;
  } else {
    Serial.println("");
    Serial.print("Inserisci indirizzo server MQTT:  ");
    while ( mqtt_server_buff.isEmpty() ) {
      mqtt_server_buff = Serial.readString();
    }
    size_mqttserver = mqtt_server_buff.length();
    mqtt_server_buff.toCharArray(mqtt_server, BUFFER_SIZE);
    Serial.println(mqtt_server);

    Serial.print("Inserisci porta:  ");
    while ( mqtt_port_buff.isEmpty() ) {
      mqtt_port_buff = Serial.readString();
    }
    size_mqttport = sizeof(int);
    *mqtt_port = mqtt_port_buff.toInt();
    Serial.println(*mqtt_port);

    MF.write_memory_wo_committ(startAddress , (uint8_t *) &size_mqttserver, sizeof(size_mqttserver));
    MF.write_memory_wo_committ(startAddress + sizeof(size_mqttserver) , (uint8_t *) mqtt_server, size_mqttserver );
    MF.write_memory_wo_committ(startAddress + sizeof(size_mqttserver) + size_mqttserver , (uint8_t *) &size_mqttport, sizeof(size_mqttport));
    MF.write_memory_wo_committ(startAddress + sizeof(size_mqttserver) + size_mqttserver  + sizeof(size_mqttport) , (uint8_t *) mqtt_port, size_mqttport );
    //MF.committ();
    return false;
  }
}

bool WiFi_Init::initialize_credential_mqtt_secure(char * mqtt_user, char * mqtt_pwd, int startAddress) {

  int size_mqtt_user = 0;
  int size_mqtt_pwd = 0;
  String mqtt_user_buff;
  String mqtt_pwd_buff;

  MF.read_memory(startAddress , (uint8_t *) &size_mqtt_user, sizeof(size_mqtt_user));

  if (size_mqtt_user > 0) {
    MF.read_memory(startAddress + sizeof(size_mqtt_user) , (uint8_t *) mqtt_user, size_mqtt_user );
    MF.read_memory(startAddress + sizeof(size_mqtt_user) + size_mqtt_user , (uint8_t *) &size_mqtt_pwd, sizeof(size_mqtt_pwd));
    MF.read_memory(startAddress + sizeof(size_mqtt_user) + size_mqtt_user  + sizeof(size_mqtt_pwd) , (uint8_t *) mqtt_pwd, size_mqtt_pwd );
    return true;
  } else {
    Serial.println("");
    Serial.print("Inserisci Username MQTT:  ");
    while ( mqtt_user_buff.isEmpty() ) {
      mqtt_user_buff = Serial.readString();
    }
    size_mqtt_user = mqtt_user_buff.length();
    mqtt_user_buff.toCharArray(mqtt_user, BUFFER_SIZE);
    Serial.println(mqtt_user);

    Serial.print("Inserisci Password MQTT:  ");
    while ( mqtt_pwd_buff.isEmpty() ) {
      mqtt_pwd_buff = Serial.readString();
    }
    size_mqtt_pwd = mqtt_pwd_buff.length();
    mqtt_pwd_buff.toCharArray(mqtt_pwd, BUFFER_SIZE);;
    Serial.println(mqtt_pwd);

    MF.write_memory_wo_committ(startAddress , (uint8_t *) &size_mqtt_user, sizeof(size_mqtt_user));
    MF.write_memory_wo_committ(startAddress + sizeof(size_mqtt_user) , (uint8_t *) mqtt_user, size_mqtt_user );
    MF.write_memory_wo_committ(startAddress + sizeof(size_mqtt_user) + size_mqtt_user , (uint8_t *) &size_mqtt_pwd, sizeof(size_mqtt_pwd));
    MF.write_memory_wo_committ(startAddress + sizeof(size_mqtt_user) + size_mqtt_user  + sizeof(size_mqtt_pwd) , (uint8_t *) mqtt_pwd, size_mqtt_pwd );
    //MF.committ();
    return false;
  }
}

bool WiFi_Init::initialize_credential_wifi(char * ssid, char * password) {

  int size_pwd = 0;
  int size_ssid = 0;
  String ssid_buff;
  String password_buff;
  MF.start_memory(FLASH_SIZE);

  MF.read_memory(ADDRESS_SSID_SIZE , (uint8_t *) &size_ssid, sizeof(size_ssid));

  if (size_ssid > 0) {
    MF.read_memory(ADDRESS_SSID_SIZE + sizeof(size_ssid) , (uint8_t *) ssid, size_ssid );
    MF.read_memory(ADDRESS_SSID_SIZE + sizeof(size_ssid) + size_ssid , (uint8_t *) &size_pwd, sizeof(size_pwd));
    MF.read_memory(ADDRESS_SSID_SIZE + sizeof(size_ssid) + size_ssid  + sizeof(size_pwd) , (uint8_t *) password, size_pwd );
    return true;
  } else {
    Serial.println("");
    Serial.print("Inserisci SSID:  ");
    while ( ssid_buff.isEmpty() ) {
      ssid_buff = Serial.readString();
    }
    size_ssid = ssid_buff.length();
    ssid_buff.toCharArray(ssid, BUFFER_SIZE);
    Serial.println(ssid);

    Serial.print("Inserisci password [minimo 8 caratteri]:  ");
    while ( password_buff.isEmpty() ) {
      password_buff = Serial.readString();
    }
    size_pwd = password_buff.length();
    password_buff.toCharArray(password, BUFFER_SIZE);
    Serial.println("********");

    MF.write_memory_wo_committ(ADDRESS_SSID_SIZE , (uint8_t *) &size_ssid, sizeof(size_ssid));
    MF.write_memory_wo_committ(ADDRESS_SSID_SIZE + sizeof(size_ssid) , (uint8_t *) ssid, size_ssid );
    MF.write_memory_wo_committ(ADDRESS_SSID_SIZE + sizeof(size_ssid) + size_ssid , (uint8_t *) &size_pwd, sizeof(size_pwd));
    MF.write_memory_wo_committ(ADDRESS_SSID_SIZE + sizeof(size_ssid) + size_ssid  + sizeof(size_pwd) , (uint8_t *) password, size_pwd );
    MF.committ();
    return false;
  }

}

bool WiFi_Init::setup_wifi(char * ssid, char * password, int Retry_max) {

  delay(10);
#if VERBOSE_WIFI == 1
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
#endif
  WiFi.begin(ssid, password);

  int retry = 0;

  while (WiFi.status() != WL_CONNECTED && (retry < Retry_max)) {
    delay(500);
#if VERBOSE_WIFI == 1
    Serial.print(".");
#endif
    retry++;
  }
  if (retry < Retry_max) {

    randomSeed(micros());

#if VERBOSE_WIFI == 1
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
#endif

    return false;

  } else {
    Serial.println("Failed to connect");
    return true;
  }
}
void WiFi_Init::sleep_wifi() {
  WiFi.mode(WIFI_OFF);
#if VERBOSE_WIFI == 1
  Serial.println("WiFi is down");
#endif
}

bool WiFi_Init::retrieve_NTP(char * ssid, char * password, int Retry_max , uint32_t * unix , char * ntpServer) {
  if (setup_wifi(ssid, password, Retry_max) == false) {

    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer );
    *unix = printLocalTime();
    return false;

  } else {
    Serial.println("Failed to connect");
    *unix = 0;
    return true;
  }


}
uint32_t WiFi_Init::printLocalTime()
{
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return 0;
  }
  time_t ret;
  ret = mktime(&timeinfo);

  //Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
  Serial.println(ret);

  return ret;
}

bool WiFi_Init::clear_credential() {
  MF.start_memory(FLASH_SIZE);
  MF.clear_memory(FLASH_SIZE);
  MF.stop_memory();
}

bool WiFi_Init::set_wifi_ap (char* ssid, char* password) {

#if VERBOSE_WIFI == 1
  Serial.print("Setting AP (Access Point)…");
#endif
  WiFi.mode(WIFI_AP);

  //WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  if (strlen(password) < 8)
    WiFi.softAP(ssid);
  else
    WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
  return true;
}

String WiFi_Init::get_MACid(){
    uint8_t baseMac[6];
    // Get MAC address for WiFi station
    esp_read_mac(baseMac, ESP_MAC_WIFI_STA);
    char baseMacChr[18] = {0};
    sprintf(baseMacChr, "%02X:%02X:%02X:%02X:%02X:%02X", baseMac[0], baseMac[1], baseMac[2], baseMac[3], baseMac[4], baseMac[5]);
    return String(baseMacChr);
}

#if!defined(NO_GLOBAL_INSTANCES) && !defined(NO_GLOBAL_EEPROM)
WiFi_Init Wifi_custom;
#endif
