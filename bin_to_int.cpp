//
// Created by naufal on 5/12/17.
//

#include <iostream>
#include <bitset>
#include <fstream>
#include <string>
#include <cstdint>
//#define RECOVERED_DECIMAL_FILE_NAME "recovered_wav_file_decimal.txt"
//#define RECOVERED_BINARY_FILE_NAME "recovered_wav_file_binary.txt"


using namespace std;

int main(int argc, char* argv[])
{
    // Read from file
    ofstream recovered_wav_file_decimal;
    ifstream recovered_wav_file_binary;

    string RECOVERED_DECIMAL_FILE_NAME  = argv[2];
    string RECOVERED_BINARY_FILE_NAME  = argv[1];

    string number;
    int decimal;
    string binary;

//    string file = RECOVERED_DECIMAL_FILE_NAME;
    recovered_wav_file_decimal.open(RECOVERED_DECIMAL_FILE_NAME);
    if (recovered_wav_file_decimal.fail())
    {
        cerr << "BTI 1 Error opening file....." << RECOVERED_DECIMAL_FILE_NAME << " exiting !!\n" << endl;
        return(-1);
    }
    recovered_wav_file_binary.open(RECOVERED_BINARY_FILE_NAME);
    if (recovered_wav_file_binary.fail())
    {
        cerr << "BTI 2 Error opening file " << RECOVERED_BINARY_FILE_NAME << "..... exiting !!\n" << endl;
        return(-1);
    }

    cout << "Bin to int: Converting " << argv[2] << " to " << argv[1] << endl;

    getline(recovered_wav_file_binary, binary);
//    cout << binary << endl;
    do
    {
        //cout << " here \n" << endl;
        //cout << binary << endl;
        bitset<16> number(binary);
//        cout << number.to_string() << endl;
        decimal = int16_t(int(number.to_ulong()));
//        cout << decimal << endl;
        recovered_wav_file_decimal << decimal << endl;
        getline(recovered_wav_file_binary, binary);

    } while(!recovered_wav_file_binary.eof());
    recovered_wav_file_decimal.close();
    recovered_wav_file_binary.close();

    return 0;

}