import io
import random
import string 
import warnings
import numpy as np
from datetime import date
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) 





with open('iplcb.txt','r', encoding='utf8', errors ='ignore') as fin:
 raw = fin.read().lower()


sent_tokens = nltk.sent_tokenize(raw) 
word_tokens = nltk.word_tokenize(raw)


lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))



POSITIVE = ("Cool","Awesome",":)",":))","Hope you like this interaction",
            "I'm very much interested in talking to you","Hi-fi")
NEGATIVE =(";(",":(","Do you feel bored?",
           "Are you not interested??","Cheer up!!!")
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up",
                   "hey","Good morning","Good evening","namaste","vanakkam")
GREETING_RESPONSES = ["hi", "hey", "nods", "hi there", "hello", "I am glad! You are talking to me"]

FAVOURITES = ("which team is your favourite?","favourite team","what team do you like","favourite team?","what team do you like?",
              "your favourite?","your favourite")
FAVOURITES_RESPONSES = ("CSK","RCB","MI","RR","SRH","DC","KKR","kXIP")

TEAMS = ["i support csk","i support rcb",
         "i support mi","i support rr","i support srh","i support dc","i support kkr","i support kxip"]
TEAMS_RESPONSES =["Start the whistles!!","Play bold!!","Chalo paltans!!","Halla bol!!","Orange army","Naya Dilli!!!","Purple Army","Red army"]

APOLOGIES =["Pardon!!??","Sorry! I'm not able to get it","Tell me more precise","What do you mean?"]

ABOUT =["Who are you??"]
ABOUT_RESP =["I'm a cricket fan","I'm an Indian"]
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    if(sentence=="how's going?" or sentence=="how are you?" or sentence=="how are you" or sentence=="whatsup"):
      return "I'm fine"
    if(sentence=="who are you?" or sentence=="who are you"):
      return random.choice(ABOUT_RESP)
    if sentence in FAVOURITES:
      return random.choice(FAVOURITES_RESPONSES)      
    for word in sentence.split():
        analysis=TextBlob(word)
        if analysis.sentiment.polarity > 0:
            return random.choice(POSITIVE)
        elif analysis.sentiment.polarity < 0:
            return random.choice(NEGATIVE)
        else:
          if word.lower() in GREETING_INPUTS:
              return random.choice(GREETING_RESPONSES)
          elif word.lower() in TEAMS:
                for i in range(0,7):
                    if TEAMS[i].lower() == word.lower():
                        return TEAMS_RESPONSES[i]
                    else: continue        
          elif word.lower() in ABOUT:
              return random.choice(ABOUT_RESP)


def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+random.choice(APOLOGIES)
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("ROBO: Hola! I'm Crickbot. I will answer your queries about IPL. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
      #if("date" in user_response):
        #print("ROBO: "+date.today())
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("ROBO: You are welcome..")
        elif(user_response.lower() in TEAMS):
          for i in range(0,len(TEAMS)):
            if user_response==TEAMS[i]:
              print("ROBO: "+TEAMS_RESPONSES[i])    
        else:
            if(greeting(user_response)!=None):
                print("ROBO: "+greeting(user_response))
            else:
                print("ROBO: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("ROBO: Bye! Enjoy the matches..")
