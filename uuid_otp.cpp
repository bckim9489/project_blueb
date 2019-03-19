#include "uuid_otp.h"
#define ALGO 940809

int uuid_otp::trans_time_func(int _time){
	_time = _time + ALGO;
	this->time = _time;
	return time;
}

stirng uuid_otp::trans_key_func(int _key){
	int tmp = _key*time;
	
