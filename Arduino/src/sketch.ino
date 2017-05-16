
//Pins for enabling motor control
const unsigned char ENABLE_PINS[] = {7, 8};

const unsigned char MOTOR_PINS[] = {5, 6, 9, 10};

const unsigned char DISTANCE_TRIG_PIN = 2;

const unsigned char DISTANCE_ECHO_PIN = 4;

enum Command { START, REQUEST_DISTANCE, SET_MOTORS };

unsigned char received_command = 0;

long microsecondsToCentimeters(long duration){
	return duration/29/2;
}

long read_distance(){
	long duration;

	digitalWrite(DISTANCE_TRIG_PIN, LOW);
	delayMicroseconds(2);
	digitalWrite(DISTANCE_TRIG_PIN, HIGH);
	delayMicroseconds(10);

	digitalWrite(DISTANCE_TRIG_PIN, LOW);

	duration = pulseIn(DISTANCE_ECHO_PIN, HIGH);

	return microsecondsToCentimeters(duration);
}

void setup() {
	for (unsigned char i = 0; i < sizeof(ENABLE_PINS)/sizeof(unsigned char); i++){
		pinMode(ENABLE_PINS[i], OUTPUT);
		digitalWrite(ENABLE_PINS[i], HIGH);
	}

	for(unsigned char i = 0; i < sizeof(MOTOR_PINS)/sizeof(unsigned char); i++){
		pinMode(MOTOR_PINS[i], OUTPUT);
	}
	
	pinMode(DISTANCE_TRIG_PIN, OUTPUT);
	pinMode(DISTANCE_ECHO_PIN, INPUT);

	Serial.begin(9600); // set the baud rate
	//Serial.println("Ready"); // print "Ready" once
	while(Serial.available()==0);
	received_command = Serial.read();
	if(received_command == START){
		Serial.println("Ready");
	}
}

void loop() {
		if(Serial.available()){ // only send data back if data has been sent
		received_command = Serial.read(); // read the incoming data
		switch(received_command){
			case REQUEST_DISTANCE: {
				//Serial.println("DISTANCE REQUESTED");
				Serial.println(read_distance());
				break;
			}
			case SET_MOTORS: {
				Serial.println("SETTING MOTOR POWERS");
				break;
			}
			default: {
				Serial.println("COMMAND UNKNOWN");
				break;
			}
		}
		//Serial.println(inByte); // send the data back in a new line so that it is not all one long line
	}
	delay(100); // delay for 1/10 of a second

//	Serial.print(read_distance());
//	delay(100);

}
