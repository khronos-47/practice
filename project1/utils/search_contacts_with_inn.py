import pandas as pd
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


directory = "project1/компас"
files = os.listdir(directory)

file = list()
for i in files:
	file.append(pd.read_excel(f"{directory}/{i}", usecols=["ИНН", "Номер телефона","Электронная почта"]))

# file.append(pd.read_excel("41 2024-08-07 10-28.xlsx", usecols=["ИНН", "Номер телефона","Электронная почта"]))
# file.append(pd.read_excel("43 2024-08-07 10-27.xlsx", usecols=["ИНН", "Номер телефона","Электронная почта"]))
# file.append(pd.read_excel("49 2024-08-07 10-28.xlsx", usecols=["ИНН", "Номер телефона","Электронная почта"]))
# file.append(pd.read_excel("52 2024-08-07 10-28.xlsx", usecols=["ИНН", "Номер телефона","Электронная почта"]))
# file.append(pd.read_excel("69 2024-08-07 10-27.xlsx", usecols=["ИНН", "Номер телефона","Электронная почта"]))
# file.append(pd.read_excel("71 2024-08-07 10-24.xlsx", usecols=["ИНН", "Номер телефона","Электронная почта"]))



def get_contact(inn):

	default = {"Номер телефона":None, "Электронная почта": None}
	try:
		inn = int(inn)
	except:
		print(f"incorrect inn   _{inn}_")
		return default

	for f in file:
		con = f[f["ИНН"] == inn].replace({np.nan: None}).to_dict(orient="records")

		if len(con ) >0:
			print(con)
			return con[0]

	return default