#include <bits/stdc++.h>

using namespace std;

int main(){
	int n;
	cin >> n;
	int result[n] = {0};
	for(int i=0; i<n; i++){
		int a;
		cin >> a;
		for(int x=0; x<3; x++){
			int b;
			cin >> b;
			if(b > a){
				result[i]++;
			}
		}
	}
	for(int i=0; i<n; i++){
		cout << result[i] << endl;
	}
}
