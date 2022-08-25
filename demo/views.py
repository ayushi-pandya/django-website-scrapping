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

    alldata = soup.find('table', class_='findList')

    if alldata is not None:
        data = alldata.find_all('tr')

        detail_dict = []

        for movie in data[:3]:
            name = movie.find('td', class_='result_text').a.text

            image = movie.find('td', class_='primary_photo').img.attrs['src']

            data = movie.find('a', href=True)
            res = requests.get('https://www.imdb.com' + data['href'])
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')

            details = soup.find('section',
                                class_='ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none '
                                       'ipc-page-section--bp-xs sc-2a827f80-1 gvCXlM').find_all('div',
                                                                                                class_='sc-2a827f80-10 fVYbpg')

            for detail in details:
                a = {}
                des = detail.find('div', class_='sc-16ede01-7 hrgVKw').text

                try:
                    directors = detail.find('ul',
                                            class_='ipc-inline-list ipc-inline-list--show-dividers '
                                                   'ipc-inline-list--inline '
                                                   'ipc-metadata-list-item__list-content baseAlt')

                    director_list = [
                        i.find('a').text
                        for i in directors.find_all('li', class_='ipc-inline-list__item')
                    ]
                except:
                    director_list = '--'

                try:
                    writers = detail.find_next('ul',
                                               class_='ipc-inline-list ipc-inline-list--show-dividers '
                                                      'ipc-inline-list--inline ipc-metadata-list-item__list-content '
                                                      'baseAlt').find_next(
                        'ul',
                        class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline '
                               'ipc-metadata-list-item__list-content baseAlt')

                    writers_list = [
                        i.find('a').text
                        for i in writers.find_all('li', class_='ipc-inline-list__item')
                    ]
                except:
                    writers_list = '--'

                try:
                    stars = detail.find_next('ul',
                                             class_='ipc-inline-list ipc-inline-list--show-dividers '
                                                    'ipc-inline-list--inline ipc-metadata-list-item__list-content '
                                                    'baseAlt').find_next(
                        'ul',
                        class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline '
                               'ipc-metadata-list-item__list-content baseAlt').find_next('ul',
                                                                                         class_='ipc-inline-list '
                                                                                                'ipc-inline-list--show'
                                                                                                '-dividers '
                                                                                                'ipc-inline-list'
                                                                                                '--inline '
                                                                                                'ipc-metadata-list'
                                                                                                '-item__list-content '
                                                                                                'baseAlt')

                    stars_list = [
                        i.find('a').text
                        for i in stars.find_all('li', class_='ipc-inline-list__item')
                    ]
                except:
                    stars_list = '--'

                try:
                    movie_type = detail.find('div', class_='ipc-chip-list__scroller').text
                except:
                    movie_type = '--'

                try:
                    ratings = detail.find('div', class_='sc-7ab21ed2-0 fAePGh')
                    rate = ratings.span.text
                except:
                    rate = '--'

                a['Name'] = name
                a['Description'] = des
                a['Director'] = director_list
                a['Writer'] = writers_list
                a['Stars'] = stars_list
                a['Image'] = image
                a['Movie Type'] = movie_type
                a['Ratings'] = rate
                detail_dict.append(a)
        print('detail_dict:', detail_dict)
        return detail_dict


class DemoFunction(View):
    def get(self, request):
        return render(request, 'demo/demo.html')

    def post(self, request):
        search = request.POST['search']
        search = search.strip()
        if search != '':
            data = search_data(search)
            if data is not None:
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse('No data found')

        else:
            return render(request, 'demo/demo.html')
