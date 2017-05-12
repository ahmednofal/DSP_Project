//
// Created by naufal on 5/12/17.
//

#include <iostream>
#include <bitset>
#include <fstream>
#include <string>

//#define RECOVERED_DECIMAL_FILE_NAME "recovered_wav_file_decimal.txt"
//#define RECOVERED_BINARY_FILE_NAME "recovered_wav_file_binary.txt"

#define RECOVERED_DECIMAL_FILE_NAME "wav_file_decimal.txt"
#define RECOVERED_BINARY_FILE_NAME "wav_file_binary.txt"

using namespace std;

int main()
{
    // Read from file
    ofstream recovered_wav_file_decimal;
    ifstream recovered_wav_file_binary;

    string number;
    int decimal;
    string binary;

//    string file = RECOVERED_DECIMAL_FILE_NAME;
    recovered_wav_file_decimal.open(RECOVERED_DECIMAL_FILE_NAME);
    if (recovered_wav_file_decimal.fail())
    {
        cerr << " Error opening file....." << RECOVERED_DECIMAL_FILE_NAME << " exiting !!" << endl;
        return(-1);
    }
    recovered_wav_file_binary.open(RECOVERED_BINARY_FILE_NAME);
    if (recovered_wav_file_binary.fail())
    {
        cerr << " Error opening file " << RECOVERED_BINARY_FILE_NAME << "..... exiting !!" << endl;
        return(-1);
    }

    getline(recovered_wav_file_binary, binary);
    do
    {
        bitset<32> number(binary);
        decimal = int(number.to_ulong()); //to binary
        recovered_wav_file_decimal << decimal << endl;
        getline(recovered_wav_file_binary, binary);

    } while(!recovered_wav_file_binary.eof());

    recovered_wav_file_decimal.close();
    recovered_wav_file_binary.close();

    return 0;

}