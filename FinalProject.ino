#include <Arduino_APDS9960.h>
#include <Arduino_LPS22HB.h>

/*
  User defined variables
*/
float tempThreshold = 50;         // Minimum temperature (f) to send alerts
int minSecsFromFirstAlert = 300;  // 5 min
int minSecsBetweenEmails = 60;    // 1 min

// true - receive alerts when above tempThreshold
// false - do not factor temperature into alerts
bool alertOnTemp = true;

// true - receive alerts when second motion has not been detected within minSecsFromFirstAlert
// false - do not factor second motion into alerts
bool alertOnSecondMotion = true;

/*
  Program variables
*/
long lastMotion = -minSecsFromFirstAlert * 1000; // Initiliaze to large negative value
long lastSend = -minSecsBetweenEmails * 1000; // Initiliaze to large negative value
bool firstMotionDetected = false; // Flip counter used for second motion alert

void setup() {
  Serial.begin(9600); // Initiliaze serial connection
  while (!Serial)
    ;
  if (!BARO.begin()) {
    Serial.println("Failed to initialize pressure sensor!");
      ;
  }
  if (!APDS.begin()) {
    Serial.println("Error initializing APDS9960 sensor!");
  }
}

void loop() {
  unsigned long now = millis(); // Initiliaze time passed
  float pressure = BARO.readPressure(); // Read pressure. Necessary for deriving temperature.
  float temperature_C = BARO.readTemperature(); // Get temperature in Celsius
  float temperature_F = ((temperature_C * 1.8) + 32); //  Convert to Fahrenheit

  if (APDS.proximityAvailable()) { // If proximity is working
    // read the proximity
    // - 0   => close
    // - 255 => far
    // - -1  => error
    int proximity = APDS.readProximity();

    if (proximity >= 0 && proximity <= 230) { // If motion detected
      if (now > (lastSend + minSecsBetweenEmails * 1000)) { // If more than minSecsBetweenEmails has passed since last 
                                                            // motion alert
        if (alertOnTemp && temperature_F >= tempThreshold) { // If temperature alerts are on and ambient temperature 
                                                             // is above threshold
          Serial.print("TEMPERATURE MOVEMENT");
          Serial.print(",");
          Serial.print(tempThreshold);
          Serial.print(",");
          Serial.println(temperature_F);
        } 
        else { // Motion detected but temperature not evaluated
          Serial.println("MOVEMENT");
        }
        lastSend = now; // Update lastSend time for cooldown between alerts
      } 
      else { // Motion detected but cooldown has not elapsed
        Serial.println("TOO SOON");
      }
      lastMotion = now; // Update lastMotion time for cooldown between alerts
      firstMotionDetected = !firstMotionDetected; // Flip flag. First motion will be true and second motion back to false.
    } 
    // If second motion alert is on, motion is first time, and more tha nminSecsFromFirstAlert has passed since last motion
    else if (alertOnSecondMotion && firstMotionDetected && (now > (lastMotion + minSecsFromFirstAlert * 1000))) { 
      Serial.println("SECOND MOTION MISSED");
      // Reset lastMotion so alert pings every minSecsFromFirstAlert until second motion has been detected
      lastMotion = now;
    } 
    else { // Nothing is happening
      Serial.println("QUIET");
    }
  }
  delay(150);
}
