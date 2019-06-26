import os
import re
import time
import pandas as pd
import numpy as np

filename = "october_2018.csv"

value = lambda x: x.strip("[]").replace("'", "").split(", ")
converters={"actiontaken": value,
			"devicetype": value,
			"deviceos": value,
			"osversion": value,
			"ipaddress": value,
			"browsertype": value,
			"connectivitytype": value,
			"screensize": value,
			"videoquality": value,
			"sitedomain": value,
			"devicename": value,
			"browserversion": value}

cols = ["gigyaid", "devicetype", "deviceos", "browsertype", "connectivitytype", "screensize"]
device_cols = ["devicetype", "deviceos", "browsertype", "connectivitytype", "screensize"]
df = pd.read_csv(filename, low_memory = False, usecols = cols, converters = converters)

for col in device_cols:
	df[col] = df[col].apply(lambda x: [i.upper() for i in x])
	if col == "devicetype":
		df[col] = df[col].apply(lambda x: list(set(['MOBILE' if re.search(r'IPHONE', i) else i for i in x])))
		df[col] = df[col].apply(lambda x: list(set(['TABLET' if re.search(r'IPAD', i) else i for i in x])))
		df[col] = df[col].apply(lambda x: list(set(['MOBILE' if re.search(r'IPOD', i) else i for i in x])))
	if col == "deviceos":
		df[col] = df[col].apply(lambda x: list(set(['ANDROID' if re.search(r'ANDROID', i) else i for i in x])))
		df[col] = df[col].apply(lambda x: list(set(['IOS' if re.search(r'IOS', i) else i for i in x])))
	if col == "browsertype":
		df[col] = df[col].apply(lambda x: list(set(['CLOUDFONE' if re.search(r'CLOUDFONE', i) else i for i in x])))

def getUnique(df, col):
	df = df[col].apply(tuple)
	unique = df.unique()
	unique = list(set([a for t in unique for a in t]))
	unique = [word.replace('NAN', 'NAN_'+col) for word in unique]
	return unique

def prepareDataDevice(df):
	s = time.time()
	feature_cols = []
	for col in device_cols:
		x = getUnique(df, col)
		feature_cols.extend(x)
	print(df.columns)
	new_df = pd.DataFrame(index = df.gigyaid, columns = feature_cols)
	df = df.set_index("gigyaid")
	for user_id in df.index.unique():
		user = df.loc[user_id]
		for col in device_cols:
			a = user[col]
			a = [word.upper() for word in a]
			a = [word.replace('NAN', 'NAN_'+col) for word in a]
			if col == "deviceos":
				a = ['ANDROID' if re.search(r'ANDROID', word) else word for word in a]
				a = ['IOS' if re.search(r'IOS', word) else word for word in a]
			if col == "devicetype":
				a = ['MOBILE' if re.search(r'IPHONE', word) else word for word in a]

			for b in a:
				new_df.loc[user_id][b] = 1

	new_df.fillna(0, inplace=True)
	for col in feature_cols:
		print(col)
		new_df[col] = new_df[col].apply(lambda x: col+'_y' if x == 1 else col+'_n')
	e = time.time()
	total_time = time.strftime("%H:%M:%S", time.gmtime(e-s))
	print("Process time: ", total_time)
	print(new_df.memory_usage().sum())
	new_df.to_csv("data.csv")

prepareDataDevice(df)

# print(getUnique(df, "devicetype"))
# print(getUnique(df, "deviceos"))
# print(getUnique(df, "browsertype"))
# print(getUnique(df, "connectivitytype"))
#
# df.to_csv("data.csv", index = False)

# print(df["devicetype"].astype(str).unique())
# print(df["deviceos"].astype(str).unique())
# print(df["browsertype"].astype(str).unique())
# print(df["connectivitytype"].astype(str).unique())