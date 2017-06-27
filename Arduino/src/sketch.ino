#include "NewPing.h"

//Pins for enabling motor control
const unsigned char ENABLE_PINS[] = {7, 8};

const unsigned char ENABLE_PINS_NUM = sizeof(ENABLE_PINS)/sizeof(unsigned char);

const unsigned char MOTOR_PINS[] = {5, 6, 9, 10};

int ZERO_POWERS[] = {0, 0, 0, 0};

const unsigned char MOTOR_PINS_NUM = sizeof(MOTOR_PINS)/sizeof(unsigned char);

const unsigned char DISTANCE_TRIG_PIN = 2;

const unsigned char DISTANCE_ECHO_PIN = 4;

const unsigned char MAX_DISTANCE = 80;

const unsigned long TIMEOUT = 1000;
const unsigned long DEFAULT_TIMEOUT = 300000;
const unsigned long MOTOR_POWERS_TIMEOUT = 500;
const unsigned long HEARTBEAT_TIMEOUT = 1000;


enum Command { START = 1, SET_MOTORS, HEARTBEAT };

unsigned char received_command = 0;

unsigned long last_heartbeat = millis();

String received_string;

NewPing sonar(DISTANCE_TRIG_PIN, DISTANCE_ECHO_PIN, MAX_DISTANCE);

boolean off = true;


unsigned int ping_speed = 50;
unsigned long ping_timer;

boolean device_ready = false;

boolean going_forward = false;

boolean motors_running = false;

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
	
	pinMode(LED_BUILTIN, OUTPUT);

    Serial.begin(9600); // set the baud rate
    ping_timer = millis();
	//Serial.setTimeout(TIMEOUT);
    Serial.setTimeout(DEFAULT_TIMEOUT);
}

void echo_check(){
    //mozda i ovde going_forward &&
    if(sonar.check_timer()){
        if(sonar.ping_result/US_ROUNDTRIP_CM < 20) {
            emergency_stop();
            Serial.println("Stopping motors!");
        }
        send_distance_info(String(sonar.ping_result/US_ROUNDTRIP_CM));
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
    if(/*device_ready &&*/ going_forward && millis() >= ping_timer){
        ping_timer += ping_speed;
        sonar.ping_timer(echo_check);
    }
	
	if (millis() - last_heartbeat > HEARTBEAT_TIMEOUT){
		emergency_stop();
		digitalWrite(LED_BUILTIN, HIGH);
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
	}

	//Serial.println("...");
	
    if(Serial.available()) {
        received_string = Serial.readStringUntil('\n'); // read the incoming data
        //Serial.print("Received: ");
        //Serial.println(received_string);
        switch(received_string.substring(0, 1).toInt()){
            case START: {
                Serial.println("Ready");
                //device_ready = true;
                break;
            }
            case SET_MOTORS: {
				signed char left_power, right_power;
				int first_delimiter = received_string.indexOf(';');
				int second_delimiter = received_string.indexOf(',');
				
				left_power = received_string.substring(first_delimiter+1, second_delimiter).toInt();
				right_power = received_string.substring(second_delimiter+1).toInt();
				//Serial.println("Left power: "+received_string.substring(first_delimiter+1, second_delimiter));
				//Serial.println("Right power: "+received_string.substring(second_delimiter+1));
				set_motor_powers(left_power, right_power);
				break;
                /*Serial.setTimeout(MOTOR_POWERS_TIMEOUT);
                signed char left_power, right_power;
                received_string = Serial.readStringUntil('\n'); // read the incoming data
                if (received_string.length()==0) {
					emergency_stop();
                    Serial.println("Setting motor powers timed out...");
                    Serial.setTimeout(DEFAULT_TIMEOUT);
                    break;
                }
                left_power = received_string.toInt();
                received_string = Serial.readStringUntil('\n'); // read the incoming data
                if (received_string.length()==0) {
					emergency_stop();
                    Serial.println("Setting motor powers timed out...");
                    Serial.setTimeout(DEFAULT_TIMEOUT);
                    break;
                }
                right_power = received_string.toInt();                 
                set_motor_powers(left_power, right_power);
                Serial.setTimeout(DEFAULT_TIMEOUT);
                break;*/
            }
			case HEARTBEAT: {
				last_heartbeat = millis();				
				digitalWrite(LED_BUILTIN, off ? HIGH : LOW);
				off=!off;
				//Serial.println("Heartbeat received <3");
				break;
			}
            default: {
				emergency_stop();
				Serial.println("COMMAND UNKNOWN"+received_string);
                //Serial.println("COMMAND UNKNOWN");
                //device_ready = false;
                break;
            }
        }
    }

}
