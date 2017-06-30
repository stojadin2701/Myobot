#include "NewPing.h"

//Pins for enabling motor control
const unsigned char ENABLE_PINS[] = {7, 8};

const unsigned char ENABLE_PINS_NUM = sizeof(ENABLE_PINS)/sizeof(unsigned char);

const unsigned char MOTOR_PINS[] = {5, 6, 9, 10};

int ZERO_POWERS[] = {0, 0, 0, 0};

const unsigned char MOTOR_PINS_NUM = sizeof(MOTOR_PINS)/sizeof(unsigned char);

const unsigned char DISTANCE_TRIG_PIN = 2;

const unsigned char DISTANCE_ECHO_PIN = 4;

const unsigned char LIGHTS_PIN = 12;

const unsigned char MAX_DISTANCE = 100;

const unsigned long TIMEOUT = 1000;
const unsigned long DEFAULT_TIMEOUT = 300000;
const unsigned long MOTOR_POWERS_TIMEOUT = 500;
const unsigned long HEARTBEAT_TIMEOUT = 1000;


enum Command { START = 1, DISTANCE_ON, GET_DISTANCE, DISTANCE_OFF, SET_MOTORS, LIGHTS_ON, LIGHTS_OFF, HEARTBEAT, END};

unsigned char received_command = 0;

unsigned long last_heartbeat = millis();

String received_string;

NewPing sonar(DISTANCE_TRIG_PIN, DISTANCE_ECHO_PIN, MAX_DISTANCE);

boolean off = true;

unsigned int ping_speed = 60;
unsigned long ping_timer;

String last_distance = "---";

boolean device_ready = false;

boolean going_forward = false;

boolean motors_running = false;

boolean measure_distance = false;

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
	going_forward = powers[0] != 0 && powers[2] != 0 && powers[1] == 0 && powers[3] == 0;
	motors_running = powers[0] != 0 || powers[1] != 0 || powers[2] != 0 || powers[3] != 0;
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
	
	pinMode(LIGHTS_PIN, OUTPUT);
	
	pinMode(LED_BUILTIN, OUTPUT);

    Serial.begin(9600); // set the baud rate
    ping_timer = millis();
	//Serial.setTimeout(TIMEOUT);
    Serial.setTimeout(DEFAULT_TIMEOUT);
}

void echo_check(){
    //mozda i ovde going_forward &&
    if(sonar.check_timer()){
        if(going_forward && sonar.ping_result/US_ROUNDTRIP_CM < 25) {
            emergency_stop();
            Serial.println("Stopping motors!");
        }
		last_distance = String(sonar.ping_result/US_ROUNDTRIP_CM);
        //send_distance_info(last_distance);
    }
}

void emergency_stop(){
	if(motors_running){
		write_motor_powers(ZERO_POWERS, MOTOR_PINS_NUM);
	}
}

void send_distance_info(String info){
    //if(device_ready){
    //    Serial.println("&"+info);
    //}
	if(going_forward) Serial.println("&"+info);
}

void loop() {
    if ((device_ready && (going_forward || measure_distance)) && millis() >= ping_timer){
        ping_timer += ping_speed;
        sonar.ping_timer(echo_check);
    }
	
	if (millis() - last_heartbeat > HEARTBEAT_TIMEOUT){
		emergency_stop();
		digitalWrite(LED_BUILTIN, LOW);
		/*digitalWrite(LED_BUILTIN, HIGH);
		delay(50);
		digitalWrite(LED_BUILTIN, LOW);
		delay(50);
		digitalWrite(LED_BUILTIN, HIGH);
		delay(50);
		digitalWrite(LED_BUILTIN, LOW);
		delay(50);
		digitalWrite(LED_BUILTIN, HIGH);
		delay(50);
		digitalWrite(LED_BUILTIN, LOW);
		*/
	}

	//Serial.println("...");
	
    if(Serial.available()) {
        received_string = Serial.readStringUntil('\n'); // read the incoming data
        //Serial.print("Received: ");
        //Serial.println(received_string);
        switch(received_string.substring(0, 1).toInt()){
			case START: {
				Serial.println("Ready");
				device_ready = true;
				break;
			}
			case DISTANCE_ON: {
				measure_distance = true;
				break;
			}
			case GET_DISTANCE: {
				Serial.println("&" + last_distance);
				break;
			}
			case DISTANCE_OFF: {
				measure_distance = false;
				break;
			}
			case SET_MOTORS: {
				signed char left_power, right_power;
				int first_delimiter = received_string.indexOf(';');
				int second_delimiter = received_string.indexOf(',');				
				left_power = received_string.substring(first_delimiter+1, second_delimiter).toInt();
				right_power = received_string.substring(second_delimiter+1).toInt();
				set_motor_powers(left_power, right_power);
				break;
			}
			case LIGHTS_ON: {
				Serial.println("Lights on...");
				digitalWrite(LIGHTS_PIN, HIGH);
				break;
			}
			case LIGHTS_OFF: {
				Serial.println("Lights off...");
				digitalWrite(LIGHTS_PIN, LOW);
				break;
			}
			case HEARTBEAT: {
				last_heartbeat = millis();				
				digitalWrite(LED_BUILTIN, off ? HIGH : LOW);
				off=!off;
				//Serial.println("Heartbeat received <3");
				break;
			}
			case END:{
				emergency_stop();
				device_ready = false;
				measure_distance = false;
				Serial.println("Bye.");				
				break;
			}
			default: {
				emergency_stop();
				Serial.println("COMMAND UNKNOWN: "+received_string);
				//Serial.println("COMMAND UNKNOWN");
				//device_ready = false;
				break;
			}
        }
    }

}
