/*
   Led Matrix controller via Serial Input.
   Based on the following library:
    - MaxMatrix.h: GitHub | riyas-org/max7219  https://github.com/riyas-org/max7219
*/
#include <MaxMatrix.h>
int DIN = 7;   // DIN pin of MAX7219 module
int CLK = 6;   // CLK pin of MAX7219 module
int CS = 5;    // CS pin of MAX7219 module
int maxInUse = 1; // Number of MAX7219 Modules
MaxMatrix m(DIN, CS, CLK, maxInUse);

void setup() {
  m.init(); // MAX7219 initialization
  m.setIntensity(8); // initial led matrix intensity, 0-15
  Serial.begin(9600); // Initialise Serial.
  //Serial.print("Initialised, Ready to Go\n");
}

/*
 * -----------
 * Data Format
 * -----------
 * Send 3 space seperated integers via serial.
 * [mode] + " " + [x co-ordinate] + " " + [y co-ordinate] + " "
 * 
 * Modes:
 * 0 - Clear Input.
 * 1 - Turn On LED.
 * 2 - Turn Off LED.
 */
void loop() {
  // Declare Variables for mode, x and y.
  int mode, x, y;

  // Check if Serial is available.
  if(Serial.available()){

    // Read mode
    mode = Serial.readStringUntil(' ').toInt();

    // If mode is 0, clear matrix.
    if(mode == 0) {
      Serial.println("Clearing Matrix");
      m.clear();
    // If mode is not 0, check and read x and y co-ordinates.
    } else {
      x = Serial.readStringUntil(' ').toInt();
      y = Serial.readStringUntil(' ').toInt();

      // Check boundary conditions for x and y.
      if(!(x >= 0 && x < 8 && y >= 0 && y < 8)) {
        Serial.print("Enter valid led co-ordinate\n");  
      // If x and y are valid.
      } else {
        // If mode is 1, turn on LED at (x, y)
        if(mode == 1) {
          Serial.print("Turning on led at ("); 
          m.setDot(y, x, true);
        // If mode is 2, turn off LED at (x, y)
        } else if (mode == 2) {
          Serial.print("Turning off led at (");
          m.setDot(y, x, false);
        }
        Serial.print(x);
        Serial.print(", ");
        Serial.print(y);
        Serial.print(")\n");
      }
    }
  }
  // Delay
  delay(100);
}
