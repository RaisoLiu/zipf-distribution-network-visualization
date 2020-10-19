from os import listdir, remove
from os.path import isfile, isdir, join
from django.http import HttpResponse
from django.shortcuts import render
from .forms import Addr_Form, Search_Form
from .js_func import build_inv_index_json, normalize_word
from .search_func import search_engine, art_get, typo
from .netChart import diging_start, zifChart
import json
import time


def network(request):
    tree_dict = {}
    if request.method == 'POST':
        ts = time.time()
        form = Search_Form(request.POST, request.FILES)
        if not form.is_valid():
            tree_dict['form'] = Search_Form()
            return render(request, 'add.html', tree_dict)
        
        search_obj = form.instance
        print(search_obj.target_str)
        tree_dict = diging_start(search_obj.target_str)
        tree_dict['form'] = Search_Form()
        if len(tree_dict['NodeSet']) == 0:
            tree_dict['msg'] = "no search result"
        else:
            
            tree_dict['zif'] = {}
            tree_dict['zif'][tree_dict['root']] = zifChart(tree_dict['root'], [])
            for it in tree_dict['NodeSet']:
                if it != tree_dict['root']:
                    tree_dict['zif'][it['label']] = zifChart(it['label'], tree_dict['zif'][tree_dict['root']]['label'])
            tree_dict['cost_time'] = str(time.time()-ts)
            tree_dict['search_done'] = 1
        return render(request, 'net-zif.html', tree_dict)
        
    else:
        tree_dict['form'] = Search_Form()
        return render(request, 'net-zif.html', tree_dict)


def homepage(request):
    return render(request, 'home.html')

def search_mark(art, tar):
    tar = normalize_word(tar)
    work_li = art.split()
    for it in range(len(work_li)):
        if normalize_word(work_li[it]) == tar:
            work_li[it] = ' <mark>' + work_li[it] + '</mark> ' 
    output = str()
    for it in work_li:
        output += it
        output += ' '
    return output

def searchpage(request):
    mypath = "."
    files = listdir(mypath)
    for f in files:
        fullpath = join(mypath, f)
        if isfile(fullpath) and f.split('.')[1] == 'json':
            if request.method == 'POST':
                form = Search_Form(request.POST, request.FILES)
                if form.is_valid():
                    search_obj = form.instance
                    res = search_engine(f, search_obj.target_str)
                    art_li = art_get(f, res)
                    search_str_li = []
                    for it, art in zip(res, art_li):
                        search_str_li.append({'times':str(it[0]), 'art':search_mark(art,search_obj.target_str)})
                    form = Search_Form()
                    search_tar_li = []
                    if len(search_str_li) == 0:
                        search_tar_li = typo(f, search_obj.target_str)
                    return render(request, 'search.html', {'search_obj':f, 'target_str': search_obj.target_str,'search_done': 1,'search_str_li': search_str_li, 'form': form, 'search_tar_li':search_tar_li})
            else:
                form = Search_Form()
                return render(request, 'search.html', {'search_obj': f, 'form': form})
    return render(request, 'search.html')

def addr_upload_view(request):
    if request.method == 'POST':
        
        mypath = "."
        files = listdir(mypath)
        img_obj = dict()
        for f in files:
            fullpath = join(mypath, f)
            if isfile(fullpath) and f.split('.')[1] == 'json':
                remove(fullpath)
            if isfile(fullpath) and f.split('.')[1] == 'png':
                img_obj['image_url'] = f
                
        form = Addr_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            source_name = str(request.FILES['file'])
            key = form.instance.key
            source_report = build_inv_index_json(source_name, key)
            return render(request, 'build.html', {'form': form, 'source_name': source_name, 'source_report': source_report, 'build_done': 1, 'img_obj':img_obj})
    else:
        form = Addr_Form()
    return render(request, 'build.html', {'form': form})
