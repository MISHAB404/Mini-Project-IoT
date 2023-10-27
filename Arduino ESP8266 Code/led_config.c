#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "wifi-ssid";
const char* password = "wifi-password";

ESP8266WebServer server(80);
const int ledPin = D1;  

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/turnOn", HTTP_GET, []() {
    digitalWrite(ledPin, HIGH);
    server.send(200, "text/plain", "LED turned on");
  });

  server.on("/turnOff", HTTP_GET, []() {
    digitalWrite(ledPin, LOW);
    server.send(200, "text/plain", "LED turned off");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
