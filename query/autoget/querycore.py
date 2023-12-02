import requests, openpyxl, json
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib.staticfiles import finders
from query.generaltools import errorMsg
from bs4 import BeautifulSoup
from .rsatest import RSA
from io import BytesIO
import pandas as pd

def lsget(ls, idx, dft=''):
    if(idx+1>len(ls)):
        return dft
    return removefh(ls[idx])

def removefh(s):
    if s[-1] == ';':
        return s[:-1]
    else:
        return s

def letterplus(s):
    return chr(ord(s)+1)

class StudentQuery:
    def __init__(self, queryType, username, password, getMode):
        self.queryType = queryType
        self.username = username
        self.password = password
        self.getMode = getMode
    
    def do_query(self):
        try:
            self.checkLogin()
        except AssertionError:
            self.result = errorMsg('认证失败, 用户名或密码错误!')
            return
        self.query_interface()
        return self.result
    
    def checkLogin(self):
        s = requests.Session()
        r = s.get('https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fjwctsp.kmust.edu.cn%2Fintegration%2Fkcas-sso%2Flogin')
        r.encoding = 'utf8'
        soup1 = BeautifulSoup(r.text, 'html.parser')
        lt = soup1.find('input', {"name":"lt"}).attrs['value']
        execution = soup1.find('input', {"name":"execution"}).attrs['value']
        _eventId = soup1.find('input', {"name":"_eventId"}).attrs['value']
        data = {
            'username':self.username,
            'password':RSA(self.password),
            'captcha':'',
            'warn':True,
            'lt':lt,
            'execution':execution,
            '_eventId':_eventId
        }
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        s.post('https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fjwctsp.kmust.edu.cn%2Fintegration%2Fkcas-sso%2Flogin', data=data, headers=headers)
        s.get('https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fjwctsp.kmust.edu.cn%2Fintegration%2Fkcas-sso%2Flogin', headers=headers)
        r = s.get('http://i.kust.edu.cn/')
        loginsoup = BeautifulSoup(r.text, 'html.parser')
        assert loginsoup.find('title').text == "昆明理工大学师生信息服务平台"
        self.session = s

    def query_interface(self):
        if self.queryType == 'grade':
            self.grade()
        elif self.queryType == 'table':
            self.table()
        # elif self.queryType == 'card':
        #     self.card()
        elif self.queryType == 'exams':
            self.exams()

    def grade(self):
        s = self.session
        r = s.get('http://jwctsp.kmust.edu.cn/integration/for-std/best/grade/sheet')
        r.encoding = 'utf-8'
        soup2 = BeautifulSoup(r.text, 'html.parser')
        studentid = soup2.find('form',{'target':'student-grades'}).attrs['action'].split('/')[-1]
        r = s.get(f'http://jwctsp.kmust.edu.cn/integration/for-std/best/grade/sheet/info/{studentid}?semester=')
        soup3 = BeautifulSoup(r.text, 'html.parser')

        datadict = {
            '学期':[],
            '课程名称':[],
            '课程代码':[],
            '课程类别1':[],
            '课程类别2':[],
            '教学班代码':[],
            '成绩':[],
            '学分':[],
            '绩点':[],
            '学分绩点':[],
            '修读性质':[],
            '备注':[]
        }

        gradeinfo = soup3.find_all('div',{'class':'row'})
        for gradeblock in gradeinfo:
            sem = gradeblock.find_all('div', {'class':'col-sm-12'})
            semname = sem[0].h3.text
            gradetb = sem[1]
            grades = gradetb.table.tbody.select('tr')
            for grade in grades:
                data = grade.select('td')
                datadict['学期'].append(semname)
                datadict['课程名称'].append(data[0].text.strip())
                datadict['课程代码'].append(data[1].text)
                datadict['课程类别1'].append(data[2].text)
                datadict['课程类别2'].append(data[3].text)
                datadict['教学班代码'].append(data[4].text)
                datadict['成绩'].append(data[5].text)
                datadict['学分'].append(data[6].text)
                datadict['绩点'].append(data[7].text)
                datadict['学分绩点'].append(data[8].text)
                datadict['修读性质'].append(data[9].text)
                datadict['备注'].append(data[10].text)
            df = pd.DataFrame(data=datadict)
        if self.getMode == '1':
            data = {
                'errorStatus':False,
                'type':0,
                'table_head':list(datadict.keys()),
                'table_body':[list(df.iloc[i]) for i in range(len(datadict['学期']))],
            }
            self.result = JsonResponse(data=data)
        elif self.getMode == '2':
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            self.result = FileResponse(output)

    def table(self):
        r = self.session.get('http://jwctsp.kmust.edu.cn/integration/for-std/course-table/get-data?bizTypeId=2&semesterId=282')
        tabledata = r.json()
        wkdaydict = {
            '周一' : 'B',
            '周二' : 'D',
            '周三' : 'F',
            '周四' : 'H',
            '周五' : 'J',
            '周六' : 'L',
            '周日' : 'N'
        }
        lsdict = {
            '第一节' : '3',
            '第三节' : '5',
            '第六节' : '8',
            '第九节' : '11',
            '第十一节' : '13',
        }

        dfdatadict = {
            '课程代号':[],
            '课程名称':[],
            '周数':[],
            '星期':[],
            '起节':[],
            '终节':[],
            '校区':[],
            '地点':[],
        }
        templatepath = finders.find('index/table_template.xlsx')
        wb=openpyxl.load_workbook(templatepath)
        table=wb['Sheet1']
        lessons = tabledata['lessons']
        for lesson in lessons:
            code = lesson['code']
            name = lesson['course']['nameZh']
            Linfo = lesson['scheduleText']['dateTimePlaceText']['text']
            if(type(Linfo) == str):
                difblock = [s.strip().split(' ') for s in Linfo.split('\n')]
                for block in difblock:
                    dfdatadict['课程名称'].append(name)
                    dfdatadict['课程代号'].append(code)
                    dfdatadict['周数'].append(lsget(block, 0))
                    dfdatadict['星期'].append(lsget(block, 1))
                    ft = lsget(block, 2)
                    if(ft):
                        ftlist = ft.split('~')
                        dfdatadict['起节'].append(ftlist[0])
                        dfdatadict['终节'].append(ftlist[1])
                    else:
                        dfdatadict['起节'].append('')
                        dfdatadict['终节'].append('')
                    dfdatadict['校区'].append(lsget(block, 3))
                    dfdatadict['地点'].append(lsget(block, 4))

        df = pd.DataFrame(data=dfdatadict)

        for s in df.itertuples():
            wkday = wkdaydict[s[4]]
            start = lsdict[s[5]]
            info = f'{s[1]}\n{s[2]}\n{s[3]}\n{s[5]}~{s[6]}\n{s[7]} {s[8]}'
            loc = f'{wkday}{start}'
            if table[loc].value:
                table[loc].value = '\n'+info
            else:
                table[loc].value = info
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        self.result = FileResponse(output)
    
    # def card(self):
    #     self.session.get('http://yktcas.kmust.edu.cn/ias/prelogin?sysid=FWDT&continueurl=http%3a%2f%2fykt.kmust.edu.cn%2fcassyno%2findex')
    #     data = {
    #         'errorcode':1,
    #         'continueurl':'http://ykt.kmust.edu.cn/cassyno/index',
    #         'ssoticketid':self.username
    #     }
    #     self.session.post('http://ykt.kmust.edu.cn/cassyno/index', data=data)
    #     r = self.session.post('http://ykt.kmust.edu.cn/User/GetCardInfoByAccountNoParm', data={'json':True})
    #     cardinfo = json.loads(r.json()['Msg'])['query_card']['card'][0]
    #     print(data)
    #     data = {
    #         'errorStatus':False,
    #         'type':0,
    #         'table_head':['卡号', '持卡者姓名','学号/工号', '卡片类型', '开卡日期', '到期日期', '冻结状态', '挂失状态', '卡内余额'],
    #         'table_body':[[cardinfo['account'], cardinfo['name'], cardinfo['sno'], cardinfo['cardname'], cardinfo['createdate'], cardinfo['expdate'], cardinfo['freezeflag'], cardinfo['lostflag'], int(cardinfo['cardbalance']) / 100]]
    #     }
    #     self.result = JsonResponse(data)
    
    def exams(self):
        r = self.session.get('http://jwctsp.kmust.edu.cn/integration/for-std/exam-arrange/')
        examsoup = BeautifulSoup(r.text, 'html.parser')
        table = examsoup.find('table', {'id':'exams'})
        trs = table.tbody.select('tr')
        datadict = {
            '课程名称':[],
            '日期时间':[],
            '考场':[],
            '楼宇':[],
            '校区':[],
        }

        for tr in trs:
            td = tr.select('td')
            datadict['课程名称'].append(td[0].text.strip())
            datadict['日期时间'].append(td[1].text)
            datadict['考场'].append(td[2].text)
            datadict['楼宇'].append(td[4].text)
            datadict['校区'].append(td[5].text)
        df = pd.DataFrame(data=datadict)
        if(self.getMode == '1'):
            data = {
                'errorStatus':False,
                'type':0,
                'table_head':list(datadict.keys()),
                'table_body':[list(df.iloc[i]) for i in range(len(datadict['课程名称']))],
            }
            self.result = JsonResponse(data=data)
        elif(self.getMode == '2'):
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            self.result = FileResponse(output)