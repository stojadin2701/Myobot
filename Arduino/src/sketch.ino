//Pins for enabling motor control
const unsigned char ENABLE_PINS[] = {7, 8};

const unsigned char MOTOR_PINS[] = {5, 6, 9, 10};

const unsigned char DISTANCE_TRIG_PIN = 2;

const unsigned char DISTANCE_ECHO_PIN = 4;

const unsigned char DISTANCE_SAMPLING_NUM = 3;

enum Command { START, REQUEST_DISTANCE, SET_MOTORS };

unsigned char received_command = 0;

long microsecondsToCentimeters(long duration){
	return duration/29/2;
}

long read_distance(){
	long duration;
	long sum = 0;

	for(int i = 0; i < DISTANCE_SAMPLING_NUM; i++){
		digitalWrite(DISTANCE_TRIG_PIN, LOW);
		delayMicroseconds(2);
		digitalWrite(DISTANCE_TRIG_PIN, HIGH);
		delayMicroseconds(10);

		digitalWrite(DISTANCE_TRIG_PIN, LOW);

		duration = pulseIn(DISTANCE_ECHO_PIN, HIGH);
		sum+=microsecondsToCentimeters(duration);
		delay(35);
	}
	return sum/DISTANCE_SAMPLING_NUM;
	//return microsecondsToCentimeters(duration);
}


void set_motor_powers(signed char left_power, signed char right_power){
	if (left_power < -100 || left_power > 100 || right_power < -100 || right_power > 100) return;

	int lp = 256*left_power/100;
	int rp = 256*right_power/100;

	int powers[] = {lp, 0, rp, 0};

	if (left_power < 0){
		powers[0] = 0;
		powers[1] = -lp;
	}
	if (right_power < 0){
		powers[2] = 0;
		powers[3] = -rp;
	}
	for(unsigned char i = 0; i < sizeof(MOTOR_PINS)/sizeof(unsigned char); i++){
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

  //  set_motor_powers(-80, -80);
  //  delay(1000);
  //  set_motor_powers(0, 0);

 /* 	int powers[] = {200, 0, 200, 0};

	for(unsigned char i = 0; i < sizeof(MOTOR_PINS)/sizeof(unsigned char); i++){
		analogWrite(MOTOR_PINS[i], powers[i]);
	}
 
    delay(1000);

	for(unsigned char i = 0; i < sizeof(MOTOR_PINS)/sizeof(unsigned char); i++){
		analogWrite(MOTOR_PINS[i], 0);
	}
*/


	Serial.begin(9600); // set the baud rate
    
//	while(Serial.available()==0);
//	received_command = Serial.read();
//	if(received_command == START){
//		Serial.println("Ready");
//	}
}

void loop() {
//	delay(100);
	if(Serial.available()){ 
		received_command = Serial.read(); // read the incoming data
		switch(received_command){
            case START: {
                Serial.println("Ready");
                break;
            }
			case REQUEST_DISTANCE: {
				Serial.println(read_distance());
		 		break;
			}
			case SET_MOTORS: {
				signed char left_power, right_power;
                while(Serial.available() == 0);
				left_power = Serial.read() - 100;	//return to the original range [-100%,100%] 
                while(Serial.available() == 0);
				right_power = Serial.read() - 100;
				set_motor_powers(left_power, right_power);
                //Serial.println("Powers sent");
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
