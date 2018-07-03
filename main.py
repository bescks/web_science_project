import urllib.request
import urllib.parse
import http.cookiejar

# set cookie
cookieFile = "cookie.text"
cookie = http.cookiejar.MozillaCookieJar(cookieFile)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/62.0.3202.94 " \
             "Safari/537.36"
headers = {'User-Agent': user_agent, 'Referer': 'https://www.zhihu.com/', 'Host': 'www.zhihu.com'}
data = {'stuid': '201200131012', 'pwd': '23342321'}
postData = urllib.parse.urlencode(data)
loginUrl = 'http://www.baidu.com'

result1 = opener.open(loginUrl, postData)

cookie.save(ignore_discard=True, ignore_expires=True)

gradeUrl = ''
result2 = opener.open(gradeUrl)
print(result2.read())


# read from cookie
# #创建MozillaCookieJar实例对象
# cookie = http.cookiejar.MozillaCookieJar()
# #从文件中读取cookie内容到变量
# cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# #创建请求的request
# req = urllib.request.Request("http://www.baidu.com")
# #利用urllib2的build_opener方法创建一个opener
# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
# response = opener.open(req)
# print (response.read())


# url = 'https://www.zhihu.com/#signin'
# user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) " \
#              "AppleWebKit/537.36 (KHTML, like Gecko) " \
#              "Chrome/62.0.3202.94 " \
#              "Safari/537.36"
# values = {'account': 'gdjaccount@163.com', 'password': 'A19930614z'}
# headers = {'User-Agent': user_agent, 'Referer': 'https://www.zhihu.com/', 'Host': 'www.zhihu.com'}
#
# data = urllib.parse.urlencode(values).encode("utf-8")
#
# httpHandler = urllib.request.HTTPHandler(debuglevel=1)
# httpsHandler = urllib.request.HTTPSHandler(debuglevel=1)
# request = urllib.request.Request(url, data, headers)
# try:
#     response = urllib.request.urlopen(request)
#     page = response.read()
#     print(page)
# except urllib.request.HTTPError as e:
#     print("[ERROR]HTTPError code is " + str(e.code) + "!")
# except urllib.request.URLError as e:
#     print("[ERROR]URLError reason is " + str(e.reason) + "!")
# else:
#     print("request is Ok!")
