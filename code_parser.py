import pickle

func_keywords = {
	"BASE": ["Arithmetic","Foreign","LongVectors","Hyperbolic","MathFun","Sys.glob","Sys.info","InternalMethods","agrep","all","args","array","Constants","autoload","Control","backsolve","Deprecated","bindenv","Encoding","bitwise","browser","Startup","bquote","DateTimeClasses","log","Cstack_info","char.expand","browserText","Logic","character","NumericConstants","by","EnvVar","body","Ops.Date","Round","Dates","Special","Extract","La_version","Last.value","Defunct","Paren","cumsum","append","R.Version","Bessel",".Platform","Random.user","curlGetHeaders","Sys.getenv","La_library","Colon","Random","dontCheck","Sys.sleep","do.call","abbreviate","Primitive","Sys.time","Sys.getpid","any","as.environment","Quotes","CallExternal","Extract.data.frame","file.info","Extract.factor","aperm","file.path","gc.time","Comparison","NA","NULL","ISOdatetime","isSymmetric","Recall","Internal","deparse","gctorture","RdUtils","base-internal","Sys.setFileTime","builtins","jitter","Sys.setenv","Syntax","Sys.which","apply","as.data.frame","base-package","Trig","kronecker","locales","call","Memory","get","UseMethod","attr","Memory-limits","findInterval","charmatch","attributes","getCallingDLL","contributors","file.show","chartr","integer","Reserved","cat","logical","Vectorize","cbind","rownames","colnames","all.equal","matrix","date","class","chol2inv","Sys.localeconv","connections","Rhome","force","commandArgs",".Device","Sys.readlink","expand.grid","all.names","as.Date","assignOps","attach","diag","maxCol","base-defunct","comment","complex","encodeString","dots","double","dcf","environment","function","formatC","getNativeSymbolInfo","base-deprecated","names","nargs","deparseOpts","as.POSIX*","cut.POSIXt","drop","as.function","expression","dput","assign","ns-hooks","callCC","missing","cut","QR.Auxiliaries","basename","col",".bincode","qr","ns-internals","files","normalizePath","capabilities","debug","getwd","chkDots","gettext","list2env","colSums","conditions","conflicts","data.matrix","raw","dataframeHelpers","grepRaw","grep","ifelse","rawConnection","delayedAssign","is.function","chol","duplicated","readChar","match.arg","dyn.load","copyright","regex","regmatches","load","extSoftVersion","crossprod","diff","gl","factor","data.class","data.frame","is.language","det","lazyLoad","lapply","readline","svd","mapply","kappa","length","difftime","strtoi","detach","dim","forceAndCall","remove","round.POSIXt","nchar","margin.table","sets","showConnections","lengths","shQuote","nlevels","numeric_version","octmode","droplevels","formals","dump","eapply","dimnames","sign","eval","match.call","sprintf","path.expand","funprog","pcre_config","eigen","file.access","message","print.data.frame","strwrap","NotYet","exists","gc","srcfile","files2","subset","print.default","gzcon","file.choose","hexmode","tempfile","find.package","formatDL","format.pval","reg.finalizer","getDLLRegisteredRoutines","getLoadedDLLs","icuSetCollate","sys.source","iconv","prmatrix","invisible","is.finite","slotOp","is.R","format","paste","system","interaction","taskCallbackManager","taskCallbackNames","format.info","rowsum","groupGeneric","grouping","traceback","interactive","is.object","parse","tracemem","scale","sQuote","is.recursive","serialize","isS4","identical","levels","setTimeLimit","print","l10n_info","system2","warning","strptime","libPaths","lower.tri","labels","list","readLines","strrep","strsplit","identity","sum","list.files","is.single","warnings","tapply","sweep","taskCallback","summary",".Machine","match.fun","is.unsorted","libcurlVersion","library.dynam","library","unlist","license","matmult","unname","scan","ls","memory.profile","on.exit",".Script","make.names","make.unique","merge","mat.or.vec","match","try","name","nrow","mode","options","socketSelect","pmatch","textConnection","weekdays","which","utf8Conversion","withVisible","polyroot","ns-dblcolon","userhooks","ns-topenv","numeric","outer","order","mean","zapsmall","zpackages","typeof","memCompress","rawConversion","prop.table","write","rapply","rank","pushBack","readBin","rep","noquote","ns-load","readRDS","readRenviron","norm","ns-reflect.Rd","row","pos.to.env","seq.Date","replace","sample","row.names","seq.POSIXt","pretty","split","source","save","proc.time","prod","quit","seek","sink","range","search","slice.index","rle","rev","table","seq","tabulate","sequence","toString","stop","trace","solve","transform","stopifnot","startsWith","sort","standardGeneric","substr","substitute","trimws","validUTF8","system.file","system.time","writeLines","vector","which.min","strtrim","structure","xtfrm","switch","with","tilde","sys.parent","unlink","timezones","zutils","unique","AsIs","Foreign-internal","Extremes"],
	"DPLYR": ["all_vars","compute","distinct","as.tbl_cube","arrange","cumall","copy_to","auto_copy","filter","filter_all","do","group_by_all","check_dbplyr","coalesce","backend_dbplyr","explain","bind","all_equal","failwith","add_rownames","case_when","group_by_prepare","group_indices","join","ident","location","lead-lag","desc","n_distinct","dim_desc","id","join.tbl_df","order_by","na_if","band_members","funs","bench_compare","recode","reexports","group_size","progress_estimated","between","nasa","group_by","tally_","select_all","select","sample","near","if_else","nth","init_logging","src_dbi","rowwise","src_local","scoped","dplyr-package","summarise_all","summarise_each","same_src","dr_dplyr","top_n","tbl_vars","select_vars","grouped_df","storms","tidyeval","src_tbls","vars","starwars","summarise","with_order","tally","tbl","tbl_cube","tbl_df","groups","make_tbl","mutate","pull","ranking","setops","slice","sql","src","common_by","arrange_all","as.table.tbl_cube"],
	"TIDYR": ["nest","smiths","spread","replace_na","separate","unite","uncount","table1","separate_rows","unnest","tidyr-package","who","extract","extract_numeric","gather","complete","expand","drop_na","deprecated-se","fill","full_seq"],
	# "%>%" is TIDYR is removed
}

