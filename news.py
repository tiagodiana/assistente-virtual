import requests


url = ('https://newsapi.org/v2/top-headlines?'
       'country=br&'
       'source=bbc-news&'
       'apiKey=05d5ce74721c41698d58009213297db9')


req = requests.get(url, timeout=3000)
json = req.json()

filter_list = ['Meutimao.com.br', 'Colunadofla.com', 'Ofuxico.com.br', 'Sportingnews.com', 'Fogaonet.com','Cbf.com.br', 'Superesportes.com.br']

cont_news = []

for c in range(int(json['totalResults'])):
    try:
        cont_news.append(json['articles'][c]['source']['name'])
    except:
        break

c = 0;
while True:
    try:
        if cont_news[c] not in filter_list:
            print(json['articles'][c]['source'])
        else:
            print("não achado")
        c +=1
    except:
        break