import requests
from datetime import datetime
import os
import pandas as pd
from io import StringIO

print(pd.__version__)

# 設定
API_URL = r'https://data.ntpc.gov.tw/api/datasets/8308ab58-62d1-424e-8314-24b65b7ab492/xml?page=0&size=5000'
OUTPUT_FOLDER = r'C:\Users\Samantha Chao\Software Development Projects\Taipei-City-Dashboard\data-processing'
OUTPUT_FILE = 'aging_new_tp.csv'
## create directory if it does not exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# receive request
response = requests.get(API_URL)
response.raise_for_status()					## Check if it's a bad request.

raw_data = response.text
# print(raw_data)
# df = pd.read_xml(raw_data)				# a depreciated approach in the future
df = pd.read_xml(StringIO(raw_data))
df_copy = df.copy()
# print(df.head(6))
# print(df["field1"])							# get column named "field1"
# print(df[df['field1'] == '新北市- 計'])		 # get row where field1 is "新北市- 計"
df_filtered = df[df_copy['field1'].str.contains('新北市- 計', na=False)].copy()		# safer to add .copy() when slicing a subset
# print(df_filtered)

# change field1 column names
# df_filtered = df_filtered['field1'].str.extract(r'(\d+)', expand=False).astype(int)
# print(df_filtered)

df_filtered["end_of_year"] = df_filtered['field1'].str.extract(r'(\d+)', expand=False).astype(int)
# print(df_filtered)

# change all other column names
df_filtered = df_filtered.rename(columns={
	"percent24": "young_age_population",
	"percent25": "young_age_percentage",
	"percent26": "working_age_population",
	"percent27": "working_age_percentage",
	"percent28": "elderly_age_population",
	"percent29": "elderly_age_percentage",
	"percent30": "elderly_dependency_ratio",
	"percent31": "youth_dependency_ratio",
	"percent32": "total_dependency_ratio",
	"percent33": "aging_index"
})

print(df_filtered)

# add timestamp column
df_filtered['date_time'] = datetime.now().isoformat()
print(df_filtered)

# keep columns in order
df_filtered = df_filtered[[
	"end_of_year",
	"young_age_population",
	"young_age_percentage",
	"working_age_population",
	"working_age_percentage",
	"elderly_age_population",
	"elderly_age_percentage",
	"elderly_dependency_ratio",
	"youth_dependency_ratio",
	"total_dependency_ratio",
	"aging_index",
	"date_time"
]
]

print(df_filtered)


out_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
df_filtered.to_csv(out_path, index=False, encoding="utf-8-sig")
print(f"Saved to {out_path}")




## handle headers
# print(response.headers)

# content_type = response.headers.get('content-type')
# print(content_type)

## json is not available
# raw_data = response.json()
# print(raw_data)


# response.raise_for_status()
# if response.status_code == 200:
# 	print('success')
# print(response)