#Meet Robo: your friend
#+идеи: https://progkids.com/blog/five-python-projects
# Обработка ответа
def response(user_response):
    #robo_response=''
    #sent_tokens.append(user_response)
    #TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    #tfidf = TfidfVec.fit_transform(sent_tokens)
    #vals = cosine_similarity(tfidf[-1], tfidf)
    #idx=vals.argsort()[0][-2]
    #flat = vals.flatten()
    #flat.sort()
    #req_tfidf = flat[-2]
    #if(req_tfidf==0):
    #    robo_response=robo_response+"I am sorry! I don't understand you"
    #    return robo_response
    #else:
    #    robo_response = robo_response+sent_tokens[idx]
    #    return robo_response
    return "Пока нет ответа"


flag=True
print("РОБО: Меня зовут РОБО. Я буду вашим личным ассистентом. Разве не здорово? Если хотите выйти, то напишите \"пока\"")
while(flag==True):
    user_response = input()
    user_response=user_response.lower().strip()
    if(user_response != 'пока'):
        resp = response(user_response)
        print("РОБО: "+response(user_response))
    else:
        flag=False
        print("РОБО: Пока! Берегите себя.") 