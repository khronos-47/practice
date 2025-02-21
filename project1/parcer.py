from project1.logger.logger_config import setup_logger
import requests
from bs4 import BeautifulSoup
import os
import json
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()
logger = setup_logger("parcer")
api_key = os.getenv("dadata_api_key")
domain = os.getenv("domain")
session = requests.Session()
main_url = os.getenv("parcer_url")


total = 0
wrong_url = 0

def parser(Url ,code = '0' )-> tuple[dict,int]:
	global total 
	global wrong_url
	total_subjects = 0
	if Url == None : 
		return None,None
	response = session.get(Url)
	if response.status_code == 200:
		logger.info(f"get request {Url}") 
	else:
		wrong_url = wrong_url +1
		logger.error(f"connect error: {response.status_code}  url: {Url}")
		return None,None
		

	data = list()
	itog = 0
	soup = BeautifulSoup(response.text, 'html.parser')
	table = soup.find_all("table")
	trs = table[1].find_all("tr")


	headers = trs[0].find_all("td")

	for i in range(len(headers)):
		headers[i] = headers[i].text.replace("\r"," ").replace("\n", " ")


	for i in range (1,len(trs) - 1):
		tds = trs[i].find_all("td")
		obj = dict()
		if len(tds)<3 :
			continue

		obj[headers[0] ] = tds[0].text.replace("\r"," ").replace("\n", " ")
		obj[headers[1] ] = tds[1].text.replace("\r"," ").replace("\n", " ")
		obj[headers[2] ] = tds[2].text.replace("\r"," ").replace("\n", " ")
		if tds[1].text == 'ИТОГО' :
			itog = int(tds[2].text)
			continue
		try :
			k = tds[0].find_all("a")[0].get("href").split("/")
		except:
			k = None
		url =   main_url
		if not k  is None :
			if len(k) > 1 :
				url = url + tds[0].find_all("a")[0].get("href").replace("./","")
				code = tds[0].text
			else:
				url = url +  code + "/" +  k[0]
		else:
			url = None
		obj["url"] = url

		nested_data, tot = parser(url, code)
		if tot == None:
			tot = 0
		obj["nested data"] = nested_data

		data.append(obj)
		total_subjects = total_subjects + 1 + tot
		total = total + 1
		print(f"\033[F\033[KWrong URL:   {wrong_url}")
		print(f"\033[Kобработано:  {total} {Url} " , end = "")

	datas  = { "Subject" : data}
	
	datas["Итог"] = total_subjects 
	
	return datas, total_subjects

	





def main():

	print("\n")
	datas,k = parser(main_url, 0)

	json_data = json.dumps(datas, ensure_ascii=False, indent=4)

	# Сохраняем в файл
	with open("products.json", "w", encoding="utf-8") as f:
	    f.write(json_data)



	#parser(response)

	#find_address_with_INN(5421110537,542100994)
	#print(get_contact(540230327779))
