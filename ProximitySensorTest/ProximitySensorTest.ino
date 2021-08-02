
#include <Servo.h>
// defines variables
int c;


class eye {
  public:
    Servo servo;
    int trigPin;
    int echoPin;
    int servoPin;
    int currentAngle;
    int minAngle;
    int maxAngle;
    int stepVal;
    void setAtt(int intrigPin, int inechoPin, int inservoPin, int inminAngle, int inmaxAngle, int instepVal){
      trigPin = intrigPin;
      echoPin = inechoPin;
      servoPin = inservoPin;
      minAngle = inminAngle;
      maxAngle = inmaxAngle;
      currentAngle = inminAngle;
      stepVal = instepVal;
      servo.attach(servoPin);
      pinMode(trigPin, OUTPUT);
      pinMode(echoPin, INPUT);
      servo.write(minAngle);
      while (servo.read() != minAngle) {
        delay(100);
      }
    }
    
    int getDistance()
    {
      long duration;
      int distance;
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin  , HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      duration = pulseIn(echoPin, HIGH);
      distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
      return distance;

    }
    void loopstep()
    {
      
      currentAngle = currentAngle + stepVal;
      servo.write(currentAngle);
      if ((currentAngle == minAngle) || (currentAngle == maxAngle )) {
                stepVal = stepVal * -1;
                c = c + 1;
    }
  }
};



int numproxy =2;
eye eyeList[2];

void setup() {
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed\
  //Create eye instances (trig echo servo)
  eyeList[0].setAtt(33,31, 28, 10, 80, 1);
  eyeList[1].setAtt(45,43,42,10, 80,1);
  //eyeList[2].setAtt(37,35,34,10, 80,1);
  //eyeList[3].setAtt(41,39,38,10, 80,1);
}

void loop() {
  //INCLUDE RESET AT C = numproxy
  if (c == numproxy){
    Serial.println("ResetFlag");
    c = 0;
  }
  for(int i=0; i < numproxy; i++) { 
    eyeList[i].loopstep();
    
    Serial.print(eyeList[i].getDistance());
    Serial.print(":");
    Serial.print(eyeList[i].currentAngle);
    Serial.print(";");
    
  }
  Serial.println("");
  delay(100);


}
