# -*- codeing:utf-8 -*-
import urllib2
import subprocess
import re
from bs4 import BeautifulSoup

movies = {}
movie_type = 15

url = 'http://www.xiamp4.com/search.asp?t={type}'.format(type=movie_type)
r = urllib2.urlopen(url).read()
soup = BeautifulSoup(r, "html.parser")
page_count = re.findall(r'<span>.+/(\d+).+</span>', str(soup.select('#pages')[0].select('span')[0]))[0]
print 'you search movies has:{0}'.format(page_count)
for page in range(1, int(page_count) + 1):
    url = 'http://www.xiamp4.com/search.asp?page={page}&searchword=&searchtype=-1&t={type}'.format(page=page,
                                                                                                   type=movie_type)
    r = urllib2.urlopen(url).read()
    soup = BeautifulSoup(r, "html.parser")
    for info in soup.select('.info'):
        detailed_info = []
        for ii in info.select("i"):
            detailed_info.append(re.match(r"<i>(?P<test>.+)</i>", str(ii)).groupdict()['test'])
        data_info = '\n'.join(detailed_info)
        info_html = info.select('h2')[0]
        com = re.compile(
            r'<h2><a href="(?P<url>.+)" target="_blank" title="(?P<movie_name>.+)">.+</a><em> (?P<time>\d+)</em></h2>')
        m = com.match(str(info_html))
        if m:
            movie_name = m.groupdict()['movie_name']
            movie_time = m.groupdict()['time']
            film_data = urllib2.urlopen('http://www.xiamp4.com{}'.format(m.groupdict()['url'])).read()
            film_soup = BeautifulSoup(film_data, "html.parser")
            for i in film_soup.select('.ndownlist'):
                rc = re.compile(r'.+<script>var GvodUrls = "(?P<url>.+)";</script>')
                m = rc.match(str(i))
                if m:
                    url = m.groupdict()['url']
                    url = url
                    
                    # print "{0}, {1}\n{2}\n{3}\n\n".format(movie_name, movie_time, data_info, url)
                    if movie_name not in movies:
                        movies[movie_name] = url
                        with open('c:/Movielinks.txt', 'a+') as f:
                            f.write("{0}, {1}\n{2}\n{3}\n\n".format(movie_name, movie_time, data_info, url))
                        # subprocess.Popen(
                        #     r"D:\Guest_temp\Program\Thunder.exe {}".format(url.decode('utf-8').encode('gbk')))
#
# print movies
