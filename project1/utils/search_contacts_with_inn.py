""" 
	универсальная утилита обработки данных из excell
	обрабатывает все файлы из папки "компас"

	берет только столбцы: "ИНН", "Номер телефона","Электронная почта"
	возвращает dict() пример {"Номер телефона":None, "Электронная почта": None}
"""
from project1.logger.logger_config import setup_logger
import pandas as pd
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
logger = setup_logger("search_contacts_with_inn.py")

directory = "project1/компас"
files = os.listdir(directory)
logger.info(f"start search files in {directory} ")

file = list()
for i in files:
	file.append(pd.read_excel(f"{directory}/{i}", usecols=["ИНН", "Номер телефона","Электронная почта"]))
logger.info(f"finding {len(file)} files")


def get_contact(inn):

	default = {"Номер телефона":None, "Электронная почта": None}
	try:
		inn = int(inn)
	except:
		logger.warning(f"incorrect inn _{inn}_")
		return default

	for f in file:
		con = f[f["ИНН"] == inn].replace({np.nan: None}).to_dict(orient="records")

		if len(con ) >0:
			return con[0]

	return default