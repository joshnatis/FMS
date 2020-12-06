/* parse foods csv from https://raw.githubusercontent.com/yufree/expodb/master/foodb/foods.csv into preferred format for our food_registry table 
 
note: since the dataset doesnt have any caloric info, just food names, the calories are randomly generated values
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <ctime>

using namespace std;

#define ID_COL 1
#define NAME_COL 1

int health_score(double cals)
{
	const int bins[] = {50, 100, 150, 200, 250, 300, 350, 400, 450, 500};
	for(int i = 0; i < 10; ++i)
		if(cals < bins[i])
			return 10 - i;
	return 0;
}

int main()
{
	srand (time(NULL));

	ifstream fin("foods_github.csv");
	ofstream fout("github_output.csv");

	vector<string> output = {};

	string line;
	string token;
	string build = "";
	int col = 0;
	int count = 1689;

	getline(fin, line); /* ignore first line */

	while(getline(fin, line))
	{
		std::istringstream iss(line);
		while(getline(iss, token, ','))
		{
			if(col == NAME_COL)
			{
				build += to_string(count) + "," + token + ",";
				int cals = 100 + (rand() % 700);
				build += to_string(cals) + "," + to_string(health_score(cals));
				fout << build << endl;
				count++;
				col = 0;
				build = "";
				break;
			}
			col++;
		}
		col = 0;
	}
}
