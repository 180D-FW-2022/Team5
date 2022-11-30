void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  String d1str;
  String d2str;
  while (Serial2.available()){
    d1str = Serial2.readString();  //read until timeout
    d1str.trim(); 
    d1str = "D1-" + d1str + '\n';
    Serial1.print(d1str);
    Serial.println(d1str);
  }
  while (Serial3.available()){
    d2str = Serial3.readString();
    d2str.trim();
    d2str = "D2-" + d2str + '\n';
    Serial1.print(d2str);
    Serial.println(d2str);
  }
  
}
