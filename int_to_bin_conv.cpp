#include <iostream>
#include <bitset>
#include <fstream>
#include <string>

//#define EMB_DECIMAL_FILE_NAME "emb_wav_file_decimal.txt"
//#define EMB_BINARY_FILE_NAME  "emb_wav_file_binary.txt"

using namespace std;

int main(int argc, char* argv[])
{
    // Read from file

    ifstream emb_wav_file_decimal;
    ofstream emb_wav_file_binary;
    string EMB_DECIMAL_FILE_NAME = argv[1];
    cout << EMB_DECIMAL_FILE_NAME << endl;
    string EMB_BINARY_FILE_NAME = argv[2];

    string number;
    int conv_int;
    string binary;

//    string file = EMB_DECIMAL_FILE_NAME;
    emb_wav_file_decimal.open(EMB_DECIMAL_FILE_NAME);
    if (emb_wav_file_decimal.fail())
    {
        cerr << " Error opening file....." << EMB_DECIMAL_FILE_NAME << " exiting !!" << endl;
        return(-1);
    }
    emb_wav_file_binary.open(EMB_BINARY_FILE_NAME );
    if (emb_wav_file_binary.fail())
    {
        cerr << " Error opening file " << EMB_BINARY_FILE_NAME  << "..... exiting !!" << endl;
        return(-1);
    }

    cout << "Int to bin: Converting " << argv[0] << " to " << argv[1] << endl;
    do
    {
        getline(emb_wav_file_decimal, number);

//        cout << number << endl;

        conv_int = stoi(number);
        binary = bitset<16>(conv_int).to_string(); //to binary
        emb_wav_file_binary << binary << endl;

    } while(!emb_wav_file_decimal.eof());
    emb_wav_file_decimal.close();
    emb_wav_file_binary.close();

//    string mybit = "11111111111111111111111111111110";
//    bitset<32> number(mybit);
//    cout << int(number.to_ulong()) << endl;
    return 0;

}