import os
import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer

loc = "F:\\internship\\blackcoffer\\Output Data Structure.xlsx"
temp = pd.read_excel(loc, sheet_name='Sheet1', engine='openpyxl')
df_out = pd.DataFrame(temp, columns=['URL'])

out_loc = "F:\\internship\\blackcoffer\\Output.xlsx"
out_wb = pd.ExcelWriter(out_loc, engine='xlsxwriter')

output = []
stop_words_loc = "F:\\internship\\blackcoffer\\stop_words\\"
stop_words = []
stop_files = os.listdir(stop_words_loc)
for x in stop_files:
    loc = stop_words_loc + x
    with open(loc,'r') as file:
        text = file.read()
    for words in text.split():
        stop_words.append(words)


print(stop_words)

with open("F:\\internship\\blackcoffer\\"+'total.txt','w') as file:
    for word in stop_words:
        file.write(word+"\n")


'''
url_loc = "F:\\internship\\blackcoffer\\text\\"
url_files = os.listdir(url_loc)
#text_words = []
clean_words = []
for x in url_files:
    loc = url_loc + x
    with open(loc,'r') as file:
        text = file.read()
    for w in text.split():
        if any(w in stop_words):
            continue
        else :
            clean_words.append(w)
'''
###################### word cleaning ends #################################


loc = "F:\\internship\\blackcoffer\\Loughran-McDonald_MasterDictionary_1993-2021.csv"
wb = pd.read_csv(loc)#,sheet_name='Loughran-McDonald_MasterDiction')#,engine='openpyxl')
mast_dict = pd.DataFrame(wb, columns=['Word'])

folder_path = "F:\\internship\\blackcoffer\\text\\"
text = ""
pos_score = 0
neg_score = 0
polar_score = 0
subj_score = 0
avg_sntnc_len = 0
cmplxwrd_per = 0
pers_pron = 0
URL_ID = 0
for file in os.listdir(folder_path):
    pers_pron = 0
    print(1)
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_name = f"{folder_path}\{file}" 
    with open(file_name,'r', encoding="utf-8") as fi:
        print(file_name)
        text = fi.read()
        # sent_tokenize is one of instances of
        # PunktSentenceTokenizer from the nltk.tokenize.punkt module
        print(text)
        tokenized = nltk.sent_tokenize(text)
        print("tokenize starts")
        print(tokenized)
        #input()
        for i in tokenized:
            sntnc = i
            print(2)
            # Word tokenizers is used to find the words
            # and punctuation in a string
            words = nltk.word_tokenize(sntnc)
            #tokenizer = RegexpTokenizer(r'\w+')
            # removing stop words from wordList
            wordsList = [w for w in words if not w in stop_words]
            posList = [w for w in wordsList if  w in mast_dict]
            negList = [w for w in wordsList if  not w in mast_dict]
            pos_score = len(posList)
            neg_score = len(negList)
            polar_score = (pos_score - neg_score)/(pos_score + neg_score) + 0.000001
            subj_score = (pos_score + neg_score)/len(wordsList) + 0.000001
            
            avg_sntnc_len = len(wordsList)/len(tokenized)
            cmplxwrds = []
            syl_cnt = 0
            char_cnt = 0
            syl = ['a','e','i','o','u']
            for word in wordsList:
                temp = word.split()
                chr_cnt = char_cnt + len(temp)
                count = 0
                for i in temp:
                    if i in syl:
                        count = count + 1
                if count >= 2 :
                    cplxwrds.append(word)
                syl_cnt = syl_cnt + count       
            
            cmplxwrd_per =  len(cmplxwrds)/len(wordsList)
            fog_ind = 0.4*(avg_sntnc_len + cmplxwrd_per)
            avg_wrd_per_sent = len(wordsList)/len(tokenized)
            cmplxwrd_cnt = len(cmplxwrds)
            wrd_cnt = len(wordsList)
            syl_per_wrd = syl_cnt/len(wordsList)
            print(sntnc)
            #input()
            tokens = nltk.tokenize.word_tokenize(sntnc)
            tags = nltk.pos_tag(tokens)

            # result of 'tags'
            # [('The', 'DT'), ('quick', 'JJ'), ('brown', 'NN'), ('fox', 'NN'), ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN')]

            grammar = 'exact: {<PRP><PRP$>}'
            parser = nltk.RegexpParser(grammar)
            result = parser.parse(tags)
            #print(result)
            for i in result:
                if (i[1] == 'PRP' or i[1] == 'PRP$'):
                    pers_pron = pers_pron + 1
            avg_wrd_len = char_cnt/len(wordsList)
    print(df_out.URL[URL_ID])
    place = df_out.URL[URL_ID]
    out = [place, pos_score, neg_score, polar_score, subj_score,avg_sntnc_len,cmplxwrd_per,fog_ind,avg_wrd_per_sent,cmplxwrd_cnt,wrd_cnt,syl_per_wrd,pers_pron,avg_wrd_len]
    print(len(out))
    output.append(out)
    #break
    #break
    URL_ID = URL_ID + 1

    print(output)
    df = pd.DataFrame(output)
    columns=["URL","POSITIVE SCORE","NEGATIVE SCORE","POLARITY SCORE","SUBJECTIVITY SCORE","AVG SENTENCE LENGTH","PERCENTAGE OF COMPLEX WORDS","FOG INDEX","AVG NUMBER OF WORDS PER SENTENCE","COMPLEX WORD COUNT","WORD COUNT","SYLABLE PER WORD","PERSONAL PRONOUN","AVG WORD LENGTH"]
    print(len(columns))
    print(out)
    df.to_excel(out_wb, columns, sheet_name='Sheet1')
