/* find and remove duplicates from a csv file (as determined by food name being identical */

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

using namespace std;

#define NAME_COL 1

int main()
{
	ifstream fin("foods_final.csv");
	ofstream fout("nodups_food.csv");
	ofstream dups_fout("dups.txt");

	vector<string> output = {};
	vector<string> names = {};

	int count = 0;
	int dup_count = 0;

	string line;
	string token;
	int col = 0;

	getline(fin, line); /* ignore first line */

	while(getline(fin, line))
	{
		count++;
		std::istringstream iss(line);
		while(getline(iss, token, ','))
		{
			if(col == NAME_COL)
			{
				if(std::find(names.begin(), names.end(), token) == names.end()) /* not found */
				{
					names.push_back(token);
					output.push_back(line);
				}
				else
				{
					dups_fout << token << endl;
					dup_count++;
				}
			}
			col++;
		}
		col = 0;
	}

	for(int i = 0; i < output.size(); ++i)
		fout << output[i] << endl;

	cout << "COUNT: " << count << "\nDUPS: " << dup_count << endl;
}
