#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  if (!mpu.begin()) {
    Serial.println("MPU6050 not found!");
    while (1);
  }
}

void loop() {
  // Flex sensors on ESP32 ADC pins
  int f1 = analogRead(34);
  int f2 = analogRead(35);
  int f3 = analogRead(32);
  int f4 = analogRead(33);
  int f5 = analogRead(25);

  // Gyro
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Print CSV row
  Serial.print(f1); Serial.print(",");
  Serial.print(f2); Serial.print(",");
  Serial.print(f3); Serial.print(",");
  Serial.print(f4); Serial.print(",");
  Serial.print(f5); Serial.print(",");
  Serial.print(g.gyro.x); Serial.print(",");
  Serial.print(g.gyro.y); Serial.print(",");
  Serial.println(g.gyro.z);

  delay(50); // ~20 samples/sec
}
