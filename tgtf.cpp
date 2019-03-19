#include <iostream>
#include <string>

using namespace std;

int main(void){
	string key;
	int time;
	int tmp_time;
	string uuid="00000000000000000000000000000000";
	stirng bus_uuid;
	int cnt = 0;
	int circle = 0;

	cout<<"key 입력: ";
	cin>>key;
	cout<<"시간 입력: ";
	cin>>time;
	tmp_time = time*10;
	//cout<<"UUID 입력(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 8-4-4-4-12): " <<endl;
	//cin>>bus_uuid;

	circle = uuid.length()/key.length();

	while(circle>0){
		if(cnt<uuid.length()){
			uuid.replace(cnt,key.length(),key);
			circle--;
		}
		else{
			
		cnt += key;
	}
