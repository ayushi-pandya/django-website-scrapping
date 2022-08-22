from django.http import JsonResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

from django.views import View


def search_data(search):
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
    PROXY = {"http": "http//80.48.119.28:8080"}
    URL = "https://www.imdb.com/find?q=" + search + '&s=tt&ref_=fn_al_tt_mr'
    response = requests.get(URL, proxies=PROXY, headers=HEADER)
    page_html = response.text

    soup = BeautifulSoup(page_html, 'html.parser')

    movies = soup.find('table', class_='findList').find_all('td', class_='result_text')

    name_list = []
    des_list = []
    director_list = []
    writer_list = []
    year_list = []

    for movie in movies[:3]:
        name = movie.a.text
        name_list.append(name)

        data = movie.find('a', href=True)
        res = requests.get('https://www.imdb.com' + data['href'])
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        details = soup.find('section', class_='ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none '
                                              'ipc-page-section--bp-xs sc-2a827f80-1 gvCXlM').find_all('div',
                                                                                                       class_='sc-2a827f80-10 fVYbpg')

        for detail in details:
            des = detail.find('div', class_='sc-16ede01-7 hrgVKw').text
            des_list.append(des)

            director = detail.find('ul',
                                   class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt').text
            director_list.append(director)

            writer = detail.find_next('ul',
                                      class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt').find_next(
                'ul',
                class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt').text
            writer_list.append(writer)

        info = soup.find('section', class_='ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none '
                                           'ipc-page-section--bp-xs sc-2a827f80-1 gvCXlM').find_all('div',
                                                                                                    class_='sc-80d4314-2 iJtmbR')

        for i in info:
            year = i.text
            year_list.append(year)

    details_dict = {'Name': name_list,
                    'Description': des_list,
                    'Director': director_list,
                    'Writer': writer_list,
                    'Year': year_list}

    return details_dict


class DemoFunction(View):
    def get(self, request):
        return render(request, 'demo/demo.html')

    def post(self, request):
        search = request.POST['search']
        search = search.strip()
        if search != '':
            names = search_data(search)
            data = {}
            for i in range(len(names['Name'])):
                data[names['Name'][i]] = names['Description'][i], names['Director'][i], names['Writer'][i], \
                                         names['Year'][
                                             i]
            return JsonResponse(list(data), safe=False)
            # return render(request, 'demo/home.html', {'data': data})
        else:
            return render(request, 'demo/home.html')
