#include "NewPing.h"

//Pins for enabling motor control
const unsigned char ENABLE_PINS[] = {7, 8};

const unsigned char ENABLE_PINS_NUM = sizeof(ENABLE_PINS)/sizeof(unsigned char);

const unsigned char MOTOR_PINS[] = {5, 6, 9, 10};

const unsigned char MOTOR_PINS_NUM = sizeof(MOTOR_PINS)/sizeof(unsigned char);

const unsigned char DISTANCE_TRIG_PIN = 2;

const unsigned char DISTANCE_ECHO_PIN = 4;

const unsigned char MAX_DISTANCE = 40;

enum Command { START, SET_MOTORS };

unsigned char received_command = 0;

String received_string;

NewPing sonar(DISTANCE_TRIG_PIN, DISTANCE_ECHO_PIN, MAX_DISTANCE);

unsigned int ping_speed = 50;
unsigned long ping_timer;

boolean device_ready = false;

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

    write_motor_powers(powers, MOTOR_PINS_NUM);

}

void write_motor_powers(int powers[], int pin_number){
    for(unsigned char i = 0; i < pin_number; i++){
		analogWrite(MOTOR_PINS[i], powers[i]);
	}
}

void setup() {
	for (unsigned char i = 0; i < ENABLE_PINS_NUM; i++){
		pinMode(ENABLE_PINS[i], OUTPUT);
		digitalWrite(ENABLE_PINS[i], HIGH);
	}

	for(unsigned char i = 0; i < MOTOR_PINS_NUM; i++){
		pinMode(MOTOR_PINS[i], OUTPUT);
	}

	pinMode(DISTANCE_TRIG_PIN, OUTPUT);
	pinMode(DISTANCE_ECHO_PIN, INPUT);

	Serial.begin(9600); // set the baud rate
    ping_timer = millis();
}

void echo_check(){
    if(sonar.check_timer()){
        if(sonar.ping_result/US_ROUNDTRIP_CM < 20) {
            int zero_arr[] = {0, 0, 0, 0};
            write_motor_powers(zero_arr, MOTOR_PINS_NUM);
        }
        //send_distance_info(String(sonar.ping_result));
    } else {
        //send_distance_info("...");
    }
}

void send_distance_info(String info){
    if(device_ready){
        Serial.println(info);
    }
}

void loop() {
    if(millis() >= ping_timer){
        ping_timer += ping_speed;
        sonar.ping_timer(echo_check);
    }

	if(Serial.available()){ 
		received_string = Serial.readStringUntil('\n'); // read the incoming data
        received_string = received_string.substring(0, received_string.length() - 1);
		switch(received_string.toInt()){
            case START: {
                Serial.println("Ready");
                device_ready = true;
                break;
            }
			case SET_MOTORS: {
                signed char left_power, right_power;
                received_string = Serial.readStringUntil('\n'); // read the incoming data
                received_string = received_string.substring(0, received_string.length() - 1);
                left_power = received_string.toInt();
                Serial.println(left_power);
                received_string = Serial.readStringUntil('\n'); // read the incoming data
                received_string = received_string.substring(0, received_string.length() - 1);
                right_power = received_string.toInt();
                Serial.println(right_power);
			    //while(Serial.available() == 0);
				//left_power = Serial.read() - 100;   //return to the original range [-100%,100%] 
                //while(Serial.available() == 0);
				//right_power = Serial.read() - 100;
				set_motor_powers(left_power, right_power);
                //Serial.println("Powers sent");
				break;
			}
			default: {
				Serial.println("COMMAND UNKNOWN");
                device_ready = false;
				break;
			}
		}
	}
	//delay(100); // delay for 1/10 of a second
}
