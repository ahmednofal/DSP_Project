#include <iostream>
#include <bitset>
#include <fstream>
#include <string>

#define DECIMAL_FILE_NAME "wav_file_decimal.txt"
#define BINARY_FILE_NAME "wav_file_binary.txt"

using namespace std;

int main()
{
    // Read from file
    ifstream wav_file_decimal;
    ofstream wav_file_binary;

    string number;
    int conv_int;
    string binary;

//    string file = DECIMAL_FILE_NAME;
    wav_file_decimal.open(DECIMAL_FILE_NAME);
    if (wav_file_decimal.fail())
    {
        cerr << " Error opening file....." << DECIMAL_FILE_NAME << " exiting !!" << endl;
        return(-1);
    }
    wav_file_binary.open(BINARY_FILE_NAME);
    if (wav_file_binary.fail())
    {
        cerr << " Error opening file " << BINARY_FILE_NAME << "..... exiting !!" << endl;
        return(-1);
    }

    do
    {
        getline(wav_file_decimal, number);

        conv_int = stoi(number);
        binary = bitset<32>(conv_int).to_string(); //to binary
        wav_file_binary << binary << endl;

    } while(!wav_file_decimal.eof());
    wav_file_decimal.close();
    wav_file_binary.close();

    return 0;

}