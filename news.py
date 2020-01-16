import requests


url = ('https://newsapi.org/v2/top-headlines?'
       'country=br&'
       'source=bbc-news&'
       'apiKey=05d5ce74721c41698d58009213297db9')


req = requests.get(url, timeout=3000)
json = req.json()

for c in json:
      if str(c).find('novela') == 0:
             print('Noticia de novela achada!\n')
    #print(json['articles'][c]['title'])
    #print(json['articles'][c]['description'])