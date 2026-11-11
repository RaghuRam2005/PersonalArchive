#include <bits/stdc++.h>

using namespace std;

int main(){
	int n;
	cin >> n;
	int result[n] = {0};
	for(int i=0; i<n; i++){
		int a;
		int b;
		int c=a;
		cin >> a;
		cin >> b;
		if(a==b){
			result[n]=0;
		}
		for(int j=a; j<b; j++){
			int val=(c-a)+(b-c);
			int check_val=(j-a)+(b-j);
			if(check_val<=val){
				c = j;
			}
		}
		cout << c << endl;
		result[n] = c;
		cout << result[n] << endl;
	}
	return 0;
}
