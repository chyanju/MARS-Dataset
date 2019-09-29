import requests
import pickle
import time

from bs4 import BeautifulSoup

def print_item(p_key, p_item, p_skp, p_dn, p_ttl):
	print("-----------------------------------------")
	print("# In {}, Skipped: {}, Proccessed: {}/{}".format(p_key, p_skp, p_dn, p_ttl))
	print("== Question ==")
	print(",".join([str(p[0]) for p in p_item[1]]))
	print("== Answers:{} ==".format(len(p_item[2])))
	for d_ansr in p_item[2]:
		print("acpt:{}/vote:{}/ansr:{}".format(
			d_ansr["acpt"],
			d_ansr["vote"],
			",".join([str(p[0]) for p in d_ansr["ansr"]]),
		))
	print("-----------------------------------------")

COMMON_URL_PREFIX = "https://stackoverflow.com/{}"
with open("./meta_dataset.pkl","rb") as f:
	meta_dataset = pickle.load(f)

# (0:p, txt), (1:code, txt)
# (d_item, d_question, d_answers)
dataset = {
	"DPLYR":[],
	"TIDYR":[],
}

skipped_urls = []

n_skipped = 0
n_done = 0
n_total = 0
# get n_total
for d_key in meta_dataset.keys():
	n_total += len(meta_dataset[d_key])

# start scraping
for d_key in dataset.keys():
	for d_item in meta_dataset[d_key]:
		try:
			d_url = COMMON_URL_PREFIX.format(d_item["url"])
			d_page = requests.get(d_url)
			if not str(d_page.status_code)[0] == '2':
				raise Exception
			d_soup = BeautifulSoup(d_page.content, 'html.parser')
			# remove all script tags first
			for d_script in d_soup(["script","style"]):
				d_script.decompose()

			d_ques_cntnr = d_soup.find_all(class_="question")[0].find_all(class_="post-text")[0]
			d_question = []
			for dd_tag in d_ques_cntnr(["p","code"]):
				if dd_tag.name == "p":
					d_question.append((0, dd_tag.get_text()))
				elif dd_tag.name =="code":
					d_question.append((1, dd_tag.get_text()))
				else:
					raise Exception

			d_ansr_cntnr = d_soup.find_all(class_="answer")
			d_answers = []
			for dd_ansr in d_ansr_cntnr:
				dd_acpt = True if "accepted-answer" in dd_ansr["class"] else False
				dd_vote = int(dd_ansr.find_all(class_="js-vote-count")[0].get_text())
				dd_cntnr = dd_ansr.find_all(class_="post-text")[0]
				dd_ansr = []
				for dd_tag in dd_cntnr(["p","code"]):
					if dd_tag.name == "p":
						dd_ansr.append((0, dd_tag.get_text()))
					elif dd_tag.name == "code":
						dd_ansr.append((1, dd_tag.get_text()))
				dd_item = {
					"acpt": dd_acpt,
					"vote": dd_vote,
					"ansr": dd_ansr,
				}
				d_answers.append(dd_item)

			dataset[d_key].append((d_item, d_question, d_answers))
			print_item(d_key, (d_item, d_question, d_answers), n_skipped, n_done, n_total)
			n_done += 1

			# take a break
			if n_done%200 == 0:
				print("# TAKING A 3-MINUTE BREAK...")
				with open("./dataset.pkl","wb") as f:
					pickle.dump(dataset, f)
				time.sleep(180)


		except Exception as e:
			# raise
			n_skipped += 1
			skipped_urls.append(d_url)
			with open("./skipped_urls.txt","w") as f:
				f.write("\n".join(skipped_urls))
			print("ERROR, SKIP.")

with open("./dataset.pkl","wb") as f:
	pickle.dump(dataset, f)
		

