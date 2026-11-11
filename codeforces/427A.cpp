#include <bits/stdc++.h>

using namespace std;

int main(){
	int n;
	cin >> n;
	int arr[n];
	for(int i=0; i<n; i++){
		cin >> arr[i];
	}
	int check = 0;
	int result = 0;
	for(int i=0; i<n; i++){
		if(arr[i]==-1){
			check--;
			if(check < 0){ 
				result ++;
				check = 0;
			}
		}
		else if(arr[i]!=-1){
			check += arr[i];
		}
	}
	cout << result << endl;
}
