#! /usr/bin/env python3
# coding: utf-8

 
def dictionnaire(token):
    compt = 0
    if token[compt] != '{':
        raise ValueError("{ attendu !")
    d = {}
    compt += 1
    cle, valeur, compt = paire(token, compt)
    d[cle] = valeur   
    while token[compt] == ',':
        compt += 1
        cle, valeur, compt = paire(token, compt)
        d[cle] = valeur   
    if token[compt] != '}':
        raise ValueError("} attendu !", token[compt])
    return d
 
def paire(token, compt):
    nouv_cle, compt = cle(token, compt)
    compt += 1    
    if token[compt] != ':':
        raise ValueError(': attendu !')
    compt += 1    
    nouv_valeur, compt = valeur(token, compt)
    return nouv_cle, nouv_valeur , compt
 
def cle(token, compt):  
    return num(token, compt)
 
def num(token, compt):
    cle = ''
    if token[compt] == ' ':
        compt += 1
    if token[compt] != '\"':
        raise ValueError('\" attendu !', token[compt])
    compt += 1
    while token[compt] != '\"':
    	cle = cle + token[compt]
    	compt += 1
    if token[compt] != '\"':
        raise ValueError('\" attendu !')
    return cle, compt
 
def valeur(token, compt):
    return components(token, compt)

def components(token, compt):
    compt += 1
    if token[compt] != '[':
    	raise ValueError('[ expected ! instead : ', token[compt] )
    l = []
    
    compt += 1
    new_component, compt = component(token, compt)
    l.append(new_component)
    while token[compt] == ',':
        compt += 1
        compt += 1 #there is a space after the ,
        new_component, compt = component(token, compt)
        l.append(new_component)
        if token[compt] == ' ' :
            compt += 1
    if token[compt] != ']':
        raise ValueError('] expected !', token[compt])
    compt += 1
    return l, compt
    
def component(token, compt):
    if token[compt] != '[':
    	raise ValueError('[ expected !')
    ID1, compt = ID(token, compt)
    ID2, compt = ID(token, compt)
    st1, compt = num_int(token, compt)
    en1, compt = num_int(token, compt)
    st2, compt = num_int(token, compt)
    en2, compt = num_int(token, compt)
    if token[compt] != ']':
        raise ValueError('] attendu !', token[compt])
    compt += 1
    return [ID1, ID2, st1, en1, st2, en2], compt

def ID(token, compt):
    if token[compt] == '[':
        compt += 1
    if token[compt] == ' ':
        compt += 1
    if token[compt] != '\"':
    	raise ValueError('\" expected !', token[compt])
    i = ""
    compt += 1
    while token[compt] != '\"':
        i = i+ token[compt]
        compt += 1
    compt += 1
    compt += 1
    if token[compt] != ' ':
        raise ValueError('space expected', token[compt])
    return i, compt
    
def num_int(token, compt):
    compt += 1
    if token[compt] == ' ':
        compt += 1
    i = ""
    while token[compt] != ','and token[compt] != ']':
        i = i + token[compt]
        compt += 1
    return int(i), compt 
    




def parse_Diffuse(input_diffuse):
    d = dictionnaire(input_diffuse)
    return d
    
  
