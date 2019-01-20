import nltk
import numpy as np
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pyttsx3
import speech_recognition as sr
import wikipedia
from textblob import TextBlob

r = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('rate',100)#100 words per minute
engine.setProperty('volume',0.9) 
a = (engine.getProperty('voices'))
engine.setProperty('voice', a[2].id)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey",  "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
			
def response(user_response):
    Friday_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        Friday_response=Friday_response+"I am sorry! I don't understand you"
        return Friday_response
    else:
        Friday_response = Friday_response+sent_tokens[idx]
        return Friday_response
flag=True

while(flag==True):
    user_response = input()
    
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("Friday: You are welcome..")
            print('')
            engine.say("You are welocome")
            engine.runAndWait()

        else:
            if(greeting(user_response)!=None):
                a = greeting(user_response)
                print("Friday: "+ a)
                print('')
                engine.say(a)
                engine.runAndWait()
          
            else:
          
                punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                no_punct = ""
                try:
                    for char in user_response:
                        if char not in punctuations:
                            no_punct = no_punct + char

                    user_response = no_punct
                    user_response = ' '.join([word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(user_response)) if pos[0] == 'N'])
                    m = wikipedia.summary(user_response)
                    x = m.encode('ascii', 'ignore')
                    f= open("text.txt","w+")
                    f.write(repr(x))
                    f.close()
                    f=open('text.txt','r',errors = 'ignore')
                    raw=f.read()
                    raw=raw.lower()# converts to lowercase
                    sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
                    word_tokens = nltk.word_tokenize(raw)# converts to list of words

                    final_words=list(set(word_tokens))
                    print("Friday: ",end="")
                    b = response(user_response)
                    print(b)
                    print('')
                    engine.say(b)
                    engine.runAndWait()
                    sent_tokens.remove(user_response)
                except Exception:
                    print('Say it again please...')
                    print('')
				
    else:
        flag=False
        print("Friday: Bye! take care..")
        print('')
        engine.say('Bye take care')
        engine.runAndWait()
		
