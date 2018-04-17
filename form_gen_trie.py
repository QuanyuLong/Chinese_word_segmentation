
import re
import math

def form_gen_trie(dictionary):                                    #this return a list
    with open(dictionary,'r',-1,'utf-8') as origin_file:
        origin = origin_file.read()
    p1 = re.compile(r'\s[a-z]+')
    p2 = re.compile(r'\n')
    p3 = re.compile(r'\s')
    leaflist = p1.split(p2.sub('',origin))
    total = 0.0
    count = 0
    for leaf in leaflist:
        if leaf == '':
            del leaflist[count]
        else:
            leafpart = p3.split(leaf)
            total += float(leafpart[-1])
        count += 1
    count = 0
    frequency = {}
    for leaf in leaflist:
        leafpart = p3.split(leaf)
        leafpart[-1] = str(math.log(float(leafpart[-1])/total))
        count += 1
        frequency[leafpart[0]] = float(leafpart[-1])
    return frequency


def seg(text):
    result_list = []
    t = 0
    for i in range(len(text)):
            if text[i] == '\n':
                result_list += [text[t:i + 1]]
                t = i + 1
    result_list += [text[t:]]
    return (result_list)










