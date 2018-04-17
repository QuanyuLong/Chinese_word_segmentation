import prob_start,prob_trans,prob_emit
start_p=prob_start.P
trans_p=prob_trans.P
emit_p=prob_emit.P
import math
from BMES import *
import os
PrevStatus={
'B':('E','S'),
'M':('M','B'),
'S':('S','E'),
'E':('B','M')
}

ThenStatus={
'B':('E','M'),
'M':('E','M'),
'S':('B','S'),
'E':('B','S')
}

MIN_FLOAT=-3.14e100
path = os.getcwd()
string=readfile(path+'\\ceshi.txt')

forward_net={}
backward_net={}

maxIterNum=20

seg,out_seq=remove_punc(string)
hidden_seq=BMES(seg)

sentence=[]
for i in range(len(out_seq)):
    sentence.append((out_seq[i],hidden_seq[i]))
states='BMSE'

def log(value):
        if value == 0:
            return MIN_FLOAT
        else:
            return math.log(value)

def buildnet():
    global forward_net
    global backward_net
    if forward_net is None or len(forward_net.keys()) == 0:
        for t, sw in enumerate(sentence):
            prob_t = {}
            for s in states:
                if t == 0:
                    prob_t[s] = start_p[s]+emit_p[s].get(sw[0], MIN_FLOAT)
                else:
                    em_p = emit_p[s].get(sw[0], MIN_FLOAT)
                    prob_t[s] = log(sum([math.e**(forward_net[t-1][s0]+trans_p[s0].get(s,MIN_FLOAT)+em_p)for s0 in states]))
            forward_net[t] = prob_t
    if backward_net is None or len(backward_net.keys()) == 0:
        T = len(sentence)-1
        for i in range(T, -1, -1):
            prob_t = {}
            if i == T:
                prob_t = dict([(s, 1) for s in states])
            else:
                for s in states:
                    prob_t[s]=log(sum([math.e**(backward_net[i+1][s1]+trans_p[s].get(s1, MIN_FLOAT)+emit_p[s1].get(sentence[i+1][0],MIN_FLOAT))for s1 in states]))
            backward_net[i] = prob_t

def forward_for_all(sentence,states):
    sos={}
    for i,char in enumerate(sentence):
        if i==0:
            for y in states:
                sos[y]=start_p[y]+emit_p[y].get(char,MIN_FLOAT)
        else:
            buf=dict(sos)
            for y in states:
                em_p=emit_p[y].get(char,MIN_FLOAT)
                sos[y]=log(sum(math.e**(buf[y0]+trans_p[y0].get(y,MIN_FLOAT)+em_p) for y0 in PrevStatus[y]))
    return log(sum(math.e**sos[y] for y in 'SE'))

def pro_of_certain(sentence,test_path):
    for i,char in enumerate(sentence):
        if i==0:
            p=start_p[test_path[i]]+emit_p[test_path[i]].get(char,MIN_FLOAT)
        else:
            tr_p=trans_p[test_path[i-1]].get(test_path[i],MIN_FLOAT)
            em_p=emit_p[test_path[i]].get(char,MIN_FLOAT)
            p=p+tr_p+em_p
    return p

def forward(sentence,states):
    if forward_net is not None and 0 in forward_net.keys():
        return forward_net[len(sentence)-1]
    prob_f={}
    for i,char in enumerate(sentence):
        if i==0:
            for y in states:
                prob_f[y]=start_p[y]+emit_p[y].get(char[0],MIN_FLOAT)
        else:
            buf=dict(prob_f)
            for y in states:
                em_p=emit_p[y].get(char[0],MIN_FLOAT)
                prob_f[y]=log(sum(math.e**(buf[y0]+trans_p[y0].get(y,MIN_FLOAT)+em_p)for y0 in PrevStatus[y]))
    return prob_f

