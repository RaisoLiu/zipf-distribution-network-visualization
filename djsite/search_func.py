import json
from os import listdir
from os.path import isfile, isdir, join
from .js_func import is_json, normalize_word
from nltk.metrics import edit_distance
import time

def art_get(f, res):
    tStart = time.time()
    art_js_set = []
    inquire = res
    with open(f, 'r') as f_stream:
        f_str = f_stream.read()
        if is_json(f_str):
            art_js_set = json.loads(f_str)

    res = []
    for it in inquire:
        res.append(art_js_set['article_list'][it[1]])
        
    tEnd = time.time()
    print("\n art_get \nIt cost %f sec" % (tEnd - tStart))
    return res

def typo(addr, tar_str):
    tStart = time.time()
    file_js = dict()
    with open(addr, 'r') as f_stream:
        f_str = f_stream.read()
        if is_json(f_str):
            file_js = json.loads(f_str)
    
    inv_idx = file_js['tokens_o']
    tar_str = normalize_word(tar_str)
    result_li = []
    for it in inv_idx:
        result_li.append((edit_distance(tar_str,normalize_word(it)), it))
    result_li = sorted(result_li)
    
    return_li = []
    num_res = len(result_li)
    lim = min(5, num_res)
    
    for idx in range(lim):
        return_li.append({'dist':result_li[idx][0], 'str':result_li[idx][1]})
        
    tEnd = time.time()
    print("\n typo \nIt cost %f sec" % (tEnd - tStart))
    return return_li


def search_engine(addr, tar_str):
    tStart = time.time()
    file_js = dict()
    with open(addr, 'r') as f_stream:
        f_str = f_stream.read()
        if is_json(f_str):
            file_js = json.loads(f_str)
        else:
            return ['','inv_index_json_Destroyed']
    
    inv_idx = file_js['w_map']
    result_count = dict()
    tar_li = tar_str.split(' ')
    
    for tar in tar_li:
        try:
            for no in inv_idx[normalize_word(tar)]:
                try:
                    result_count[no] = result_count[no]+1
                except:
                    result_count[no] = 1
        except:
            pass
    result_li = []
    
    for cnt in result_count:
        result_li.append((result_count[cnt], cnt))
    result_li = sorted(result_li)
    
    return_li = []
    num_res = len(result_li)
    lim = min(10, num_res)
    
    for idx in range(lim):
        return_li.append(result_li[-1 - idx])
    
    tEnd = time.time()
    print("\n search_engine \nIt cost %f sec" % (tEnd - tStart))
    return return_li