def func_detector_longest(p_code):
	# print("# in {}".format(p_code))
	# should be able to detect all of the appearings
	# !!! Notice: currently we assume that no function is substring of other functions
	# !!! AND: a function only appears once in a code snippet
	func_idx = []
	for d_key in func_keywords.keys():
		for d_func in func_keywords[d_key]:
			d_idx = p_code.find(d_func)
			if d_idx > -1:
				func_idx.append((d_idx, d_func))
	sorted_func_idx = sorted(func_idx, key=lambda p:len(p[1]), reverse=True)
	if len(sorted_func_idx)==0:
		return None
	else:
		return sorted_func_idx[0][1]


def func_scanner(p_code, is_outermost_layer=False):
	# !!! a function call must contain ()
	if "(" not in p_code or ")" not in p_code:
		# no function call according to the assumption
		return func_detector_longest(p_code)
	d_len = len(p_code)
	lr_pairs = []
	tmp_lb = []
	tmp_rb = []
	# detect bracket boundaries
	for i in range(d_len):
		if p_code[i] == "(":
			tmp_lb.append(i)
		if p_code[i] == ")":
			tmp_rb.append(i)
		if len(tmp_lb)>0 and len(tmp_lb)==len(tmp_rb):
			lr_pairs.append((tmp_lb[0],tmp_rb[-1]))
			tmp_lb = []
			tmp_rb = []
	# construct the current node
	if len(lr_pairs) == 1:
		r_dep_trees = {}
		d_func = func_detector_longest(p_code[0:lr_pairs[0][0]])
		r_dep_trees[d_func] = func_scanner( p_code[lr_pairs[0][0]+1:lr_pairs[0][1]] )
	elif len(lr_pairs) > 1:
		if is_outermost_layer:
			r_dep_trees = []
			for d_idx in range(len(lr_pairs)):
				d_pair = lr_pairs[d_idx]
				if d_idx == 0:
					d_func = func_detector_longest(p_code[0:d_pair[0]])
					r_dep_trees.append( {d_func:func_scanner( p_code[d_pair[0]+1:d_pair[1]] )} )
				else:
					p_pair = lr_pairs[d_idx-1]
					d_func = func_detector_longest(p_code[p_pair[1]+1:d_pair[0]])
					r_dep_trees.append( {d_func:func_scanner( p_code[d_pair[0]+1:d_pair[1]] )} )
		else:
			r_dep_trees = {}
			for d_idx in range(len(lr_pairs)):
				d_pair = lr_pairs[d_idx]
				if d_idx == 0:
					d_func = func_detector_longest(p_code[0:d_pair[0]])
					r_dep_trees[d_func] = func_scanner( p_code[d_pair[0]+1:d_pair[1]] )
				else:
					p_pair = lr_pairs[d_idx-1]
					d_func = func_detector_longest(p_code[p_pair[1]+1:d_pair[0]])
					r_dep_trees[d_func] = func_scanner( p_code[d_pair[0]+1:d_pair[1]] )
	else: 
		# cannot be 0 since it's been filtered out at the beginning
		# unless: 1. %>% function(){(%>%)} 2. error in code
		# so treat it as a terminal layer and do not go deeper
		r_dep_trees = {}
		d_func = func_detector_longest(p_code[0:tmp_lb[0]])
		r_dep_trees[d_func] = None
	return r_dep_trees

