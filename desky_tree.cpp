//
// Created by patrickpragman on 6/30/22.
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


set<string> WHITESPACE = {" ", "\n"};
set<string> DELIMETERS = {"(", ")"};
set<string> FUNCTIONS = {"sin", "cos"}; // tbc
set<string> OPERATORS = {"^", "*", "/", "+", "-"};
set<string> all = {" ", "\n", "(", ")", "sin", "cos", "^", "*", "/", "+", "-"};

bool in_set(string val, set<string> tgt){

    set<string>::iterator it = tgt.begin();
    while (it != tgt.end()){
        if (val == *it){
            return true;
        }
        it++;
    }
    return false;

}


class Token {
    public:
        string symbols;
        string type_of = NULL;
        bool is_computable = false;
        int precedence = 9;
    
    void show(){
        cout << this->symbols << ":" << endl;
        cout << "\t type: "<< this->type_of << endl;
        cout << "\t computable: "<< this->is_computable << endl;
        cout << "\t precedence: "<< this->precedence << endl;
    }
};

Token make_token_from_string(string word) {
    Token tok = Token();
    tok.symbols = word;
    
    if (in_set(word, all)){
        tok.is_computable = false;
    } else {
        tok.is_computable = true;
    }

    if (in_set(word, OPERATORS)){
        tok.type_of = "operator";
    } else if (in_set(word, FUNCTIONS)) {
        tok.type_of = "function";
    } else if (in_set(word, DELIMETERS)){
        tok.type_of = "delimiter";
    } else if (in_set(word, WHITESPACE)){
        // shouldn't ever happen
        tok.type_of = "whitespace";
    } else {
        tok.type_of = "value";
    }

    return tok;

}

vector<Token> tokenize(string tokens){

    vector<Token> output_token_vector;

    string::iterator it = tokens.begin();
    string word = "";
    while (it != tokens.end()){

        cout << *it << endl;
        
        if (in_set(*it, all)){
            // we found a character that tells us something structurally!  cool!
            output_token_vector.push_back(make_token_from_string(word));
            word = "";
            
        } else {
            word = word + *it;
        }

        it++;
    }


    return output_token_vector;
}


int main () {

    string tester = "(6/5) 4";
    vector<Token> toks = tokenize(tester);

    for (vector<Token>::iterator it = toks.begin(); it != toks.end(); it++){
        ignore *it->show();
    }

    return 0;
}