import json
import xmltodict
from nltk.stem import PorterStemmer 
import json
import nltk
import matplotlib.pyplot as plt
import time

def path_json(js, pth_li, lvl):
    if pth_li[0] == ' ':
        return js
    if lvl < len(pth_li):
        try:
            return path_json(js[pth_li[lvl]], pth_li,lvl+1)
        except:
            return js
    else:
        return js

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def normalize_word(tar):
    cg = str()
    for t in tar:
        if t.isalpha():
            cg += t.lower()
    try:
        return stemmer.stem(cg)
    except:
        stemmer = PorterStemmer()
        return stemmer.stem(cg)

def dfs_find_list(source):
    if isinstance(source,dict):
        for it in source.keys():
            return dfs_find_list(source[it])
    elif isinstance(source,list):
        return source
    else:
        print("error dfs_find_list")

def dfs_find_text(source, key):
    string_in_key = str()
    if isinstance(source, dict):
        for it in source.keys():
            if it == key:
                if isinstance(source[it], str):
                    string_in_key = string_in_key + string_plus(source[it])
                else:
                    string_in_key = string_in_key + string_plus(dfs_dict_string(source[it]) ) 
            else:
                string_in_key = string_in_key + string_plus(dfs_find_text(source[it], key))
    return string_in_key

def dfs_dict_string(source):
    string_in_key = str()
    if isinstance(source, dict):
        for it in source.keys():
            if isinstance(source[it], str):
                string_in_key = string_in_key + string_plus(source[it])
            else:
                string_in_key = string_in_key + string_plus(dfs_dict_string(source[it]))
    if isinstance(source, list):
        for it in source:
            if isinstance(it, str): 
                string_in_key = string_in_key + string_plus(it)
            else:
                string_in_key = string_in_key + string_plus(dfs_dict_string(it))
    return string_in_key

def string_plus(source):
    output = ' '
    try:
        if len(source) > 10:            
            output = output + source
    except:
        pass
    return output

def build_inv_index_json(source_name, key):
    tStart = time.time()
    
    source_dict = dict()
    source_report = dict()
    article_list = []
    tokens = []
    tokens_o = []
    word_set = []
    num_sentences = 0
    w_token = dict()
    w_map = dict()
    w_sum_num = 0
    
    with open(str('media/') + source_name, 'r') as file_stream:
        source_file_string = file_stream.read()
        if is_json(source_file_string):
            source_dict = json.loads(source_file_string)
        else:
            try:
                source_dict = xmltodict.parse(source_file_string) 
            except:                    
                return source_report
    
    raw_article_list = dfs_find_list(source_dict)
    for it in raw_article_list:
        tmp = dfs_find_text(it, key)
        num_sentences = num_sentences + len(tmp.split('.'))
        article_list.append(tmp)

    
    
    for article, idx in zip(article_list, range(len(article_list))):
        article_word_li = article.split(' ')
        for word in article_word_li:
            word_o = word
            word = normalize_word(word)
            if len(word) > 1:
                word_set.append((word, idx))
                tokens.append(word)
                tokens_o.append(word_o)

    freq = nltk.FreqDist(tokens)

    fig = plt.figure(figsize = (23,5))
    plt.gcf().subplots_adjust(bottom=0.15) 

    freq.plot(100, cumulative=False)

    fig.savefig('media/freqDist.png', bbox_inches = "tight")
    plt.close()
    
    freq = nltk.FreqDist(tokens_o)

    fig = plt.figure(figsize = (23,5))
    plt.gcf().subplots_adjust(bottom=0.15) 

    freq.plot(100, cumulative=False)

    fig.savefig('media/freqDist2.png', bbox_inches = "tight")
    plt.close()
    

    for word in word_set:
        w_sum_num = w_sum_num + 1
        try:
            w_map[word[0]].append(word[1])
        except:
            w_map[word[0]] = [word[1]]
  
    

    name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) 
    
    with open(name+'_inv_index.json', 'w') as f:
        json.dump({'w_map':w_map, 'article_list':article_list, 'tokens_o':tokens_o}, f)
    
    
    source_report['num_dword'] = len(w_map)
    source_report['num_art'] = len(article_list)
    source_report['num_char'] = len(source_file_string)
    source_report['num_word'] = w_sum_num
    source_report['num_sentences'] = num_sentences
    
    tEnd = time.time()
    print("\n build_inv_index_json \n It cost %f sec" % (tEnd - tStart))

    return source_report