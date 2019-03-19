#ifndef UUID_OTP
#define UUID_OTP

#include <iostream>
#include <string>

class uuid_otp {
	private:
		int key_val;
		int time;
		string uuid;
	public:
		int trans_time_func(int);
		string trans_key_func(int);
		int trance_uuid_func(string);
}

#endif
