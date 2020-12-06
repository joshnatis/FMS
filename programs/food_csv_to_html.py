fin="food_type3.csv"

with open(fin, "r") as f:
	strip=f.readline()
	print('<!DOCTYPE html>\n<html lang="en">\n<head>\n\n<title>FoodDB</title>\n<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1"/>\n<link rel="stylesheet" href="styles.css"></head>\n<body>')
	for line in f:
		fields=line.split(",")
#		food_id, food_name, calories, health_scale, image
		print("<div class=\"food\">")
		print("\t<div class=\"left\">")
		print("\t\t<h1 class=\"food_name\">", fields[1], "</h1>")
		print("\t\t<img alt=\"\" src=\"" + fields[4][:-1], "\" class=\"food_img\">")
		print("\t</div>")
		print("\t<div class=\"right\">")
		print("\t\t<p class=\"calories\">", fields[2], "</p>")
		print("\t\t<p class=\"health_scale\">", fields[3], "</p>")
		print("\t</div>")
		print("</div>")
	print("</body></html>")
