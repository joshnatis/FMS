#============================================================================#
# Title        : tabulator                                                   #
# Author       : Josh Natis                                                  #
# Description  : Process delimeter-separated text (like CSV or TSV)          #
#                into a MySQL-style ASCII table diagram                      #
# Repository   : https://github.com/joshnatis/tabulate                       #
#                Note that this instance of the tabulator is a modified      #
#                version of the source -- rather than printing the table     #
#                to standard out, the table is returned as a string.         #
# License      : MIT                                                         #
# Usage        :                                                             #
#    As a standlone program:                                                 #
#       python3 tabulator.py <file> [optional delimiter]                     #
#                                                                            #
#    As an imported module:                                                  #
#       (1) Load your data into a matrix (a list of lists), where each inner #
#           list contains a row of data (each element of said list being one #
#           value from your file). i.e. type(matrix) = list(list(str)).      #
#           Optionally, pad your values with an extra space on either side.  #
#           Take a look at the main() function for an example of this.       #
#                                                                            #
#       (2) Pass your data to pad_missing_columns().                         #
#           This is optional, but it assures that each of your rows has the  #
#           same amount of elements in it (yielding a table that's not       #
#           jagged)                                                          #
#                                                                            #
#       (3) Pass your data to print_table, which will return the resulting   #
#           table as a string.                                               #
#============================================================================#

import sys

def get_max_col_lengths(df):
	lengths = []
	num_cols = len(df[0])
	for i in range(num_cols):
		lengths.append(max([len(row[i]) for row in df]))
	return lengths

def print_table(df):
	num_cols = len(df[0])
	col_widths = get_max_col_lengths(df)
	df_width = sum(col_widths) + 1 + num_cols

	header = True

	table = ""

	table += print_border(df_width, col_widths) + "\n"
	for row in df:
		table += "|"
		for i in range(len(row)):
			table += row[i].ljust(col_widths[i]) + "|"
		table += "\n"

		if header:
			table += print_border(df_width, col_widths) + "\n"
			header = False
	table += print_border(df_width, col_widths)
	return table

def print_border(df_width, col_widths):
	border = "-" * (df_width - 1)
	elapsed = 0
	for length in col_widths:
		elapsed += length
		border = border[:elapsed] + "+" + border[elapsed + 1:]
		elapsed += 1
	return "+" + border

def pad_missing_columns(df):
	max_cols = len(df[0])
	for i in range(len(df)):
		if len(df[i]) < max_cols:
			df[i] += [''] * (max_cols - len(df[i]))
		elif len(df[i]) > max_cols:
			df[i] = df[i][:max_cols]

def main():
	delim = ","
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<file> [optional delimiter]")
		exit(1)
	elif len(sys.argv) == 3:
		delim = sys.argv[2]

	df = []
	try:
		with open(sys.argv[1],'r') as f:
			for row in f:
				columns = [(" " + col.strip() + " ") for col in row.split(delim)]
				df.append(columns)

			pad_missing_columns(df)
			print(print_table(df))

	except IndexError:
		print("IndexError: make sure your fields don't have a '" + delim + "' within them.")
	except OSError:
		print("Unable to open the file", sys.argv[1])

if __name__ == "__main__":
	main()

