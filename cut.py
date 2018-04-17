#-*- coding:utf-8 -*-
from finalseg import *
from form_gen_trie import *
min_freq=0.0
import os
path = os.getcwd()

FREQ=form_gen_trie(path+'\\dict.txt')

def get_DAG(sentence):
    DAG={}
    N=len(sentence)
    for i in range(N):
        k=i
        word = sentence[i]
        DAG[i]=[]
        while k<N :
            if word in FREQ and FREQ[word]:
                DAG[i].append(k)
            k=k+1
            word=sentence[i:k+1]
        if i not in DAG[i]:
            DAG[i].insert(0,i)
    return DAG

def calc(sentence,DAG):
    route={}
    N=len(sentence)
    route[N]=(0.0,'')
    for idx in range(N-1,-1,-1):
        candidates=[(FREQ.get(sentence[idx:x+1],min_freq)+
        route[x+1][0],x)for x in DAG[idx]]
        route[idx]=max(candidates)
    return route

def cut_at_first(route,sentence):
    ed = -1
    for pos in range (len(sentence)):
        if pos > ed:
            ed = int(route[pos][-1])
            if pos == ed:
                print (sentence[pos]+'|',end = '')
            else:
                print (sentence[pos:ed+1]+'|',end = '')

def __cut_DAG(sentence):
    DAG =get_DAG(sentence)
    route=calc(sentence, DAG)
    x = 0
    buf = ''
    N = len(sentence)
    while x < N:
        y = route[x][1] + 1
        l_word = sentence[x:y]
        if y - x == 1:
            buf += l_word
        else:
            if buf:
                if len(buf) == 1:
                    yield buf
                    buf = ''
                else:
                    if not FREQ.get(buf):
                        for t in cut(buf):
                            yield t
                    else:
                        for elem in buf:
                            yield elem
                    buf = ''
            yield l_word
        x = y

    if buf:
        if len(buf) == 1:
            yield buf
        elif not FREQ.get(buf):
            for t in cut(buf):
                yield t
        else:
            for elem in buf:
                yield elem

def __cut_DAG_for_single(sentence,possi_new):
    DAG =get_DAG(sentence)
    route=calc(sentence, DAG)
    x = 0
    buf = ''
    N = len(sentence)
    while x < N:
        y = route[x][1] + 1
        l_word = sentence[x:y]
        if y - x == 1:
            buf += l_word
        else:
            if buf:
                if len(buf) == 1:
                    buf = ''
                else:
                    if not FREQ.get(buf):
                        possi_new.append(buf)
                    buf = ''
        x = y

    if buf:
        if len(buf) != 1 and not FREQ.get(buf):
            possi_new.append(buf)
    return possi_new

def cut_at_last(sentence):
    cut_list=[]
    for word in __cut_DAG(sentence):
        cut_list.append(word)
    return '|'.join(cut_list)

def possi(sentence):
    possi_new=[]
    possi_new= __cut_DAG_for_single(sentence,possi_new)
    a=len(possi_new)
    for i in range(len(possi_new)):
        for p in range(len(possi_new[i])-1):
            for q in range(1,len(possi_new[i])-p):
                possi_new.append(possi_new[i][p:p+q+1])
    for i in range(a):
        possi_new.pop(0)
    return possi_new