def backward(sentence,states):
    if backward_net is not None and 0 in backward_net.keys():
        return backward_net[len(sentence)-1]
    prob_b={}
    T=len(sentence)-1
    for i in range(T,-1,-1):
        if i==T:
            for y in states:
                prob_b[y]=0
        else:
            buf=dict(prob_b)
            for y in states:
                prob_b[y]=log(sum(math.e**(buf[y0]+trans_p[y].get(y0,MIN_FLOAT)+emit_p[y0].get(sentence[i+1],MIN_FLOAT)) for y0 in ThenStatus[y]))
    return prob_b

def get_r(sentence,t,states):
    prob_r={}
    sum=0.0
    prob_forward=forward(sentence[0:t+1],states)
    prob_backward=backward(sentence[t:],states)
    for y in states:
        prob_r[y]=prob_forward[y]+prob_backward[y]
        sum=sum+math.e**prob_r[y]
    buf = dict(prob_r)
    for y in states:
        if math.e**buf[y]==0.0:
            prob_r[y]=MIN_FLOAT
        else:
            if math.e**buf[y] == 0.0:
                prob_t[y]=MIN_FLOAT
            else:
                prob_r[y]=log((math.e**buf[y])/sum)
    return prob_r

def get_xi(sentence,t,states):
        xi={}
        sum=0.0
        T=len(sentence)
        for s in states:
            xi[s] = 1
        if t==T-1:
            return None
        prob_forward=forward(sentence[0:t+1],states)
        prob_backward=backward(sentence[t:T],states)
        for s in states:
            for s1 in states:
                tmp=(s, s1)
                xi[tmp]=prob_forward[s]+prob_backward[s1]+trans_p[s].get(s1,MIN_FLOAT)+emit_p[s1].get(sentence[t+1],MIN_FLOAT)
                sum += math.e**xi[tmp]
        buf=dict(xi)
        for s in states:
            for s1 in states:
                tmp=(s,s1)
                if math.e**buf[tmp]==0.0:
                    xi[tmp]=MIN_FLOAT
                else:
                    xi[tmp]=log(math.e**buf[tmp]/sum)
        return xi

def doEM():
    global maxIterNum
    while maxIterNum > 0:
        buildnet()
        seq_r = {}
        seq_xi = {}
        for i, sw in enumerate(sentence):
            seq_r[i] = get_r(sentence, i, states)
            seq_xi[i] = get_xi(sentence, i, states)
        updatePI(seq_r, states)
        updateTrans(seq_r, seq_xi, states)
        updateEmit(sentence, seq_r, states)
        if ErrorIsOk(sentence):
            break
        maxIterNum -= 1

def updatePI(seq_r, states):
    for s in states:
        start_p[s] = seq_r[0][s]

def updateTrans(seq_r, seq_xi, states):
    for s in states:
        sum_r=0.0
        for t in range(0,len(seq_r)-1):
            sum_r+=math.e**seq_r[t][s]
        for s1 in states:
            sum_xi=0.0
            for t in range(0,len(seq_r)-1):
                sum_xi += math.e**seq_xi[t][(s, s1)]
            trans_p[s][s1] =log(sum_xi/sum_r)

def updateEmit(sentence, seq_r, states):
    for s in states:
        sum_r = 0.0
        state_output={}
        for t in range(0,len(seq_r)):
            sum_r+=math.e**seq_r[t][s]
            state_output.setdefault(sentence[t],0.0)
            state_output[sentence[t]] += math.e**seq_r[t][s]
        for o in state_output.keys():
            emit_p[o]=log(state_output[o]/sum_r)

def ErrorIsOk(sentence):
    prob, path =viterbi([s[0] for s in sentence],states,start_p,trans_p,emit_p)
    print(prob,path)
    for state_viterbi in path:
        for right in sentence:
            if right[1] != state_viterbi:
                return False
    return True


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    for y in states:
        V[0][y] = start_p[y] + emit_p[y].get(obs[0], MIN_FLOAT)
        path[y] = [y]
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            em_p = emit_p[y].get(obs[t], MIN_FLOAT)
            (prob, state) = max([(V[t-1][y0] + trans_p[y0].get(y, MIN_FLOAT) + em_p, y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return prob, path[state]

doEM()


