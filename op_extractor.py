# ordered pair extractor
import pickle


def subset_filter(p_ops):
	func_subset = ["spread","gather","separate","unite","select","filter","summarise","group_by","mutate","join"]
	d_ops = []
	for d_pair in p_ops:
		if d_pair[0] in func_subset and d_pair[1] in func_subset:
			d_ops.append(d_pair)
	return d_ops

def op_extractor(p_dep):
	# extract the ordered pair from the parsed dependency structure
	all_ops = []
	if type(p_dep)==list:
		token_list = []
		for d_token in p_dep:
			if type(d_token)==str or d_token is None:
				token_list.append(d_token)
			elif type(d_token)==dict:
				token_list.append(list(d_token.keys())[0])
				all_ops += op_extractor(d_token) # recursive add
			elif type(d_token)==list:
				token_list.append(None)
				all_ops += op_extractor(d_token) # recursive add
			else:
				# currently does not deal with list type, or other types, just ignore
				token_list.append(None)
		if len(token_list)>1:
			for i in range(1, len(token_list)):
				all_ops.append( (token_list[i-1],token_list[i]) )
		return all_ops
	elif type(p_dep)==dict:
		# assume only one key at this layer
		if len(list(p_dep.keys()))>0:
			return op_dfs(p_dep[list(p_dep.keys())[0]], list(p_dep.keys())[0])
		else:
			return []
	else:
		return []

def op_dfs(p_dep, p_ckey):
	all_ops = []
	if type(p_dep)==dict:
		for d_key in p_dep.keys():
			all_ops.append( (d_key,p_ckey) )
			all_ops += op_dfs(p_dep[d_key], d_key)
	#else: nothing can be done, just return []
	return all_ops

with open("./parsed_dataset.pkl","rb") as f:
	parsed_dataset = pickle.load(f)

op_dataset = parsed_dataset
n_total = 0
n_done = 0
for d_key in op_dataset.keys():
	n_total += len(op_dataset[d_key])
# add one more kv: "ansr_op" / ordered pair
for d_key in op_dataset.keys():
	for i in range(len(op_dataset[d_key])):
		n_done += 1
		print("\r# Processing {}/{}".format(n_done,n_total),end="")
		for j in range(len(op_dataset[d_key][i][2])):
			d_item = op_dataset[d_key][i][2][j]
			d_dep = d_item["ansr_parsed"]
			op_dataset[d_key][i][2][j]["ansr_op"] = subset_filter(op_extractor(d_dep))
print()

with open("./op_dataset.pkl","wb") as f:
	pickle.dump(op_dataset, f)




"""
op_dataset = {
	"DPLYR":[
		(
		/metadata/{
			"url":str, "vote":int, "ansr":int, "acpt":int, "view":int, "title":str, "tags":list of str, "time":float
		},
		/question/[
			(0,txt),(1,code),...
		],
		/answers/[
			{"acpt":bool, "vote":int, "ansr":[(0,str),(1,code),...], "ansr_parsed":[ [],[],... ], "ansr_op":[ (),(),... ]},
			{},{},
			...
		],
		),
		(),(),...
	],
	"TIDYR":...
}
"""