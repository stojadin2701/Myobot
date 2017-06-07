#include "NewPing.h"

//Pins for enabling motor control
const unsigned char ENABLE_PINS[] = {7, 8};

const unsigned char ENABLE_PINS_NUM = sizeof(ENABLE_PINS)/sizeof(unsigned char);

const unsigned char MOTOR_PINS[] = {5, 6, 9, 10};

const unsigned char MOTOR_PINS_NUM = sizeof(MOTOR_PINS)/sizeof(unsigned char);

const unsigned char DISTANCE_TRIG_PIN = 2;

const unsigned char DISTANCE_ECHO_PIN = 4;

const unsigned char MAX_DISTANCE = 40;

const unsigned long DEFAULT_TIMEOUT = 300000;
const unsigned long MOTOR_POWERS_TIMEOUT = 2000;

enum Command { START = 1, SET_MOTORS };

unsigned char received_command = 0;

String received_string;

NewPing sonar(DISTANCE_TRIG_PIN, DISTANCE_ECHO_PIN, MAX_DISTANCE);

unsigned int ping_speed = 50;
unsigned long ping_timer;

boolean device_ready = false;

boolean going_forward = false;

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
    if(powers[0] != 0 && powers[2] != 0 && powers[1] == 0 && powers[3] == 0) going_forward = true;
    else going_forward = false;

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

    Serial.begin(115200); // set the baud rate
    ping_timer = millis();
    Serial.setTimeout(DEFAULT_TIMEOUT);
}

void echo_check(){
    //mozda i ovde going_forward &&
    if(sonar.check_timer()){
        if(sonar.ping_result/US_ROUNDTRIP_CM < 20) {
            int zero_arr[] = {0, 0, 0, 0};
            write_motor_powers(zero_arr, MOTOR_PINS_NUM);
            Serial.println("Stopping motors!");
        }
        send_distance_info(String(sonar.ping_result/US_ROUNDTRIP_CM));
    }
}

void send_distance_info(String info){
    if(device_ready){
        Serial.println(info);
    }
}

void loop() {
    if(device_ready && going_forward && millis() >= ping_timer){
        ping_timer += ping_speed;
        sonar.ping_timer(echo_check);
    }

    if(Serial.available()) {
        received_string = Serial.readStringUntil('\n'); // read the incoming data
        Serial.print("Received: ");
        Serial.println(received_string);
        switch(received_string.toInt()){
            case START: {
                Serial.println("Ready");
                device_ready = true;
                break;
            }
            case SET_MOTORS: {
                Serial.setTimeout(MOTOR_POWERS_TIMEOUT);
                signed char left_power, right_power;
                received_string = Serial.readStringUntil('\n'); // read the incoming data
                if (received_string.length()==0) {
                    Serial.println("Setting motor powers timed out...");
                    Serial.setTimeout(DEFAULT_TIMEOUT);
                    break;
                }
                left_power = received_string.toInt();
                received_string = Serial.readStringUntil('\n'); // read the incoming data
                if (received_string.length()==0) {
                    Serial.println("Setting motor powers timed out...");
                    Serial.setTimeout(DEFAULT_TIMEOUT);
                    break;
                }
                right_power = received_string.toInt();                 
                set_motor_powers(left_power, right_power);
                Serial.setTimeout(DEFAULT_TIMEOUT);
                break;
            }
            default: {
                Serial.println("COMMAND UNKNOWN");
                device_ready = false;
                break;
            }
        }
    }

}
