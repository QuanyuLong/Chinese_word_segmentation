from operation_to_dict import *

def remove_punc(string):
    blocklist = string.split('|')
    atlast = []
    for block in blocklist:
        if just_chinese(block) == True:
            atlast.append(block)
    return ('|'.join(atlast).replace(b'\xe3\x80\x82'.decode('utf-8'),'') , ''.join(atlast).replace(b'\xe3\x80\x82'.decode('utf-8'),''))

def BMES(string_seg_nop):
    BMESlist = []
    for i in range(len(string_seg_nop)):
        if just_chinese(string_seg_nop[i]) == True :
            if i == 0 and string_seg_nop[1] != '|':
                BMESlist.append('B')
            elif i == 0 and string_seg_nop[1] == '|':
                BMESlist.append('S')
            elif i+1 == len(string_seg_nop):
                if string_seg_nop[i-1] == '|':
                    BMESlist.append('S')
                if string_seg_nop[i-1] != '|':
                    BMESlist.append('E')
            elif i > 0 and string_seg_nop[i-1] != '|' and string_seg_nop[i+1] != '|':
                BMESlist.append('M')
            elif i > 0 and string_seg_nop[i-1] == '|' and string_seg_nop[i+1] == '|':
                BMESlist.append('S')
            elif i > 0 and string_seg_nop[i-1] != '|' and string_seg_nop[i+1] == '|':
                BMESlist.append('E')
            elif i > 0 and string_seg_nop[i-1] == '|' and string_seg_nop[i+1] != '|':
                BMESlist.append('B')
    return ''.join(BMESlist)
