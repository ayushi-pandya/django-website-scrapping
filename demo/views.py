from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

from django.views import View


def search_data(search):
    names = []
    information = []
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
    PROXY = {"http": "http//80.48.119.28:8080"}
    URL = "https://www.imdb.com/find?q=" + search + '&s=tt&ref_=fn_al_tt_mr'
    response = requests.get(URL, proxies=PROXY, headers=HEADER)
    page_html = response.text

    soup = BeautifulSoup(page_html, 'html.parser')

    movies = soup.find('table', class_='findList').find_all('td', class_='result_text')
    for movie in movies[:5]:
        name = movie.a.text
        names.append(name)

        data = movie.find('a', href=True)
        res = requests.get('https://www.imdb.com' + data['href'])
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        details = soup.find('section', class_='ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none '
                                              'ipc-page-section--bp-xs sc-2a827f80-1 gvCXlM').find_all('div',
                                                                                                       class_='sc-2a827f80-10 fVYbpg')
        # print(details)
        for detail in details:
            des = detail.find('div', class_='sc-16ede01-7 hrgVKw').text
            director = detail.find('ul',
                                   class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt').text
            writer = detail.find_next('ul',
                                      class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt').find_next(
                'ul',
                class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt').text
            year = detail.find('li', class_='ipc-inline-list__item').text
            print('director:', director)
            print('writer:', writer)
            print('star:', year)
    # 'ipc-inline-list__item'
    # 'ipc-inline-list__item'
    # print('name:',name['href'])
    # print('name:',name.split()[1])

    # info = movie.text
    # # print('name:', info[1])
    #
    # information.append(info)

    details_dict = {'MovieName': names,
                    'MovieInfo': information}

    return details_dict


class DemoFunction(View):
    def get(self, request):
        return render(request, 'demo/demo.html')

    def post(self, request):
        search = request.POST['search']
        search = search.strip()
        if search != '':
            names = search_data(search)
            a = {}
            for i in range(len(names['MovieName'])):
                a[names['MovieName'][i]] = names['MovieInfo'][i]
            return render(request, 'demo/demo.html', {'data': a})

        else:
            return render(request, 'demo/demo.html')
