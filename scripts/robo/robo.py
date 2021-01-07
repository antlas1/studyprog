# Обработка ответа
def response1(word):
	return "Одно непонятное слово"
	
def response2(word1,word2):
	return "Два непонятных слова"
	
def response3(word1,word2,word3):
	return "Три непонеятных слова"

#Основная программа. Не менять!
flag=True
print("РОБО: Меня зовут РОБО. Я буду вашим личным ассистентом. Разве не здорово? Если хотите выйти, то напишите \"пока\"\n>", end='')
while(flag==True):
	user_response = input()
	user_response=user_response.lower().strip()
	if(user_response != 'пока'):
		words_resp = user_response.split(' ')
		if len(words_resp)>3:
			print("РОБО: очень много слов, я понимаю от одного до трёх. Попробуйте еще раз.\n>", end='')
		elif len(words_resp)==0 or (len(words_resp)==1 and len(words_resp[0])==0):
			print("РОБО: ну, помолчим.\n>", end='')
		else:
			resp = "Неизвестно"
			if len(words_resp)==1:
				resp = response1(words_resp[0])
			elif len(words_resp)==2:
				resp = response2(words_resp[0],words_resp[1])
			else:
				resp = response3(words_resp[0],words_resp[1],words_resp[2])
			print("РОБО: "+resp+"\n>", end='')
	else:
		flag=False
		print("РОБО: Пока! Берегите себя.") 