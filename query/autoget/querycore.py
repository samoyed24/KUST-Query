import pandas as pd
import openpyxl
from . import main, rsatest, tablegen
import requests, time
from bs4 import BeautifulSoup
from .rsatest import RSA
import pandas as pd
from . import tablegen
from io import BytesIO
from django.http import Http404, JsonResponse, HttpResponse


# def checkLogin(username, password):
#     try:
#         main.gradeQuery(username, password, check=True)
#     except:
#         return False
#     else:
#         return True

class StudentQuery:
    def __init__(self, queryType, username, password):
        self.queryType = queryType
        self.username = username
        self.password = password
    
    def do_query(self):
        try:
            resp = main.query(self.queryType, self.username, self.password)
        except Exception as e:
            print(e)
            return False
        else:
            output, filename = resp
            response = HttpResponse()
            response["Content-Type"] = "application/vnd.ms-excel"
            response['Content-Disposition'] = 'attachment;filename=%s' % filename
            response.write(output.getvalue())
            output.close()
            return response