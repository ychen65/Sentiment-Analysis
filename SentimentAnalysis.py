# Yongqiang Chen 
import json
import os
import nltk
import csv
import operator
from nltk.corpus import words
from nltk.corpus import stopwords


try:
    # Checks if someone has the reviews file that contains the json file
    if os.path.exists("reviews"):
        os.chdir("reviews")

    # Reads the json file
    with open("yelp_academic_dataset_review_small.json") as yelp_reviews_json:
        yelp_reviews = json.load(yelp_reviews_json)

    dic={}
    review_words = []
    lem_words_list = []
    words3=[]

    #stopwords and common words
    stop_words = stopwords.words("english")
    common_words = words.words("en")
    lem = nltk.WordNetLemmatizer()

    print("Tokenizing and lemmatizing reviews...")
    for i in range(len(yelp_reviews)):

        # Nltk tokenize
        #for review in review_text:
        review_words = set(nltk.word_tokenize(yelp_reviews[i]["text"].lower()))

        #remove words in stopwords
        words1=set([word for word in review_words if word not in set(stop_words) and word.isalpha()])

        # Lemmatize
        lem_words_list.append(lem.lemmatize(word) for word in words1)

        # remove words in words corpus
        words2=[set(lem_words_list[i]) & set(common_words)]

        words3.extend(words2)

        #each word to its star rate
        for k in list(words3[i]):
            if k not in dic:
                dic[k]=[yelp_reviews[i]['stars']]
            else:
                dic[k].append(yelp_reviews[i]['stars'])

    #discard lemma fewer than 10 times
    new_dic={k:v for k,v in dic.items() if len(v)>10}

    # calcul the average star rating
    for k,v in new_dic.items():
        new_dic[k]=sum(v)/len(v)

    #sort
    text=sorted(new_dic.items(),key=operator.itemgetter(1), reverse=False)

    print("Creating csv file...")

    #write in a csv file
    with open("sentimentlevel.csv", "w") as outfile:
        writer=csv.writer(outfile, delimiter=",")
        writer.writerow(["Lemma","Sentiment level"])

        # save 500 most negative and 500 most postive
        for row in text[-1:-500:-1]:
            writer.writerow(row)
        for row in text[500::-1]:
            writer.writerow(row)
            
    print("Done.")
except FileNotFoundError:
    print("\"yelp_academic_dataset_review_small.json\" does not exist.")
