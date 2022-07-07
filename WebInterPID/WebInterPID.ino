#include "header.h"

void setup() {
  Serial.begin(115200);
  Serial.println("Press button in 5 sec to erase FLASH.");
  pinMode(flashPin, INPUT_PULLUP);

  int counter = millis();
  while ( millis() - counter < 5000) {
    if (digitalRead(flashPin) == LOW)
    {
      Serial.println("Erasing...");
      Wifi_custom.clear_credential();
      delay(2000);
      Serial.println("Reboot");
      ESP.restart();
    }
  }

    // Initialize SPIFFS
  if(!SPIFFS.begin(true)){
    Serial.println("An Error has occurred while mounting SPIFFS");
    return;
  }
  
  
  if(Wifi_custom.check_credential(&wifi_settings) == false){
  /***********************WIFI SOFT AP FOR CONF*********************/
  Wifi_custom.set_wifi_ap("Configure_Device", "12345678");
 
  server.on("/", HTTP_GET, [](){
    if(!handleFileRead("/config.html")) server.send(404, "text/plain", "FileNotFound");
  });
  server.on("/Configuration", handle_OnReceiveParam);
  server.begin();
  while(1)  server.handleClient();
  /****************************************************************/
  }else{
  /****************WIFI INIT CONNECTION TO NETWORK****************/
    //Wifi_custom.sleep_wifi();
    delay(1000);   
    
    if( strlen(wifi_settings.ip) != 0 && strlen(wifi_settings.subnet) !=0 && strlen(wifi_settings.gw) !=0 ){
      Wifi_custom.conf_static_settings(wifi_settings.ip,wifi_settings.gw,wifi_settings.subnet);
    }

    connection_state = Wifi_custom.setup_wifi(wifi_settings.ssid,wifi_settings.ssidpwd,retry);

    if (connection_state == true ) {
    while (connection_state == true){
      Serial.println("Fail!");
      connection_state = Wifi_custom.setup_wifi(wifi_settings.ssid,wifi_settings.ssidpwd,retry);
    }
    } else {
    Serial.print("Connect to: ");
    Serial.println(wifi_settings.ssid);
    server.on("/", HTTP_GET, [](){
    if(!handleFileRead("/index.html")) server.send(404, "text/plain", "FileNotFound");
    });
    server.on("/tup", handle_tup);
    server.on("/tminus", handle_tminus);
    server.on("/sel", handle_sel);
    server.on("/prog", handle_prog);
    server.begin();
    }
  }  
  /****************************************************************/
}
void loop() {
   server.handleClient();
  /*************DO WHAT YOU WANT*******************************/
}

void handle_tup(){
    server.send(200, "text/html");
}
void handle_tminus(){
    server.send(200, "text/html");
}
void handle_sel(){
    server.send(200, "text/html");
}
void handle_prog(){
    server.send(200, "text/html");
}

void handle_OnReceiveParam(){

#if DEBUG == 1
  Serial.println(server.arg("bname"));
  Serial.println(server.arg("ssid"));
  Serial.println(server.arg("ssidpwd"));
  Serial.println(server.arg("mqttaddr"));
  Serial.println(server.arg("mqttport"));
  Serial.println(server.arg("mqttuser"));
  Serial.println(server.arg("mqttpwd"));
  //Serial.println(server.arg("dhcp"));
  Serial.println(server.arg("ip"));
  Serial.println(server.arg("subnet"));
  Serial.println(server.arg("gw")); 
#endif
  
  server.arg("bname").toCharArray(wifi_settings.bname,server.arg("bname").length()+1  );  
  server.arg("ssid").toCharArray(wifi_settings.ssid,server.arg("ssid").length()+1    );   
  server.arg("ssidpwd").toCharArray(wifi_settings.ssidpwd,server.arg("ssidpwd").length() +1   );
  server.arg("mqttaddr").toCharArray(wifi_settings.mqttaddr,server.arg("mqttaddr").length()+1  ); 
  server.arg("mqttport").toCharArray(wifi_settings.mqttport,server.arg("mqttport").length()+1  );  
  server.arg("mqttuser").toCharArray(wifi_settings.mqttuser,server.arg("mqttuser").length()+1  );    
  server.arg("mqttpwd").toCharArray(wifi_settings.mqttpwd,server.arg("mqttpwd").length() +1   );  
  server.arg("ip").toCharArray(wifi_settings.ip,server.arg("ip").length()+1       );
  server.arg("subnet").toCharArray(wifi_settings.subnet,server.arg("subnet").length()+1     );
  server.arg("gw").toCharArray(wifi_settings.gw,server.arg("gw").length()+1       );
  
  Wifi_custom.initialize_credential_fromWebpage(&wifi_settings);
  server.send(200, "text/html");
  
}
void handle_Conf(String myFile) {
    
    if (SPIFFS.exists(myFile)) {
      Serial.println(F("myFile founded on   SPIFFS"));
      
      File file = SPIFFS.open(myFile, "r");    
      
      size_t sent = server.streamFile(file, "text/css");
      file.close();
    }
}
String getContentType(String filename){
  if(server.hasArg("download")) return "application/octet-stream";
  else if(filename.endsWith(".htm")) return "text/html";
  else if(filename.endsWith(".html")) return "text/html";
  else if(filename.endsWith(".css")) return "text/css";
  else if(filename.endsWith(".js")) return "application/javascript";
  else if(filename.endsWith(".png")) return "image/png";
  else if(filename.endsWith(".gif")) return "image/gif";
  else if(filename.endsWith(".jpg")) return "image/jpeg";
  else if(filename.endsWith(".ico")) return "image/x-icon";
  else if(filename.endsWith(".xml")) return "text/xml";
  else if(filename.endsWith(".pdf")) return "application/x-pdf";
  else if(filename.endsWith(".zip")) return "application/x-zip";
  else if(filename.endsWith(".gz")) return "application/x-gzip";
  return "text/plain";
}
bool handleFileRead(String path){
  Serial.println("handleFileRead: " + path);
  if(path.endsWith("/")) path += "index.htm";
  String contentType = getContentType(path);
  String pathWithGz = path + ".gz";
  if(SPIFFS.exists(pathWithGz) || SPIFFS.exists(path)){
    if(SPIFFS.exists(pathWithGz))
      path += ".gz";
    File file = SPIFFS.open(path, "r");
    size_t sent = server.streamFile(file, contentType);
    file.close();
    return true;
  }
  return false;
}
