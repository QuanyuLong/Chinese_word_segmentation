from cut import*
from form_gen_trie import *

def seg_for_txt(originfile,savepath):
    with open(originfile,'r') as ready:
        originstr = ready.read()
        blocklist = seg(originstr)
        seglist = []
        for sentence in blocklist:
            DAG = get_DAG(sentence)
            route = calc(sentence,DAG)
            for i in cut_at_first(route,sentence):
                seglist.append(i)
    with open(savepath,'w',-1,'utf-8') as after_file:
        segstr = ''.join(seglist)
        after_file.write(segstr)

seg_for_txt('text.txt','after.txt')


