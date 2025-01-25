import requests
from bs4 import BeautifulSoup
import os
import json
from project1.database.models import parser_storage
from project1.database.database import get_db
from sqlalchemy.orm import Session
from project1.utils.search_contacts_with_inn import get_contact

url = "https://prognoz.vcot.info"
session = requests.Session()


def get_request():
	"""
		функция для подклчение на сайт 
	"""
	url = "https://prognoz.vcot.info/default/default/confirm/?e=mva@nso.ru&h=99dfd32317a0ed864f98872d2d8d4f26&se=prognoz@vniitruda.ru"
	response = session.get(url)
	if response.status_code == 200:
		print("Успешное подключение!")
	else:
		print(f"connect error: {response.status_code}")
		exit()
	
	return response 

def find_address_with_INN(INN, KPP=0):
	"""
		берет ИНН и КПП ((опционально , нужно что бы найти конкретный филиал ))
		возвращает кортеж с данными 
		возвращает False при ошибке запроса
	"""
	url = "http://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"

	api_key = "93d565449b876ddb521af38876915cc2889b9740"


	headers = { 
	"Content-Type": "application/json",
	"Accept": "application/json",
	"Authorization": "Token 93d565449b876ddb521af38876915cc2889b9740" }
	kpp = str(KPP)
	data = {"query": str(INN) }

	response = requests.post(url,json= data, headers=headers)

	if response.status_code != 200:
		print(f"Ошибка запроса {response.status_code}")
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


def parser2(response):
	""" 
		фунция парсит сайт 
		берет response (ответ на запрос к сайту)

		парсит его получает данные из 
		find_address_with_INN(INN, KPP=0) и если он не дал 
		контактов получает их из get_contact(INN)

		при полном парсинге сохраняет все в базу данных 

	"""


	soup = BeautifulSoup(response.text, 'html.parser')
	db = next(get_db())
	try:
		path = "step2"
		os.mkdir(path)
		
	except:
		pass

	file = open(f"{path}/table.txt","w")
	def table_parser(table):
		"""
			вспомогательная функция парсит таблички по ссылке
			подстройена под радительскую функцию и поэтому вложена в ней
		"""
		th = table.find_all("th")
		lines = table.find_all('tr')
		


		for i in range(2,len(lines)):
			a = lines[i].find_all("td")
			name = a[0].text

			for j in range (1,6):

				try:
					k = a[j].find_all("a")[0]
				except:
					continue

				href = k.get("href").replace("®ion","&region")
				#print(href)


				table_res = session.get(url + href)

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

					#print("Phone:", phone,"  ",email," ",employee_count)


					

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



	panel2 = soup.find(id='panel_2',recursive=True)
	sub1_panel2 = panel2.find( id='panel_ed059bddbb59879821d31d8ea84dc724_1',recursive=True)
	table_parser(sub1_panel2)

	sub1_panel2 = panel2.find( id='panel_ed059bddbb59879821d31d8ea84dc724_2',recursive=True)
	table_parser(sub1_panel2)

	sub1_panel2 = panel2.find( id='panel_ed059bddbb59879821d31d8ea84dc724_3',recursive=True)
	table_parser(sub1_panel2)
	db.commit()

def main():
	response = get_request()
	parser2(response)
	#parser(response)

	#find_address_with_INN(5421110537,542100994)
	#print(get_contact(540230327779))
