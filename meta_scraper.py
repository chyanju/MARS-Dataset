import requests
import time
import calendar
import pickle

from bs4 import BeautifulSoup

def print_item(p_key, p_pgno, p_item):
	print("-----------------------------------------")
	print("# In {}, Page {}".format(p_key, p_pgno))
	for d_key in p_item.keys():
		print("{}: {}".format(d_key, p_item[d_key]))
	print("-----------------------------------------")


mURL = {
	"DPLYR": (238, "https://stackoverflow.com/questions/tagged/dplyr?sort=votes&page={}&pagesize=50"),
	"TIDYR": (30, "https://stackoverflow.com/questions/tagged/tidyr?sort=votes&page={}&pagesize=50"),
}

meta_dataset = {
	"DPLYR":[],
	"TIDYR":[],
}

for d_key in meta_dataset.keys():
	for d_pgno in range(1, mURL[d_key][0]):
		d_URL = mURL[d_key][1].format(d_pgno)
		try:
			d_page = requests.get(d_URL)
			if not str(d_page.status_code)[0] == '2':
				raise Exception
			d_soup = BeautifulSoup(d_page.content, 'html.parser')
			d_containers = d_soup.find_all(class_="question-summary")
			for d_div in d_containers:
				dd_vote = int(d_div.find_all(class_="vote-count-post")[0].get_text())
				dd_ansr = int(list(d_div.find_all(class_="status")[0].children)[1].get_text()) # number of answers
				dd_acpt = True if len(d_div.find_all(class_="answered-accepted"))>0 else False
				dd_view = int(d_div.find_all(class_="views")[0]['title'].replace("views","").replace("view","").replace(",",""))
				dd_title= list(d_div.find_all(class_="summary")[0].children)[1].get_text()
				dd_url  = list(list(d_div.find_all(class_="summary")[0].children)[1].children)[0]["href"]
				dd_tags = d_div.find_all(class_="tags")[0].get_text().strip().split()
				dd_tmp1 = list(d_div.find_all(class_="user-action-time")[0].children)[1]['title']
				dd_time = calendar.timegm(time.strptime(dd_tmp1,"%Y-%m-%d %H:%M:%SZ"))
				# time in float: seconds since the epoch

				dd_item = {
					"url" : dd_url,
					"vote": dd_vote,
					"ansr": dd_ansr,
					"acpt": dd_acpt,
					"view": dd_view,
					"title":dd_title,
					"tags": dd_tags,
					"time": dd_time,
				}

				meta_dataset[d_key].append(dd_item)

				print_item(d_key, d_pgno, dd_item)
		except Exception as e:
			print("ERROR, SKIP.")

with open("./meta_dataset.pkl","wb") as f:
	pickle.dump(meta_dataset,f)