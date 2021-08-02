import processing.serial.*;
Serial myPort;  // The serial port
int lf = 10;    // Linefeed in ASCII
String myString = null;
float x,y,angle;
float num;
float num2;
int i = 0;
String val;

public void settings() {
    
  size(820, 820);
  noSmooth();
}

void setup() {
  // List all the available serial ports
  printArray(Serial.list());
  // Open the port you are using at the rate you want:
  myPort = new Serial(this, Serial.list()[0], 9600);

  background(0);
  translate(410, 410);
  stroke(255);
  strokeWeight(3);  // Default
}

//void draw()
//{
//  if ( myPort.available() > 0) 
//  {  // If data is available,
//  val = myPort.readStringUntil('\n');         // read it and store it in val
//  } 
//println(val); //print it out in the console
//}


void draw() {
  
  while (myPort.available() > 0) {
    myString = myPort.readStringUntil('\n');
    myString = myString.substring(0, myString.length() - 2);
    if (myString != null) {
    String[] q = splitTokens(myString, " ; ");   
    
    
    num=float(q[1]);  // Converts and prints float
    num2 = float(q[0]);  // Converts and prints float
    
    //Pass from polars to cartesians adna dd 410 to be in the middle of the 820 by 820 screen. 
    angle = num * 0.0174533;
    if (num == 45){
      clear();
    }
    println(num2);
    x = (sin(angle)*num2 + 410);
    y = (cos(angle)*num2 + 410);
   
    }
    if(num == 0 )
    {
      background(0);    
      translate(410, 410);
    }
    point(x, y);
    
  }
  myPort.clear();
}
