# Read data from the phone's sensors, display them and communicate with the microcontroller

[*github.com/jazz-2*](https://github.com/jazz-2)

------------------
## Demonstration of sensor data reading
![phoneSensors.gif](https://github.com/jazz-2/PhoneSensors_PC_MCU/assets/141406828/e55825de-a654-46ca-96a3-3fec587b71e2)


**Tested on Arduino NANO 33 IoT, ESP32.**

------------------
### Description
This project contains **Python** and __C++__ code that allows you to read data from your phone's sensors (accelerometer, gyroscope, magnetometer, pressure, etc.) using Android apps such as:
* [*Sensorstream IMU+GPS*](https://play.google.com/store/apps/details?id=de.lorenz_fenster.sensorstreamgps)
* [*Wireless IMU*](https://play.google.com/store/apps/details?id=org.zwiener.wimu)

The microcontroller sends information to the computer to start monitoring the sensor data, and then the computer notifies the microcontroller when the sensor exceeds a set threshold `sensorTreshold`.

### Notes
* The computer, microcontroller and phone should be connected to the same WiFi network.
* You can find your computer IP address by running `ipconfig` in Command Prompt.
