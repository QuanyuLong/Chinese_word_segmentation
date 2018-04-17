import re
import prob_start,prob_trans,prob_emit
start_p=prob_start.P
trans_p=prob_trans.P
emit_p=prob_emit.P

PrevStatus = {
'B':('E','S'),
'M':('M','B'),
'S':('S','E'),
'E':('B','M')
}
MIN_FLOAT=-3.14e100

def viterbi(sentence, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    for y in states: #init
        V[0][y] = start_p[y] + emit_p[y].get(sentence[0],MIN_FLOAT)
        path[y] = [y]
    for t in range(1,len(sentence)):
        V.append({})
        newpath = {}
        for y in states:
            em_p = emit_p[y].get(sentence[t],MIN_FLOAT)
            (prob,pre_state ) = max([(V[t-1][y0] + trans_p[y0].get(y,MIN_FLOAT) + em_p ,y0) for y0 in PrevStatus[y] ])
            V[t][y] =prob
            newpath[y] = path[pre_state] + [y]
        path = newpath

    (prob, final_state) = max([(V[len(sentence) - 1][y], y) for y in ('E','S')])

    return (prob, path[final_state])

def __cut(sentence):
    global emit_P
    prob, pos_list = viterbi(sentence, 'BMES', start_p, trans_p, emit_p)
    begin,nexti = 0,0
    for i, char in enumerate(sentence):
        pos = pos_list[i]
        if pos == 'B':
            begin = i
        elif pos == 'E':
            yield sentence[begin:i + 1]
            nexti = i + 1
        elif pos == 'S':
            yield char
            nexti = i + 1
    if nexti < len(sentence):
        yield sentence[nexti:]

re_han = re.compile("([\u4E00-\u9FD5]+)")
re_skip = re.compile("(\d+\.\d+|[a-zA-Z0-9]+)")


def cut(sentence):
    blocks = re_han.split(sentence)
    for blk in blocks:
        if re_han.match(blk):
            for word in __cut(blk):
                yield word
        else:
            tmp = re_skip.split(blk)
            for x in tmp:
                if x:
                    yield x
