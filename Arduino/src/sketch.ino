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


void set_motor_powers(signed char left_power, signed char right_power){
	if (left_power < -100 || left_power > 100 || right_power < -100 || right_power > 100) return;

//	Serial.println(left_power);
//	Serial.println(right_power);

	int lp = 256*left_power/100;
	int rp = 256*right_power/100;

//	Serial.println(lp);
//	Serial.println(rp);

	int powers[] = {lp, 0, rp, 0};
	
//	Serial.println(powers[0]);
//	Serial.println(powers[1]);
//	Serial.println(powers[2]);
//	Serial.println(powers[3]);

	if (left_power < 0){
		powers[0] = 0;
		powers[1] = -lp;
	}
	if (right_power < 0){
		powers[2] = 0;
		powers[3] = -rp;
	}
	for(unsigned char i = 0; i < sizeof(MOTOR_PINS)/sizeof(unsigned char); i++){
//		Serial.println(powers[i]);
		analogWrite(MOTOR_PINS[i], powers[i]);
	}
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

/*	analogWrite(MOTOR_PINS[0], 200);
	analogWrite(MOTOR_PINS[1], 0);
	analogWrite(MOTOR_PINS[2], 200);
	analogWrite(MOTOR_PINS[3], 0);

	delay(1000);

	analogWrite(MOTOR_PINS[0], 0);
	analogWrite(MOTOR_PINS[2], 0);
*/
	while(Serial.available()==0);
	received_command = Serial.read();
	if(received_command == START){
		Serial.println("Ready");
	}
}

void loop() {
	if(Serial.available()){ 
		received_command = Serial.read(); // read the incoming data
		switch(received_command){
			case REQUEST_DISTANCE: {
				//Serial.println("DISTANCE REQUESTED");
				Serial.println(read_distance());
		 		break;
				}
			case SET_MOTORS: {
		       		//Serial.println("SETTING MOTOR POWERS");
				signed char left_power, right_power;
				left_power = Serial.read() - 100;	//return to the original range [-100%,100%] 
				right_power = Serial.read() - 100;
				set_motor_powers(left_power, right_power);
		//		Serial.println(left_power);
		//		Serial.println(right_power);
				break;
				 }
			default: {
				Serial.println("COMMAND UNKNOWN");
				break;
				 }
		}
	}
	delay(100); // delay for 1/10 of a second
}
