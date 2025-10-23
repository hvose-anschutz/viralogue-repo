#include <iostream>
#include <vector>
#include <string>

using namespace std;

// to compile in command terminal: g++ <program.cpp> -o <output>
// then to run: ./output

int main() {
    vector<string> msg {"Hello", "C++", "World", "from", "VS Code", "and the C++ extension!"};

    for (const string& word : msg) {
        cout << word << " ";
    }
    cout << endl;
    return 0;
}
