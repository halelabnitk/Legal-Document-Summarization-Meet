from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lz = WordNetLemmatizer()

import re
import pickle
import os
import pandas as pd

def remove_spaces_and_periods(abbreviation):
    '''
    Cleans abbreviation
    Cr. P. C. -> CrPC
    '''

    cleaned_string = abbreviation.replace(" ", "").replace(".", "")
    return cleaned_string

def merge_contiguous_single_chars(strings):
    '''
    In most of the cases single characters doesnt make any sense, there are single characters that usually represents
    last names or a char of a abbreviation.
    That why we are using this behaviour to solve the problem of abbreviation by combining single characters.
    In this way we can indentify our abbreviation in our text.
    This function just merges all those characters so that we can just look at a word later on map that with its full form.
    '''

    merged_strings = []
    current_string = ""

    for s in strings:
        if len(s) == 1:
            current_string += s
        else:
            if len(current_string)==1:
                merged_strings.append(current_string)
                current_string = ""
            elif len(current_string)>1:
                merged_strings.append(remove_spaces_and_periods(current_string))
                current_string = ""
            merged_strings.append(s)

    if current_string:
        merged_strings.append(remove_spaces_and_periods(current_string))

    return merged_strings

#Loading mappings that we got from ./analysis/analysis.
# here is our abbreviations mapping dictionary
with open('../intermediate/mappings.pickle','rb') as file:
    mappings = pickle.load(file)

#got these legal stopwords by analysis
with open('../intermediate/legal_stopwords.pickle','rb') as file:
    legal_stopwords = pickle.load(file)

def ValidationOfRomanNumerals(string):
    return bool(re.search(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",string))

def value(r):
    if (r == 'I'):
        return 1
    if (r == 'V'):
        return 5
    if (r == 'X'):
        return 10
    if (r == 'L'):
        return 50
    if (r == 'C'):
        return 100
    if (r == 'D'):
        return 500
    if (r == 'M'):
        return 1000
    return -1
 
def romanToDecimal(str):
    res = 0
    i = 0
    if not ValidationOfRomanNumerals(str):
        return str
    while (i < len(str)):
        s1 = value(str[i])
        if (i + 1 < len(str)):
            s2 = value(str[i + 1])
            if (s1 >= s2):
                res = res + s1
                i = i + 1
            else:
                res = res + s2 - s1
                i = i + 2
        else:
            res = res + s1
            i = i + 1
    return f"{res}"

def preprocess(text):
    jgs = []
    for line in text: 
        content = wordpunct_tokenize(line)
        content = merge_contiguous_single_chars(content)
        jgs.append(content)

    newj = []
    for lst in jgs:
        j=0
        dummy = []
        while j < len(lst)-1:
            temp = remove_spaces_and_periods(lst[j] + lst[j+1])
            if temp in mappings.keys():
                dummy.append(mappings[temp])
                j+=2
            elif lst[j] in mappings.keys():
                dummy.append(mappings[lst[j]])
                j+=1
            else :
                dummy.append(lst[j])
                j+=1
        if j<len(lst):
            if lst[j] in mappings.keys():
                dummy.append(mappings[lst[j]])
            else:
                dummy.append(lst[j])
        newj.append(dummy)
    
    restricted_words = stopwords.words('english')+legal_stopwords
    extras = ["'t","'ve","'d"," ",""]
    lst = []
    for j in range(len(newj)):
        review = [lz.lemmatize(romanToDecimal(word.upper()).lower()) for word in newj[j] if word.lower() not in restricted_words and word.lower() not in extras]
        review = " ".join(review)
        review = re.sub('[^a-zA-Z0-9]',' ', review)
        review = (re.sub(' +', ' ', review)).strip()
        if len(review)>0 : lst.append(review)
    return lst