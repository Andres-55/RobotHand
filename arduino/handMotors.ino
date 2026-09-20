#include <Servo.h>

Servo s1;
Servo s2;
Servo s3;
Servo s4;
Servo s5;

void setup() {
  Serial.begin(9600);
  s1.attach(3);
  s2.attach(5);
  s3.attach(6);
  s4.attach(9);
  s5.attach(10);
}

void loop() {
  if (Serial.available() >= 5) {
    int angle1 = Serial.parseInt();
    int angle2 = Serial.parseInt();
    int angle3 = Serial.parseInt();
    int angle4 = Serial.parseInt();
    int angle5 = Serial.parseInt();

    // Basic angle range check (0–180) for each
    if (angle1 >= 0 && angle1 <= 180)
    {
      s1.write(angle1);
    }

    if(angle2 >= 0 && angle2 <= 180)
    {
      s2.write(angle2);
    }

    if(angle3 >= 0 && angle3 <= 180)
    {
      s3.write(angle3);
    }

    if(angle4 >= 0 && angle4 <= 180)
    {
      s4.write(angle4);
    }

    if(angle5 >= 0 && angle5 <= 180)
    {
      s5.write(angle5);
    }
  }
}