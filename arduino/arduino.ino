const int sensorPin = 6;
int sensorState = 0;
unsigned long time = 0;
int shakes = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(sensorPin, INPUT);
  Serial.begin(9600);

}

void loop() {
  sensorState = digitalRead(sensorPin);
  
  shakes = shakes + sensorState;
  if (shakes >= 100) {
    shakes = 100;
  }

  if (millis() - time >= 500) {
    Serial.println(shakes);
    shakes = 0;
    time = millis();
  }
  delay(10);
}
