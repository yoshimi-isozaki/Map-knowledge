import re
match = re.search(r'@*/', 'https://www.google.co.jp/maps/place/%E9%A6%99%E6%A4%8E%E9%A7%85%E6%9D%B1%E5%85%AC%E5%9C%92/@33.6565064,130.4430107,15z/data=!4m8!1m2!2m1!1z56aP5bKh5biCIOmmmeakjuOAgOWFrOWckg!3m4!1s0x35418f3c67d64d13:0x8fb637a525115409!8m2!3d33.6582798!4d130.4445994')
url = 'https://www.google.co.jp/maps/place/%E9%A6%99%E6%A4%8E%E9%A7%85%E6%9D%B1%E5%85%AC%E5%9C%92/@33.6565064,130.4430107,15z/data=!4m8!1m2!2m1!1z56aP5bKh5biCIOmmmeakjuOAgOWFrOWckg!3m4!1s0x35418f3c67d64d13:0x8fb637a525115409!8m2!3d33.6582798!4d130.4445994'
print('password:', match.group())
print(url.find('@')) # 91
print(url.find('z/')) # 117
print(url[91+1:117-3])