def code_processor(p_code):
	if "%>%" in p_code:
		true_list = []
		tmp0 = ""
		tmp1 = p_code.split("\n")
		for i in range(len(tmp1)):
			if i==0:
				tmp0 = tmp1[i]
			else:
				if tmp1[i-1].endswith((",", "(", "%>%", ", ", "( ", "%>% ")):
					tmp0 += tmp1[i]
				else:
					true_list.append(tmp0)
					tmp0 = tmp1[i]
		true_list.append(tmp0) # the last one
		# print("true list: {}".format(true_list))
		if len(true_list)==1:
			r_dep_trees = func_scanner(true_list[0], is_outermost_layer=True)
		else:
			r_dep_trees = []
			for d_code in true_list:
				if "%>%" in d_code:
					d_code_list = d_code.split("%>%")
					# print("dcodelist: {}".format(d_code_list))
					rdl = []
					for dd_code in d_code_list:
						rdl.append( func_scanner(dd_code) ) # not outermost, can be: dict/str/None, cannot be: list
					# print("rdl:{}".format(rdl))
					dd = None
					for d_item in rdl:
						if type(d_item)==dict:
							# extend key:None to key:{} to support dict insertion
							if d_item[list(d_item.keys())[0]] is None:
								d_item[list(d_item.keys())[0]] = {}
							if type(d_item[list(d_item.keys())[0]]) == str:
								d_item[list(d_item.keys())[0]] = {d_item[list(d_item.keys())[0]]:None}

							if type(dd)==dict:
								d_item[list(d_item.keys())[0]][list(dd.keys())[0]] = dd[list(dd.keys())[0]]
								dd = d_item
							else: # then it's str
								d_item[list(d_item.keys())[0]][dd] = {}
								dd = d_item
						else:
							dd = {d_item:dd} # recursive add
						# print("step dd: {}".format(dd))
					r_dep_trees.append(dd)
				else:
					r_dep_trees.append( func_scanner(d_code) )
	else:
		r_dep_trees = func_scanner(p_code.replace("\n"," "), is_outermost_layer=True)
	return r_dep_trees


test_code_1 = """unique(substr(names(df)[-1], 1, 3))"""
test_code_2 = """
unique(names(), chartr(), complex(double(), formatC()))
unique(substr(names(df)[-1], 1, 3))
"""
test_code_3 = """
df %>% select(-site) %>% names() %>% substr(1,3) %>% unique() %>%
  lapply(function(x){unite_(df, x, grep(x, names(df), value = TRUE), 
                            sep = '/', remove = TRUE) %>% select_(x)}) %>%
  bind_cols() %>% mutate(site = as.character(df$site)) %>% select(site, starts_with('D'))
"""
test_code_4 = """'mtcars %>%\n     mutate(mpg=replace(mpg, cyl==4, NA)) %>%\n     as.data.frame()\n'"""

# print(func_scanner(test_code_1, is_outermost_layer=True))
# print(func_scanner(test_code_2.replace("\n"," "), is_outermost_layer=True))

# print(code_processor(test_code_1))
# print(code_processor(test_code_2))
# print(code_processor(test_code_3))
# print(code_processor(test_code_4))
# raise

# print(func_detector_longest("namesflwkejfl"))

with open("./dataset.pkl","rb") as f:
	dataset = pickle.load(f)
# (metadata, question, answers) - tuple
# [{"acpt":bool, "vote":int, "ansr":[(0,str),(1,str),...]}, {}, {}, ...]

parsed_dataset = dataset

n_total = 0
n_done = 0
for d_key in dataset.keys():
	n_total += len(dataset[d_key])

# add one more kv: "ansr_parsed"
for d_key in parsed_dataset.keys():
	for i in range(len(parsed_dataset[d_key])):
		n_done += 1
		print("\r# Processing {}/{}".format(n_done,n_total),end="")
		for j in range(len(parsed_dataset[d_key][i][2])):
			d_item = parsed_dataset[d_key][i][2][j]
			parsed_dataset[d_key][i][2][j]["ansr_parsed"] = []
			for d_ansr in d_item["ansr"]:
				if d_ansr[0]==1: # code
					# !!! NOTICE: add a minimum code length req
					if len(d_ansr[1])>20:
						parsed_dataset[d_key][i][2][j]["ansr_parsed"].append(code_processor(d_ansr[1]))
print()

with open("./parsed_dataset.pkl","wb") as f:
	pickle.dump(parsed_dataset, f)

"""
parsed_dataset = {
	"DPLYR":[
		(
		/metadata/{
			"url":str, "vote":int, "ansr":int, "acpt":int, "view":int, "title":str, "tags":list of str, "time":float
		},
		/question/[
			(0,txt),(1,code),...
		],
		/answers/[
			{"acpt":bool, "vote":int, "ansr":[(0,str),(1,code),...], "ansr_parsed":[ [],[],... ]},
			{},
			...
		],
		)
	],
	"TIDYR":...
}
"""