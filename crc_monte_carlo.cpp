
#include <iostream>
using namespace std;
int main()
{
	srand(time(0));
	int finally[4] = { 0,0,0,0 };     // these will be the four calls GG GB BB BG (good called bad and ect)
	bool call;			// this is to test its decision of a bad call or nt to if its actually a good call
	int binary[11];		// teh array carrying the bianary string
	int modcheck[3];
	double noise = .05;	// the noisey channel percentage
	int base = 0;
	int base2 = 0;// the base for creating the modulo
	int modulo = 0;		// the modulo created from the base
	double noisechck = 0;		// to see iff the noise it chosen or not
	//create cycle redundancy/ modulo
	for (int k = 0; k < 100; k++)
	{
		for (int h = 0; h < 10; h++)
		{
			for (int j = 0; j < 10; j++)
			{
				base = 0;
				base2 = 0;
				for (int i = 0; i < 8; i++)
				{
					binary[i] = rand() % (1 - 0 + 1);
					base += (binary[i] * (pow(2, (8 - i - 1))));
				}
				modulo = base % 7;
				switch (modulo) {
				case 0:
					binary[8] = 0;
					binary[9] = 0;
					binary[10] = 0;
					break;
				case 1:
					binary[8] = 0;
					binary[9] = 0;
					binary[10] = 1;
					break;
				case 2:
					binary[8] = 0;
					binary[9] = 1;
					binary[10] = 0;
					break;
				case 3:
					binary[8] = 0;
					binary[9] = 1;
					binary[10] = 1;
					break;
				case 4:
					binary[8] = 1;
					binary[9] = 0;
					binary[10] = 0;
					break;
				case 5:
					binary[8] = 1;
					binary[9] = 0;
					binary[10] = 1;
					break;
				case 6:
					binary[8] = 1;
					binary[9] = 1;
					binary[10] = 0;
					break;
				case 7:
					binary[8] = 1;
					binary[9] = 1;
					binary[10] = 1;
					break;
				default:
					cout << "		error ";
					return(0);
				}

				// create code for noisey channel
				for (int i = 0; i < 11; i++)
				{
					if ((rand() % 101) / 100.0 <= noise) // Fix integer division issue
					{
						binary[i] = (binary[i] == 0) ? 1 : 0; // Simplified bit flipping
					}
				}

				// create check for cycle redundancy
				for (int i = 0; i < 8; i++)
				{
					base2 += (binary[i] * (pow(2, (8 - i - 1))));
				}
				modulo = base2 % 7;
				switch (modulo) {
				case 0:
					modcheck[0] = 0;
					modcheck[1] = 0;
					modcheck[2] = 0;
					break;
				case 1:
					modcheck[0] = 0;
					modcheck[1] = 0;
					modcheck[2] = 1;
					break;
				case 2:
					modcheck[0] = 0;
					modcheck[1] = 1;
					modcheck[2] = 0;
					break;
				case 3:
					modcheck[0] = 0;
					modcheck[1] = 1;
					modcheck[2] = 1;
					break;
				case 4:
					modcheck[0] = 1;
					modcheck[1] = 0;
					modcheck[2] = 0;
					break;
				case 5:
					modcheck[0] = 1;
					modcheck[1] = 0;
					modcheck[2] = 1;
					break;
				case 6:
					modcheck[0] = 1;
					modcheck[1] = 1;
					modcheck[2] = 0;
					break;
				case 7:
					modcheck[0] = 1;
					modcheck[1] = 1;
					modcheck[2] = 1;
					break;
				default:
					cout << "		error ";
					return(0);
				}
				//                      this is a check to asertain which call it will put out
				call = true;
				for (int i = 0; i < 3; i++)
				{
					if (modcheck[i] != binary[i + 8])
					{
						call = false;
						break;
					}
				}
				if ((call == true) && (base == base2))//		GG
				{
					finally[0]++;
				}
				else if ((call == false) && (base == base2))//	GB
				{
					finally[1]++;
				}

				else if ((call == false) && (base != base2))//	BB
				{
					finally[2]++;
				}

				else if ((call == true) && (base != base2))//	BG
				{
					finally[3]++;
				}

			}
		}
	}
		for (int i = 0; i < 4; i++)
		{
			cout << finally[i] << endl;
		}
}


// add blue add green and blue/green devide it by 100to get a prrcent improvement