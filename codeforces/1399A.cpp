#include <bits/stdc++.h>

using namespace std;

int main(){
	int n;
	cin >> n;
	vector<string> res;
	for(int i=0; i<n; i++){
		int m;
		cin >> m;
		int arr[m];
		for(int j=0; j<m; j++){
			cin >> arr[j];
		}
		for(int a=0; a<m/2; i++){
			for(int b=a+1; b<m; b++){
				if(arr[a] < arr[b]){
					arr[a] = 0;
				}
			}
		}
		int result = 0;
		for(int a=0; a<m; a++){
			if(arr[a]!=0){
				result ++;
			}
		}
		if(result==1){
			res.insert(res.begin()+i, "YES");
		}
		else{
			res.insert(res.begin()+i, "NO");
		}
	}
	for(int i=0; i<n; i++){
		cout << res[i] << endl;
	}
	return 0;
}
