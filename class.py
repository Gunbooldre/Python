import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool


#Главная функция
def main():
    url = 'http://banknotes.finance.ua/'
    links = []
    #Получить ссылки
    all_links = get_all_links(get_html(url), links)
    with Pool(2) as p:
        p.map(make_all,all_links)
    
#Получение URL
def get_html(url):
    r = requests.get(url)
    return r.text

#сама функция для многопоточности
def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)

#Получение url страниц
def get_all_links(html, links):
    f = open('file.csv','w')
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.find_all('div',class_='wm_countries')
    for i in href:
        for link in i.find_all('a'):
            links +=[link['href']]
        return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    try: 
        name = soup.find('div','pagehdr').find('h1').text
    except:
        name = 'ne nashel'
    try: 
        price = [pn.find('b').text for pn in soup.find('div', class_='wm_exchange').find_all('a',class_ = 'button',target = False)]+[pr.text for pr in soup.find('div',class_ ='wm_exchange').find_all('td',class_ = 'amount')]
        if len(price) == 6:
            price = price+price[0]+price[3]+price[1]+price[4]+price[2]+price[5]
        elif len(price) == 4:
            price = price[0]+price[2]+price[1]+price[3]
    except:
        price = 'ne vizhu'
    data = {'name':name, 'price':price}
    return data

def write_csv(data):
    with open('file.csv', 'a') as f:
        writer = csv.writer(f) 
        writer.writerow((data['name'] ,data['price']))



#Запуск фуннции 
if __name__ == '__main__':
    main()