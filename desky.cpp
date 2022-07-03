/*
Ok.  I've been working on this since the 25th of June, and so far this is the best I can do.
It can't do arbitarily deep nested perens.  That's a frustration I could not figure out.
But I need to move on...

This was a really good learning project.  I learned a lot from this.


it handles order of operations and one level of perens... but that's it
in python it was much easier to set this up - I was able to make it go arbitrarily deep
easily
*/
#include <algorithm>
#include <iostream>
#include <string.h>
#include <cstdlib>
#include <cmath> // not emplimented beyond POW... in the future other functions
#include <vector>
#include <set>
#include <iterator>
using namespace std;

set<string> SAVED_CHARS = {"^", "*", "/", "+", "-", "(", ")"};
set<string> WHITE_SPACE = {" ", "", "\t", "\n"};
string OPEN_PERENS = "(";
string CLOSE_PERENS = ")";
vector<string> ORDER_OF_OPERATORS = {"^", "*", "/", "+", "-"};




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

void execute_op(vector<string> &v, string op) {
    vector<string>::iterator vi = v.begin();
    int index = 0;
    while (index < v.size()){

        if (*vi == op){
            vi--; // go left one slot
            string left = *vi; vi++; // put that value in a varable then move to the right side of the equation
            v.erase(vi);
            string right = *vi;
            v.erase(vi);
            string parsed = parse_operators(left, right, op);
            // cout << left << op << right << "=" << parsed << endl; // debug
            vi--; // go back two steps we want to change the current left value
            *vi = parsed;
            index = 0;
            vi = v.begin(); // go back to the very beginning
            // printv(v);
        } else {
        vi++; 
        index++;}
    }
}

void reduce(vector<string> &v){
    vector<string>::iterator vi = v.begin();
    int index = 0;

    // first break down the perens into individual problems and solve each one of those
    while (index < v.size()){
        if (*vi == OPEN_PERENS){
            /*
            if you encounter an open perens we need to:

                find the closure of that perens
                perform the action inside the perens

            */

            vector<string> subvector;
            v.erase(vi); // just cut it out
            while (*vi != CLOSE_PERENS) {
                subvector.push_back(*vi);
                v.erase(vi);
            }
            v.erase(vi);
            // now recursively reduce the sub problems
            reduce(subvector);
            // now we need to insert the subvector back into the position it was at in the vector but reduced
            v.insert(vi, begin(subvector), end(subvector));
            //printv(v);
            //*vi = subvector.at(0); // this is the index with the close perens, so it's find to switch it out
            vi = v.begin();
            index = 0;            
        } else {
        index++;
        vi++;}
    }
    // printv(v); // debug
    // now we should have all of our problems as the values of perens - now do PEMDAS and continue to reduce
    execute_op(v, "^");
    execute_op(v, "*");
    execute_op(v, "/");
    execute_op(v, "+");
    execute_op(v, "-");
}


int main(){
    string s;
    cout << "enter a math problem: "; getline(cin, s);
    vector<string> v = s_to_v(s);
    reduce(v);
    cout << s << " = " << v.at(0) << endl; 
    return 0;
}