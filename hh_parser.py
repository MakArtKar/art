import requests
from bs4 import BeautifulSoup as bs
import csv

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

base_url = 'https://samara.hh.ru/search/vacancy?text=python&area=1'


def hh_parse(base_url, headers):
    jobs = []
    urls = [base_url + '&page=0']
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa':'pager-page'})
            count = int(pagination[-1].text)
        except:
            pass
        for i in range(1, count):
            url = base_url + f'&page={i}'
            urls.append(url)

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            for div in divs:
                try:
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-employer'}).text
                    text1 = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy_snippet_responsibility'}).text
                    text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    content = text1 + ' ' + text2
                    jobs.append({
                        'title':title,
                        'href': href,
                        'company': company,
                        'content': content
                    })
                except:
                    pass
            print(len(jobs))
    else:
        print('ERROR')
    return jobs

def file_writer(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))

jobs = hh_parse(base_url, headers)
file_writer(jobs)