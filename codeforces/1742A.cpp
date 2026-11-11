#include <bits/stdc++.h>

using namespace std;

int main(){
	int n;
	cin >> n;
	string result[n];
	for(int i=0; i<n; i++){
		int a, b, c;
		cin >> a >> b >> c;
		if(a+b == c || a+c == b || b+c==a){
			result[i] = "YES";
		}
		else{
			result[i] = "NO";
		}
	}
	for(int i=0; i<n; i++){
		cout << result[i] << endl;
	}
	return 0;
}
