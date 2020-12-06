# quick and dirty script to get food data from the shoddy openfoodfacts api

import requests
import json
import sys
import os
import argparse
import time

USER_AGENT = 'curl/7.54.0' # why not lmfao
BASE_URL = "https://us.openfoodfacts.org/code/"
headers = {'user-agent': USER_AGENT}

NUM_DIGITS = 0
LIMIT = 5000

def sanitize(food):
	return food.replace(",", " ").replace("  ", " ")

def isHealthy(kcals):
	healthy_cal_limit = 300
	weight = 0.80
	if kcals < healthy_cal_limit:
		return random() < weight
	else:
		return random() < (1 - weight)

def healthScore(kcals):
	kcals = float(kcals)
	bins = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
	for i in range(len(bins)):
		if kcals < bins[i]:
			return len(bins) - i
	return 0

num_items = 0
page_num = 0

while num_items < LIMIT:
	sys.stderr.write("Page: " + str(page_num) + ("x" * NUM_DIGITS) + " Items: " + str(num_items) + "\n")
	url = BASE_URL + str(page_num) + ("x" * (NUM_DIGITS - len(str(page_num)))) + ".json"
	page_num += 1
	if page_num == 9:
		page_num = 0
		NUM_DIGITS += 1

	response = requests.get(url, headers=headers)
	products = response.json()['products']

	for item in products:
		if "product_name" in item.keys():
			food = item['product_name']
			if len(food) == 0:
				continue
			kcals = -1
			if "energy-kcal_value" in item['nutriments'].keys():
				kcals = item['nutriments']['energy-kcal_value']
			elif "energy-kcal" in item['nutriments'].keys():
				kcals = item['nutriments']['energy-kcal']
			elif "energy-kcal_serving" in item['nutriments'].keys():
				kcals = item['nutriments']['energy-kcal_serving']
			else:
				continue

			print(str(num_items) + "," + sanitize(food) +  "," + str(kcals) + "," + str(healthScore(kcals)) )
			num_items += 1
