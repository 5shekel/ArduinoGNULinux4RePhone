/*
 * Blink
 * Turns on an LED on for one second, then off for one second, repeatedly
 * and changes color every 20 seconds.
 */

#define LED_R 18
#define LED_G 17
#define LED_B 16

const int led[] = { LED_R, LED_G, LED_B };

// the setup function runs once when you press reset or power the board
void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(led[i], OUTPUT);    // initialize LEDs as output
    digitalWrite(led[i], HIGH); // HIGH (LOW is full color, HIGH is off)
  }
}

// the loop function runs over and over again forever
void loop() {
  // change color every 20 seconds
  for (int i = 0; i < 3; i++) {
    for (int c = 0; c < 10; c++) {
      digitalWrite(led[i], LOW); // turn the LED on
      delay(1000);               // wait for a second
      digitalWrite(led[i], HIGH);// turn the LED off
      delay(1000);               // wait for a second
    }
  }
}
