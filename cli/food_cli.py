#============================================================================#
# Title        : Food Management System CLI                                  #
# Author       : Josh Natis                                                  #
# Description  : An ncurses-based command-line user interface to the         #
#                Food Management System database.                            #
# Repository   : https://github.com/joshnatis/FMS                            #
# License      : MIT                                                         #
# Usage        : python3 food_cli.py                                         #
#============================================================================#

import curses
import curses_scrollable
import food_db

def init_curses():
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)

def getmaxdim():
	rows, cols = curses.LINES, curses.COLS
	return min(rows, 30), min(cols, 120)

def max_strlen(str_list):
	return len(max(str_list, key=len))

def display_title_screen(screen, figlet_title, ascii_title, msg):
	screen.clear()
	screen.bkgd('/', curses.color_pair(1))
	screen.refresh()

	rows, cols = getmaxdim()

	# an attempt at centering the window
	win = curses.newwin(rows - 2, cols - 4,  rows // 20, cols // 40)

	try: # big screen
		win.addstr(figlet_title, curses.color_pair(3) | curses.A_BOLD)
	except curses.error: # lil screen
		win.clear()
		win.addstr(1, 2, ascii_title, curses.color_pair(3) | curses.A_BOLD)
	except:
		exit()

	win.addstr(rows - 4, cols - 6 - len(msg), msg)

	curses.curs_set(0)
	win.bkgd(' ', curses.color_pair(2))
	win.box()
	c = win.getch()
	win.clear()
	curses.curs_set(1)
	return c

#page 1
def display_welcome(screen):
	figlet_title = """
	___               _
       / __\__   ___   __| |
      / _\/ _ \ / _ \ / _` |
     / / | (_) | (_) | (_| |
     \/   \___/ \___/ \__,_|

							       _
       /\/\   __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_
      /    \ / _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
     / /\/\ \ (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_
     \/    \/\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
			  |___/
      __           _
     / _\_   _ ___| |_ ___ _ __ ___
     \ \| | | / __| __/ _ \ '_ ` _ \\
     _\ \ |_| \__ \ ||  __/ | | | | |
     \__/\__, |___/\__\___|_| |_| |_|
	 |___/
	"""
	ascii_title = "FOOD MANAGEMENT SYSTEM"
	msg = "[PRESS ANY KEY TO CONTINUE]"
	display_title_screen(screen, figlet_title, ascii_title, msg)

#page 4
def display_farewell(screen):
	figlet_title = """"
        ___                _ _
       / _ \___   ___   __| | |__  _   _  ___
      / /_\/ _ \ / _ \ / _` | '_ \| | | |/ _ \\
     / /_\\\\ (_) | (_) | (_| | |_) | |_| |  __/
     \____/\___/ \___/ \__,_|_.__/ \__, |\___|
                                   |___/
                         /
       /\\  ___  /\\      /
      // \\/   \\/ \\\\
     ((    O O    ))
      \\  /     \\ //
       \\/  | |  \\/
        |  | |  |
        |  | |  |
        |   o   |
        | |   | |
        |m|   |m|
     """
	ascii_title = "GOODBYE"
	msg = "[OR NOT... PRESS R TO RESTART]"
	c = display_title_screen(screen, figlet_title, ascii_title, msg)

	return chr(c).lower() == "r"

#page 2
def display_login(screen):
	rows, cols = getmaxdim()
	begin_y = rows // 20
	begin_x = cols // 40
	win = curses.newwin(rows - 2, cols - 4, begin_y, begin_x)
	win.box()
	win.addstr(begin_y, begin_x, "LOGIN", curses.A_BOLD | curses.A_UNDERLINE)

	msg1 = "USERNAME:"
	msg2 = "PASSWORD:"
	win.addstr(begin_y + 2, begin_x, msg1)
	win.addstr(begin_y + 4, begin_x, msg2)
	win.refresh()

	win_user = curses.newwin(1, 20, begin_y + 3, begin_x + len(msg1) + 4)
	win_user.bkgd(' ', curses.color_pair(3) | curses.A_REVERSE)

	textbox_user = curses.textpad.Textbox(win_user)
	textbox_user.edit()
	username = textbox_user.gather()[:-1]

	win_passwd = curses.newwin(1, 20, begin_y + 5, begin_x + len(msg2) + 4)
	win_passwd.bkgd(' ', curses.color_pair(4))

	curses.noecho()
	textbox_passwd = curses.textpad.Textbox(win_passwd)
	textbox_passwd.edit()
	password = textbox_passwd.gather()[:-1]

	win.clear()
	win.refresh()

	return (username, password)

#a general re-usable menu component
def display_menu(choices, begin_y, begin_x, nlines=None, ncols=None, title=None):
	if not nlines: nlines=len(choices) + 2
	if not ncols: ncols=max_strlen(choices) + 4
	if title:
		nlines += 1
		ncols = max(ncols, len(title) + 2)

	win_menu = curses.newwin(nlines, ncols, begin_y, begin_x)

	win_menu.bkgd(' ', curses.color_pair(3))
	win_menu.box()
	win_menu.keypad(True) # enable arrow keys
	curses.curs_set(0)

	if title: win_menu.addstr(begin_y, begin_x - 1, title, curses.A_BOLD |
	                                                       curses.A_UNDERLINE |
	                                                       curses.A_ITALIC)
	choice = -1
	highlight = 0

	y_offset = 2 if title else 1
	while True:
		for i in range(len(choices)):
			if i == highlight:
				win_menu.attron(curses.A_REVERSE)
			win_menu.addstr(i + y_offset, 1, choices[i])
			win_menu.attroff(curses.A_REVERSE)

		choice = win_menu.getch()

		if choice == curses.KEY_UP:
			highlight = (highlight - 1) % len(choices)
		elif choice == curses.KEY_DOWN:
			highlight = (highlight + 1) % len(choices)
		elif choice == 10: #enter
			break

	return choices[highlight]

#page 3 sub-windows
def display_categories_and_clients(win, query_params, coords):
	begin_y, begin_x = coords

	categories = ["Currently Available Items", "History of Purchases"]
	category = display_menu(categories, begin_y, begin_x, title="Category")
	query_params["category"] = category

	clients = ["Household", "User"]
	begin_y, begin_x = begin_y + len(categories), begin_x + max_strlen(categories) + 1
	client = display_menu(clients, begin_y, begin_x)
	query_params["client"] = client

	if client != "Household":
		users = food_db.getusers()

		begin_y, begin_x = begin_y + len(clients), begin_x + max_strlen(clients) + 1
		nlines, ncols = len(users) - 8, max_strlen(users) + 4
		dims = (nlines, ncols, begin_y, begin_x)
		win_menu = curses.newwin(*dims)
		win_menu.bkgd(' ', curses.color_pair(3))

		menu_screen = curses_scrollable.Screen(users, win_menu, dims, selectable=True)
		client = menu_screen.run()
		query_params["client"] = client

	win.clear()
	win.refresh()

#page 3 sub-windows
def display_subjects_and_orders(win, query_params, coords):
	begin_y, begin_x = coords

	subjects = ["View items", "View quantities of items", "View money spent", "View %healthy"]
	title = query_params["client"] + "'s " + query_params["category"]
	subject = display_menu(subjects, begin_y, begin_x, title=title)
	query_params["subject"] = subject.split()[1].lower()

	win.clear()
	win.refresh()

	if query_params["subject"] == "items":
		title = "Order " + query_params["client"] + "'s " + query_params["category"] + " By:"
		orderings = ["quantity", "total_price", "purchase_date",
			     "expiration_date", "food_id", "store_id"]
		order = display_menu(orderings, begin_y, begin_x, title=title)
		query_params["order"] = order

		polarities = ["Ascending", "Descending"]
		begin_y, begin_x = begin_y + len(orderings), begin_x + max_strlen(orderings) + 1
		polarity = display_menu(polarities, begin_y, begin_x)
		query_params["order"] = order + (" DESC" if polarity == "Descending" else " ASC")

	elif query_params["subject"] == "quantities" or query_params["subject"] == "money":
		title = "Purchased:" if query_params["subject"] == "quantities" else "Spent:"
		time_periods = ["This Week", "This Month", "This Year", "All Time"]
		time_period = display_menu(time_periods, begin_y, begin_x, title=title)
		query_params["time_period"] = time_period.split()[1]

		if query_params["subject"] == "quantities":
			polarities = ["Ascending", "Descending"]
			begin_y += len(time_periods)
			begin_x += max_strlen(time_periods) + 1
			polarity = display_menu(polarities, begin_y, begin_x)
			query_params["order"] = "DESC" if polarity == "Descending" else "ASC"

	query_params["category"] = query_params["category"].split()[0]

#page 3 sub-window
def display_data(win, query_params, coords):
	rows, cols = getmaxdim()
	begin_y, begin_x = coords

	data = food_db.getdata(query_params)
	if not data:
		raise KeyboardInterrupt

	dims = (rows - 2, cols - 4, begin_y, begin_x + 1)
	data_screen = curses_scrollable.Screen(data, win, dims)
	try: data_screen.run()
	except curses.error:
		max_width = cols - begin_x - 4
		data = [row[:max_width] for row in data]
		data_screen = curses_scrollable.Screen(data, win, dims)
		data_screen.run()

#page 3
def display_main():
	rows, cols = getmaxdim()
	begin_y = rows // 20
	begin_x = cols // 40

	win = curses.newwin(rows - 2, cols - 4,  begin_y, begin_x)
	win.bkgd('.', curses.color_pair(2))
	win.refresh()

	query_params = {}

	coords = (begin_y, begin_x)
	display_categories_and_clients(win, query_params, coords)
	display_subjects_and_orders(win, query_params, coords)

	win.clear()
	win.bkgd(' ', curses.color_pair(3))
	win.refresh()
	display_data(win, query_params, coords)

def main(screen):
	init_curses()
	display_welcome(screen)

	username, password = display_login(screen)
	food_db.login(username, password)

	cont = True
	while cont:
		display_main()
		cont = display_farewell(screen)

try:
	curses.wrapper(main)
except food_db.mysql.connector.Error as err:
	print(err)
except KeyboardInterrupt:
	print("Bye")

