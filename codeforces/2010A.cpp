#include <bits/stdc++.h>

using namespace std;

int main(){
	int a;
	cin >> a;
	for(int j=0; j<a; j++){
		int n;
		cin >> n;
		int result = 0;
		for(int i=0; i<n; i++){
			int w = 0;
			cin >> w;
			if(i%2==0){
				result = result + w;
			}
			if(i%2!=0){
				result = result - w;
			}
		}
		cout << result << endl;	
	}
	return 0;
}
