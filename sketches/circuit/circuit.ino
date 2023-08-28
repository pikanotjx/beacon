/*
  This sketch is based on the Arduino example "Fade" by David A. Mellis that 
  is publically available.
  
  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Fade
*/

int led = 2;         // The PWM pin the LED is attached to
int data;            // Any data received from the serial port
int brightness = 0;  // The brightness of the LED (0-255)
int fadeAmount = 5;  // The amount to fade the LED by

// Runs once at the beginning of the sketch and at every reset
void setup() {
  // Sets up the circuit (e.g., sets pin modes, initializes variables, etc.)
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  digitalWrite(LED_BUILTIN, LOW);
}

// Runs over and over again forever
void loop() {
  // Runs as long as there is serial data available to read
  while ( Serial.available() )
  {
    data = Serial.read();
    Serial.println(data);

    if (data == 49)
    {
      analogWrite(led, brightness); 

      if (brightness > 0)
      {
        brightness = brightness - fadeAmount;
      }
        
      delay(15);
    }
    else 
    {
      // set the brightness of pin 9:
      analogWrite(led, brightness);

      // change the brightness for next time through the loop:
      if (brightness < 255)
      {
        brightness = brightness + fadeAmount;
      }

      delay(15);
    }
    
    // else
    // {
    //   brightness = brightness + fadeAmount;
    // 
    //   // reverse the direction of the fading at the ends of the fade:
    //   if (brightness <= 0 || brightness >= 255) {
    //     fadeAmount = -fadeAmount;
    //   }
    //   // wait for 30 milliseconds to see the dimming effect
    //   delay(30);
    // }    
  }
}
