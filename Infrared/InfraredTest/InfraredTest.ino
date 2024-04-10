int count = 1;
const int button = 10;
void setup()
{
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  pinMode(sw, INPUT);
}

void loop()
{
  if(digitalRead(button == HIGH)
  {
  	count++;
  }
     
  int sense = analogRead(A0);
  if(sense > 500 || count % 2 == 0)
  {
    Serial.println("0");
  }
  else
  {
    Serial.println("1");
  }
  delay(1000);
}