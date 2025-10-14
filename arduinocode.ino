
#include <SoftwareSerial.h>
#include "DFRobot_C4001.h"
#include <MPU6050_tockn.h>
#include <Wire.h>

// --- SENSOR OBJECTS ---
SoftwareSerial mySerial(8, 9); // RX, TX for Radar
DFRobot_C4001_UART radar(&mySerial, 9600);
MPU6050 mpu6050(Wire);

// --- PARAMETERS ---
const unsigned long PRINT_INTERVAL = 200;
long timer = 0;
const int MIN_ENERGY_THRESHOLD = 500;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);

  while (!radar.begin()) {
    delay(1000);
  }
  radar.setSensorMode(eSpeedMode);
  radar.setDetectThres(/*min*/15, /*max*/900, /*thres*/75);
  radar.setDelay(/*appear*/0.1, /*disappear*/0.5);
  radar.setFrettingDetection(eON);
}

void loop() {
  mpu6050.update();

  if (millis() - timer > PRINT_INTERVAL) {
    uint8_t targetNum = radar.getTargetNumber();
    int targetEnergy = radar.getTargetEnergy();

    // *** MODIFIED LOGIC: Send a clean, comma-separated data string ***
    if (targetNum > 0 && targetEnergy > MIN_ENERGY_THRESHOLD) {
      // Data format: status,dist,speed,energy,angleX,angleY,angleZ
      Serial.print("1,");
      Serial.print(radar.getTargetRange());
      Serial.print(",");
      Serial.print(radar.getTargetSpeed());
      Serial.print(",");
      Serial.print(targetEnergy);
      Serial.print(",");
      Serial.print(mpu6050.getAngleX());
      Serial.print(",");
      Serial.print(mpu6050.getAngleY());
      Serial.print(",");
      Serial.println(mpu6050.getAngleZ());
    } else {
      // Send '0' for "No Person Detected"
      Serial.println("0");
    }

    timer = millis();
  }
}
