//DFRobot.com
//Compatible with the Arduino IDE 1.0
//Library version:1.1
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#if defined(ARDUINO) && ARDUINO >= 100
#define printByte(args)  write(args);
#else
#define printByte(args)  print(args,BYTE);
#endif

uint8_t bell[8]  = {0x4, 0xe, 0xe, 0xe, 0x1f, 0x0, 0x4};
uint8_t note[8]  = {0x2, 0x3, 0x2, 0xe, 0x1e, 0xc, 0x0};
uint8_t clock[8] = {0x0, 0xe, 0x15, 0x17, 0x11, 0xe, 0x0};
uint8_t heart[8] = {0x0, 0xa, 0x1f, 0x1f, 0xe, 0x4, 0x0};
uint8_t duck[8]  = {0x0, 0xc, 0x1d, 0xf, 0xf, 0x6, 0x0};
uint8_t check[8] = {0x0, 0x1, 0x3, 0x16, 0x1c, 0x8, 0x0};
uint8_t cross[8] = {0x0, 0x1b, 0xe, 0x4, 0xe, 0x1b, 0x0};
uint8_t retarrow[8] = {	0x1, 0x1, 0x5, 0x9, 0x1f, 0x8, 0x4};

const uint8_t nchars = 20;
const uint8_t nlines = 4;

// set the LCD address to 0x27 for a 20 chars and 4 line display
LiquidCrystal_I2C lcd(0x27, nchars, nlines);

void setup() {
  lcd.init();                      // initialize the lcd
  lcd.backlight();

  lcd.createChar(0, bell);
  lcd.createChar(1, note);
  lcd.createChar(2, clock);
  lcd.createChar(3, heart);
  lcd.createChar(4, duck);
  lcd.createChar(5, check);
  lcd.createChar(6, cross);
  lcd.createChar(7, retarrow);
  lcd.home();

  lcd.print("Hello world...");
  lcd.setCursor(0, 1);
  lcd.print(" i ");
  lcd.printByte(3);
  lcd.print(" RePhone!");
  delay(5000);
  displayKeyCodes();
}

// display all keycodes
void displayKeyCodes(void) {
  uint8_t c = 0;
  while (1) {
    lcd.clear();
    lcd.print(c == 0 ? "Codes 0x00" : "Codes 0x");
    lcd.print(c, HEX);
    for (int i = 1; i < nlines && c != 0xFF; i++) {
      lcd.setCursor(0, i);
      for (int j = 0; j < nchars && c != 0xFF; j++)
        lcd.printByte(c++);
    }
    if (c == 0xFF) {
      lcd.printByte(c);
      c = 0;
    }
    lcd.setCursor(10, 0);
    lcd.print("-0x");
    lcd.print(c == 0 ? 0xFF : c - 1, HEX);
    delay(5000);
  }
}

void loop() {
}
