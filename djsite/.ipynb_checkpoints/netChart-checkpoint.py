import nltk
import json
import time
import math
import queue
from nltk.stem import PorterStemmer 
from nltk.metrics import edit_distance

tokens_li = []
tokens_li_stem = []
token_2_stem = dict()
stem_to_tokens = dict()
inv_index = dict()
tokens_li_1dim = []
stem_times_per_article = []
replace_li = ['(', '//', ':', ')', '.', '!', ',', '   ', '  ', '"', '\''] 
stopword_add_li = ['THE', 'The', 'To', 'We', 'A']
label_root = list()
ps = PorterStemmer()


def init():
    try:
        from nltk.corpus import stopwords    
    except:
        nltk.download('stopwords')
        from nltk.corpus import stopwords
    EngStopWords = set(stopwords.words('english'))

    id_file = open('pubmed_article_3w4.json', 'r')
    id_list = json.load(id_file)['article']
    for i in  range(len(id_list)):
        tmp = id_list[i]['abstract']
        for j in replace_li:
            tmp = tmp.replace(j, ' ')
        id_list[i]['abstract'] = tmp

        tokens_li.append(tmp.split())
    for i in stopword_add_li:
        EngStopWords.add(i)
    for i in range(len(id_list)):
        tmp_li = []
        for j in range(len(tokens_li[i])):

            tmp = tokens_li[i][j]
            if tmp in EngStopWords:
                continue
            try:
                tmp_li.append(token_2_stem[tmp])
                tokens_li_1dim.append(token_2_stem[tmp])
            except:
                after_stem = ps.stem(tmp)
                tmp_li.append(after_stem)
                token_2_stem[tmp] = after_stem
                stem_to_tokens[after_stem] = tmp
                tokens_li_1dim.append(after_stem)
        tokens_li_stem.append(tmp_li)
        stem_times_per_article.append({})
        for j in tmp_li:
            try:
                stem_times_per_article[i][j] += 1
            except:
                stem_times_per_article[i][j] = 1
            try:
                inv_index[j].add(i)
            except:
                inv_index[j] = set()
                inv_index[j].add(i)

            
def zifChart(tar_str, ref):
    tar_str = find_root(tar_str)
    tar_time_dict = {}
    tar_time_li = []
    
    cnt = 0

    for it in stem_times_per_article:
        if tar_str in it:
            cnt += 1
            for itt in it:

                try:
                    tar_time_dict[itt] += 1
                except:
                    tar_time_dict[itt] = 1


    label = []
    data = []
    
    if len(ref) == 0:   
        print("hihi")
        for it in tar_time_dict:
            tar_time_li.append((tar_time_dict[it], it))
        tar_time_li = sorted(tar_time_li, reverse = True)
        for it in tar_time_li[0:100]:
            label.append(stem_to_tokens[it[1]])
            data.append(it[0])
            #data.append(math.log(it[0]))
    else:
        label = ref
        for it in label:
            try:
                data.append(tar_time_dict[token_2_stem[it]])
            except:
                data.append(0)
        
    return {'label':label, 'data':data}


def find_root(tar):
    if tar in token_2_stem:
        return token_2_stem[tar]
    if tar in stem_to_tokens:
        return tar

    mini = 1000
    mini_tar = str()
    
    for it in token_2_stem:
        tmp = edit_distance(it, tar)
        if tmp < mini:
            mini = tmp
            mini_tar = it
        elif tmp == mini and len(mini_tar) > len(it):
            mini = tmp
            mini_tar = it
    print(mini_tar)
    return token_2_stem[mini_tar]
    

def diging_start(start_tar):
    if len(tokens_li) == 0:
        init()
    

    dig_lvl = 0.1
    tree = dict()
    idDict = dict()
    NodeSet = list()
    EdgeSet = list()
    idx = 1
    
    start_tar = find_root(start_tar)
    print(start_tar)
    if not start_tar in stem_to_tokens:
        return {'tree':tree, 'root': start_tar, 'EdgeSet':EdgeSet, 'NodeSet':NodeSet}
    
    


    Q = queue.Queue()
    Q.put((1, start_tar, idx))
    NodeSet.append({'id':idx, 'label':stem_to_tokens[start_tar], 'shape': "star", 'size': 20, 'color': "#FB7E81"})
    idDict[start_tar] = idx



    idx = 1
    while not Q.empty():
        tar = Q.get()
        this_idx = tar[2]
        if tar[1] in tree:
            continue
        res = search_relat_word(tar[1])

        tree[tar[1]] = res
        for it in res:
            score = tar[0]*it[0] + LCS(inv_index[it[1]], inv_index[start_tar])
            if score > dig_lvl:  
                try:
                    nxt_id = idDict[it[1]]
                except:
                    idx += 1
                    nxt_id = idx
                    idDict[it[1]] = idx
                    NodeSet.append({'id':nxt_id, 'label':stem_to_tokens[it[1]]})
                if not it[1] in tree:
                    EdgeSet.append({'from': this_idx, 'to': nxt_id})
                    Q.put((score, it[1], nxt_id))
    return {'tree':tree, 'root': stem_to_tokens[start_tar], 'EdgeSet':EdgeSet, 'NodeSet':NodeSet}








            
def LCS(A, B):
    z = len(A.intersection(B))
    union_len = len(A)+len(B) - z
    return z / union_len

def topfive_append(self_li, tar):
    if len(self_li) < 5:
        self_li.append(tar)
    elif self_li[0] < tar:
        self_li[0] = tar
    else:
        return self_li      
    for idx in range(len(self_li)-1):
        if self_li[idx] > self_li[idx+1]:
            self_li[idx], self_li[idx+1] = self_li[idx+1], self_li[idx] # swap
        else:
            break
    return self_li
    
def search_relat_word(tar):
    tar_set = inv_index[tar]
    topfive = list()    
    for it in inv_index:
        if tar == it:
            continue
        score = LCS(tar_set, inv_index[it])
        topfive = topfive_append(topfive, (score, it))
    return topfive