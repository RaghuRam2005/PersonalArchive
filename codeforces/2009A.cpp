#include <bits/stdc++.h>

using namespace std;

int main(){
    int n;
    cin >> n;
    vector<int> result;
    for(int i=0; i<n; i++){
        int a;
        int b;
        cin >> a >> b;
        int c = a;
        int min_val = 1000000000;
        while(a<=c && c<=b){
            if((c-a)+(b-c)>0){
                min_val = min(min_val, (c-a)+(b-c));
            }
            c++;
        }
        if (min_val == 1000000000){
            result.insert(result.begin()+i, 0);
        }
        else{
            result.insert(result.begin()+i, min_val);
        }
    }
    for(int i=0; i<n; i++){
        cout << result[i] << endl;
    }
}