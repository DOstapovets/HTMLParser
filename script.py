import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import datetime
import csv

url = "http://oktv.ua/search"
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

output_file = open("out.csv", "wb")
wr = csv.writer(output_file)

page = 0
date_start = datetime.date(2017, 02, 07)
date_finish = (date_start + datetime.timedelta(days=1))
while True:
    values = {'order_start': date_start.strftime("%d.%m.%Y"),
              'order_finish': date_finish.strftime("%d.%m.%Y"),
              'start': page}
    data = urllib.urlencode(values)
    req = urllib2.Request(url=url, data=data, headers=headers)
    response = urllib2.urlopen(req)

    html = response.read()
    soup = BeautifulSoup(html)
    apart_list = soup.find('div', {'class': 'ajax-pagination-content'}).findAll('div', {'class': 'object_v_spiske'})
    if not len(apart_list):
        break
    for item in apart_list:
        apart = []
        apart.append(url+item.find('a').get('href'));
        apart.append(url+item.find('img').get('src'))
        apart.append(''.join(item.find('div', {'class': 'object_price'}).findAll(text=True)).strip())
        apart.append(''.join(item.find('div', {'class': 'object_title'}).findAll(text=True)).strip())
        ul = item.find('ul').findAll('li')
        for li in ul:
            apart.append(''.join(li.findAll(text=True)).strip())
        wr.writerow([unicode(s).encode("utf-8") for s in apart])
    page += 12
output_file.close()
