#include <bits/stdc++.h>

using namespace std;

int main(){
	int comp;
	comp = 1 + 2 + 3;
	int a;
	for(int i=0;i<2;i++){
		cin >> a;
		comp = comp - a;
	}
	cout << comp << endl;
	return 0;
}
