from project1.logger.logger_config import setup_logger
import requests
from bs4 import BeautifulSoup
import os
import json
from project1.database.models import parser_storage
from project1.database.database import get_db
from sqlalchemy.orm import Session
from project1.utils.search_contacts_with_inn import get_contact
from dotenv import load_dotenv
import os

load_dotenv()
logger = setup_logger("parcer")
url = os.getenv("dadata_url") 
api_key = os.getenv("dadata_api_key")
domain = os.getenv("domain")
session = requests.Session()


def get_request():
	"""
		функция для подключение на сайт 
	"""
	url = os.getenv("parcer_url") 
	response = session.get(url)
	if response.status_code == 200:
		logger.info("Successful connection!")
	else:
		logger.error(f"connect error: {response.status_code}")
		exit()
	
	return response 

def find_address_with_INN(INN, KPP=0):
	"""
		берет ИНН и КПП ((опционально , нужно что бы найти конкретный филиал ))
		возвращает кортеж с данными 
		возвращает False при ошибке запроса
	"""
	logger.info(f"find_address {INN}, {KPP}" )

	url = os.getenv("dadata_url")
	api_key = os.getenv("dadata_api_key")

	headers = { 
		"Content-Type": "application/json",
		"Accept": "application/json",
		"Authorization": f"Token {api_key}" 
		}
	kpp = str(KPP)
	data = {"query": str(INN) }

	response = requests.post(url,json= data, headers=headers)

	if response.status_code != 200:
		logger.warning(f"Ошибка запроса {response.status_code} {response.json()}")
		return False
	#print(response.json())
	parsed_data = response.json()["suggestions"]
	for data in parsed_data:
		if "kpp" in data["data"] and data["data"]["kpp"] == kpp:
			return (
				data["data"]["address"]["data"]["source"],
				data["data"]["address"]["data"]["area_with_type"],
				data["data"]["emails"] or None,
				data["data"]["phones"] or None,
				data["data"]["employee_count"] or None
				)
	for data in parsed_data:
		if "branch_type" in data["data"] and data["data"]["branch_type"] == "MAIN":
			return (
				data["data"]["address"]["data"]["source"],
				data["data"]["address"]["data"]["area_with_type"],
				data["data"]["emails"] or None,
				data["data"]["phones"] or None,
				data["data"]["employee_count"] or None
				)
	if len(parsed_data) == 0:
		return (None, None,None,None,None)
	else:
		return (
			parsed_data[0]["data"]["address"]["data"]["source"],
			parsed_data[0]["data"]["address"]["data"]["area_with_type"],
			parsed_data[0]["data"]["emails"] or None ,
			parsed_data[0]["data"]["phones"] or None,
			parsed_data[0]["data"]["employee_count"] or None,
			)


def parser2(response, enterprise_type = "all"):
	""" 
		фунция парсит сайт 
		берет response (ответ на запрос к сайту)

		парсит его получает данные из 
		find_address_with_INN(INN, KPP=0) и если он не дал 
		контактов получает их из get_contact(INN)

		при полном парсинге сохраняет все в базу данных 

	"""

	total_items = 0
	soup = BeautifulSoup(response.text, 'html.parser')
	db = next(get_db())


	def table_parser(table):
		"""
			вспомогательная функция парсит таблички по ссылке
			подстройена под радительскую функцию и поэтому вложена в ней
		"""
		th = table.find_all("th")
		lines = table.find_all('tr')
		status = False


		for i in range(2,len(lines)):
			a = lines[i].find_all("td")
			name = a[0].text
			if enterprise_type.lower() in name.lower() and enterprise_type != "all":
				status =True
			else:
				continue
			for j in range (1,6):

				try:
					k = a[j].find_all("a")[0]
				except:
					continue

				href = k.get("href").replace("®ion","&region")
				#print(href)

				table_res = session.get(domain + href)

				table_in_href = BeautifulSoup(table_res.text, 'html.parser')
				heads = table_in_href.find_all("th")

				for line in table_in_href.find_all("tr"):
					ob = line.find_all("td")
					if ob == []:
						continue
					#print(ob)
					ownership_form = f"{th[1].text.replace('формы собственности', '')}" 
					economic_activity = f"{name}"
					number = f"{ th[1+j].text }"
					organization =  ob[1].text
					inn = ob[2].text
					kpp = ob[3].text

					datas = find_address_with_INN(ob[2].text, ob[3].text)
					if datas == False:
						db.commit()
						exit()

					address,region,email,phone,employee_count = datas

					contacts = get_contact(ob[2].text)

					if phone is None:
						phone = contacts["Номер телефона"]

					if email is None:
						email = contacts["Электронная почта"]

					new_data = parser_storage(
						ownership_form = ownership_form,
						economic_activity = economic_activity,
						number = number,
						organization = organization,
						inn = inn,
						kpp =kpp,
						address =address,
						region = region,
						phone = phone,
						email = email,
						employee_count = employee_count 
						)

					db.add(new_data)
					nonlocal  total_items
					total_items = total_items + 1
					print(f"\rОбработано: {total_items}   | {ownership_form}| {economic_activity}| {number}| {organization}| {inn}", end='', flush=True)
			if status:
				db.commit()
				return



	panel2 = soup.find(id='panel_2',recursive=True)
	sub1_panel2 = panel2.find( id='panel_ed059bddbb59879821d31d8ea84dc724_1',recursive=True)
	table_parser(sub1_panel2)
	logger.debug("end parcing panel_ed059bddbb59879821d31d8ea84dc724_1")
	sub1_panel2 = panel2.find( id='panel_ed059bddbb59879821d31d8ea84dc724_2',recursive=True)
	table_parser(sub1_panel2)
	logger.debug("end parcing panel_ed059bddbb59879821d31d8ea84dc724_2")
	sub1_panel2 = panel2.find( id='panel_ed059bddbb59879821d31d8ea84dc724_3',recursive=True)
	table_parser(sub1_panel2)
	logger.debug("end parcing panel_ed059bddbb59879821d31d8ea84dc724_3")
	db.commit()
	logger.debug("db commit")

def main():

	response = get_request()
	
	parser2(response, "Рыболовство и рыбоводство")
	#parser(response)

	#find_address_with_INN(5421110537,542100994)
	#print(get_contact(540230327779))
