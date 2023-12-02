import requests
from django.http import JsonResponse

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    location = getLocation(ip)
    return (ip, location)

def getLocation(IP):
    try:
        r=requests.get(f'http://whois.pconline.com.cn/ipJson.jsp?ip={IP}&json=true', timeout=(1, 1))
        return r.json()['addr']
    except:
        return ''

def errorMsg(errorMsg):
    data = {
        'errorStatus':True,
        'errorMsg':errorMsg
    }
    return JsonResponse(data)