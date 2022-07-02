//
// Created by patrickpragman on 6/25/22.
//
#include <algorithm>
#include <iostream>
#include <string.h>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <set>
#include <iterator>
using namespace std;

set<string> SAVED_CHARS = {"^", "*", "/", "+", "-", "(", ")"};
set<string> WHITE_SPACE = {" ", "", "\t", "\n"};
string OPEN_PERENS = "(";
string CLOSE_PERENS = ")";
set<string> ORDER_OF_OPERATORS = {"^", "*", "/", "+", "-"};

string parse_operators(string left, string right, string op){

    float fleft = stof(left);
    float fright = stof(right);

    if (op == "^"){
        return to_string(pow(fleft, fright));
    } else if (op == "*") {
        return to_string(fleft * fright);
    } else if (op == "/") {
        return to_string(fleft / fright);
    } else if (op == "+") {
        return to_string(fleft + fright);
    } else if (op == "-") {
        return to_string(fleft - fright);
    } else {
        return "NONE!";
    }
}


void printv(vector<string> v){
    vector<string>::iterator it = v.begin();

    if (v.size() == 0){
        cout << "< >" << endl; 
    } else {

        cout << "<";
        while (it != v.end() - 1){
            cout << *it << ", ";
            it++;
        }
        cout << *it;
        cout << ">" << endl;
    }
}




vector<string> s_to_v(string s){
    vector<string> out;
    // first make an array of characters out of the string...

    string::iterator si = s.begin();
    string word;
    while (si != s.end()){
        string c(1, *si);
        if (WHITE_SPACE.find(c) != WHITE_SPACE.end()){
            if (!word.empty()){
                out.push_back(word);
            }            
            word.erase();
        } else if (SAVED_CHARS.find(c) != SAVED_CHARS.end()){
            if (!word.empty()){
                out.push_back(word);
            }
            out.push_back(c);
            word.erase();
        } else {
            word = word + c;
        }
        si++;

    }

    if (!word.empty()){
        out.push_back(word);
    }

    return out;
}

int get_steps_to_close_perens(vector<string> v){
    int index = 0;

    vector<string>::iterator it = v.begin();
    while (it != v.end()){
        if (*it == CLOSE_PERENS){
            return index;
        }

        index++;
        it++;
    }

    index++;
    if (index > v.size()){
        throw invalid_argument("No closing perens!");
    }
    return index;
}

string reduce(vector<string> &v){

    vector<string>::iterator vi = v.begin();

    string target_operator(1, '+');

    while (v.size() >= 1){
        if (*vi == OPEN_PERENS){
            v.erase(vi);
            vector<string> subvector;
            while (*vi != CLOSE_PERENS){
                subvector.push_back(*vi);
                v.erase(vi);
            }
            // now recursively reduce the sub problems
            *vi = reduce(subvector); // this is the index with the close perens, so it's find to switch it out
        }

        string left = *vi; vi++;
        string op = *vi; vi++;

        if (*vi == OPEN_PERENS){
            v.erase(vi);
            vector<string> subvector;
            while (*vi != CLOSE_PERENS){
                subvector.push_back(*vi);
                v.erase(vi);
            }
            // now recursively reduce the sub problems
            *vi = reduce(subvector); // this is the index with the close perens, so it's find to switch it out
        }

        string right = *vi;

        if (op == target_operator){

        }

        vi++; // to actually make the loop move forward along the vector

    }

    return v.at(0);
}


int main(){

    string s = "(5 + 10)^10.4";
    vector<string> v = s_to_v(s);
    printv(v);
    cout << get_steps_to_close_perens(v) << endl;
    printv(v);
    return 0;
}