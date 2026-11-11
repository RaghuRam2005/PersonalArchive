#include <bits/stdc++.h>

using namespace std;

int main(){
    int n;
    cin >> n;
    for(int i=0; i<n; i++){
        int m;
        cin >> m;
        vector<int> balls;
        for(int j=0; i<m; j++){
            int k;
            cin >> k;
            balls.insert(balls.begin()+j, k);
        }
    }
}