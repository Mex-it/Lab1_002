#include "Arduino.h" // Stupid arduino lib and minimalized sprintf buf!

// Buffers
char buf[30];
char tBuf[10];
char hBuf[10];

// Values
float temp = 20.01;
float humid = 1.01;

void setup()
{
  Serial.begin(115200);

  delay(2500); // Delay after reset (DTS)
}

void loop()
{
  dtostrf(temp, 4, 2, tBuf);
  dtostrf(humid, 4, 2, hBuf);

  sprintf(buf, "%s,%s\n", tBuf, hBuf); // Build

  Serial.print(buf); // Send
}
