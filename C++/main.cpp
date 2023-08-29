// https://github.com/jazz-2
#include <Arduino.h>
#include <WiFi.h>        //for ESP32
#include <WiFiGeneric.h> //for ESP32
// #include <WiFiNINA.h> //for Arduino NANO 33 IoT

const char *ssid = "WiFiName";     // WiFi name
const char *password = "password"; // WiFi password
const uint16_t port = 5004;
const char *hostIP = "?.?.?.?";    // IP address

#define LED_internal LED_BUILTIN

String ReceivedData = "";
const String WrongData = "00";
const String PhoneSensorDataRequest = "11";
const String ExpectedData = "22";

void LEDinfo()
{
  if (ReceivedData == ExpectedData)
  {
    for (uint8_t i = 0; i < 10; i++)
    {
      digitalWrite(LED_internal, HIGH);
      delay(100);
      digitalWrite(LED_internal, LOW);
      delay(100);
    }
  }
  else
  {
    for (uint8_t i = 0; i < 10; i++)
    {
      digitalWrite(LED_internal, HIGH);
      delay(500);
      digitalWrite(LED_internal, LOW);
      delay(50);
    }
  }
}

void WiFiSendReceive()
{
  static String message = PhoneSensorDataRequest;

  WiFiClient client;

  if (!client.connect(hostIP, port))
  {
    Serial.println("Connection to host failed! WiFi turned on? Try to reopen Python program");
    delay(1000);
    return;
  }

  client.print(message); // send data to the computer
  Serial.println("Connection to the server was successful!");

  while (ReceivedData != ExpectedData)
  {
    int i_read = 0;
    static int wait = 1000;
    static const int BufferSize = 256;
    char ReciveBuffer[BufferSize] = {'\0'};

    for (int i = 0; i <= wait; i++)
    {
      while (client.available())
      {
        ReciveBuffer[i_read] = client.read(); // receiving data
        i_read++;
        i = wait;
      }
      delay(1);
    }

    if (ReciveBuffer[0] == '\0')
    {
      static bool toogleLED = false;
      digitalWrite(LED_internal, toogleLED = !toogleLED);
      Serial.print("Waiting for message from the computer...\n");
    }
    else
    {
      client.stop();
      Serial.println("Client disconnected...");

      Serial.print("Data received from the computer: ");
      for (int i = 0; i < i_read; i++)
      {
        Serial.print(ReciveBuffer[i]);
      }
      ReceivedData = (String)ReciveBuffer;
      Serial.print('\n');

      if (ReceivedData == WrongData)
      {
        Serial.println("Computer received wrong data!");
        break;
      }
    }
  }
}

void setup()
{

  Serial.begin(115200);
  pinMode(LED_internal, OUTPUT);
}

void loop()
{

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("WiFi connection attempt");
    delay(4000);
  }
  Serial.println("Connected to the WiFi");
  WiFiSendReceive();
  WiFi.disconnect(true, true); // for ESP32
  WiFi.mode(WIFI_OFF);         // for ESP32
  // WiFi.end();                  // for Arduino NANO 33 IoT
  LEDinfo();

  ReceivedData = "";
  delay(5000);
}
