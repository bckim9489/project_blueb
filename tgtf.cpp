#include <iostream>
#include <string>

using namespace std;

int main(void){
	string code_array = "bafced0357192468";
	
	string key;
	int time;
	int g_tmp_time;
	string uuid;
	string bus_uuid;
	bool flag = true;
	string tmp_uuid = "0";
	int tmp_key;

	cout<<"key 입력: ";
	cin>>key;
	cout<<"시간 입력: ";
	cin>>time;
	//cout<<"UUID 입력(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 8-4-4-4-12): " <<endl;
	//cin>>bus_uuid;
/*
	circle = uuid.length()/key.length();

	while(circle>0){
		if(cnt<uuid.length()){
			uuid.replace(cnt,key.length(),key);
			circle--;
			cnt += key.length();
		}
	}
	cnt = cnt - uuid
	return 0;
}
*/
	
	while(flag){
		int tmp_time = g_tmp_time;
		if(uuid.empty()||uuid.length()<33){
			for(int i=0; i<key.length(); i++){
				tmp_key = key[i];
				tmp_key -= tmp_time;
				tmp_time--;
				if(tmp_key<0){
					tmp_key += tmp_time%3;
					if(tmp_key>code_array.length()-1){
						tmp_key -= (code_array.length()-1);
					}
				}
				else{
					uuid.append(1, code_array[tmp_key]);
				}
			}
		}
		
		if(uuid.length()==32){
			//uuid.erase(32, (uuid.length()-32));
			flag = false;
		}
	}

	cout<<"UUID: "<<uuid<<endl;
	return 0;
}
