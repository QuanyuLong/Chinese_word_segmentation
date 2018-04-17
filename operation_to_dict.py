import re
from form_gen_trie import *
import os
import string
path = os.getcwd()

def just_Chinese(word):
    p = re.compile(r'^[\u4E00-\u9FA5]|[a-zA-Z]')
    string1 = b'\xe3\x80\x82\xef\xbc\x8c\xef\xbc\x9f\xef\xbc\x88\xef\xbc\x89\xef\xbc\x9b\xef\xbc\x9a\xe2\x80\x98\xe2\x80\x99\xe2\x80\x9c\xe2\x80\x9d\xe3\x80\x90\xe3\x80\x91\xe3\x80\x81\xef\xbc\x81\xe2\x80\x94\xe2\x80\x94\xe3\x80\x8a\xe3\x80\x8b\xe2\x80\xa6\xe2\x80\xa6\xe3\x80\x8c\xe3\x80\x8d\xc2\xb7'.decode('utf-8')
    string2 = string.punctuation
    if word == '':
        return False
    else:
        for char in word:
            if re.match(p,char) == None and char not in string1 and char not in string2:
                pass
            else:
                return False
        return True

def Chinese(word):
    p1 = re.compile(r'^[\u4E00-\u9FA5]|[a-zA-Z]')
    string1 = b'\xe3\x80\x82\xef\xbc\x8c\xef\xbc\x9f\xef\xbc\x88\xef\xbc\x89\xef\xbc\x9b\xef\xbc\x9a\xe2\x80\x98\xe2\x80\x99\xe2\x80\x9c\xe2\x80\x9d\xe3\x80\x90\xe3\x80\x91\xe3\x80\x81\xef\xbc\x81\xe2\x80\x94\xe2\x80\x94\xe3\x80\x8a\xe3\x80\x8b\xe2\x80\xa6\xe2\x80\xa6\xe3\x80\x8c\xe3\x80\x8d\xc2\xb7'.decode('utf-8')
    string2 = string.punctuation
    if word =='':
        return False
    else:
        for i in word:
            if re.match(p1,i) == None and i != ' ' and i not in string1 and i not in string2:
                return True
            else:
                pass
        return False

def add_to_dict(word,frequency,):
    judge = Chinese(word)
    if judge == True:
        with open(path+'\\dict.txt','a',-1,'utf-8') as origin_file:
            origin_file.write(word+' '+str(frequency)+' ne')
    else:
        return judge

def general_service_word(word,level = 5):
    with open(path+'\\dict.txt','r',-1,'utf-8') as origin_file:
        origin = origin_file.read()
    p1 = re.compile(r'\s[a-z]+')
    p2 = re.compile(r'\n')
    p3 = re.compile(r'\s')
    leaflist = p1.split(p2.sub('', origin))
    count = 0
    for leaf in leaflist:
        if leaf == '':
            del leaflist[count]
        else:
            leafpart = p3.split(leaf)
            if leafpart[0] == word:
                leafpart[-1] = str(int(leafpart[-1])+level)
            leaflist[count] = ' '.join(leafpart)
        count += 1
    os.remove(path+'\\dict.txt')
    with open(path+'\\dict.txt', 'w', -1, 'utf-8') as after_file:
        after = ' ne'.join(leaflist)+' ne'
        after_file.write(after)

def search(word):
    p = re.compile(r'\s')
    judge = Chinese(word)
    n = False
    answer = []
    if judge == True:
        wordlist = form_gen_trie(path+'\\dict.txt')
        for wordfreq in wordlist:
            if word in wordfreq :
                answer.append(p.split(wordfreq)[0])
                n = True
        if n == False :
            return False
        else:
            answer.sort(key = len)
            return answer
    else:
        return judge

def search_abs(word):
    p = re.compile(r'\s')
    judge = Chinese(word)
    if judge == True:
        for wordfreq in form_gen_trie(path+'\\dict.txt'):
            if word == p.split(wordfreq)[0]:
                return True
        return False
    else:
        return judge


def automatic_add(sentence_after_seg):
    sentence_list = sentence_after_seg.split('|')
    for block in sentence_list:
        judge = just_Chinese(block)
        if judge == True:
            if search_abs(block) == True:
                general_service_word(block,1)
            else:
                add_to_dict(block,1)
        else:
            pass

def readfile(path):
    try:
        bfile = open(path, 'r', -1, 'utf-8')
        filestr = bfile.read()
    except UnicodeDecodeError:
        try:
            bfile = open(path, 'r', -1, 'gbk')
            filestr = bfile.read()
        except UnicodeDecodeError:
            return 'The file isn\'t coded with \'gbk\' or\'utf-8\'!'
    bfile.close()
    return filestr



