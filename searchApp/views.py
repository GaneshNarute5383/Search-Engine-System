# from django.db.models.fields import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.views.generic import View
from pandas.io import json

from .utils import render_to_pdf
import itertools
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import WebContent, Contact, Feedback, SitemapInfo,SignUp
from django.core.paginator import Paginator
from time import time
from .models import Keywords


# Create your views here.





def studyhome(request):
    return render(request, "studyhome.html")


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def privacy(request):
    return render(request, "privacy.html")


def policy(request):
    return render(request, "policy.html")


def console(request):
    return render(request, "console.html")


def feedback(request):
    return render(request, "feedback.html")


def contact(request):
    return render(request, "contact.html")


def getFeedback(request):
    a = Feedback(fullname=request.GET["fullname"],
                 email=request.GET["email"],
                 feedback=request.GET["message"])
    a.save()
    return render(request, "feedbacksuccess.html")


def getContact(request):
    a = Contact(fullname=request.GET['fullname'],
                email=request.GET['email'],
                subject=request.GET['subject'],
                message=request.GET['message'])
    a.save()
    return render(request, "contactsuccess.html")


def getSitemap(request):
    a = SitemapInfo(url=request.GET["url"],
                    sitemap=request.GET["sitemap"])
    a.save()
    return render(request, "sitemapsuccess.html")

def getsignup(request):
    obj = SignUp(fname=request.GET["fname"],
    mname=request.GET["mname"],
    lname=request.GET["lname"],
    email=request.GET["email"],
    mobile_number = request.GET["mobile"],
    password = request.GET["pwd"],
    conformed_password = request.GET["conpass"])
    obj.save()
    return render(request,"login.html")

def check_login(request):
    email = request.GET['fname']
    password = request.GET['pass']
    obj = SignUp.objects.filter(email = email)
    if obj :
        for i in obj :
            fetch_password = i.password
            if fetch_password == password:
                request.session['username'] = email
                return render(request, "console.html")
            else:
                 return render(request, "login.html" ,{"message":"Please enter correct username or password"})
    return render(request, "login.html" ,{"message":"Please enter correct username or password"})


def check_console(request):

    if  request.session.has_key('username') :
        return render(request, "console.html")
    else :
        return render(request, "login.html")

def log_out(request):
  try:
      del request.session['username']
  except:
      pass
  return render(request,'login.html')


def result(request):
    return render(request, "result.html")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def searchContent(request):
    start = time()
    find = request.GET.get('userinput')

    data = request.GET.get('data')
    if find:
        query = find
        request.session["q"] = find
        stopwords = """a about above actually after again against all almost also although always am an and any are as at be became become because been before being below between both but by can could did do does doing down during each either else few for from further had has have having he he'd he'll hence he's her here here's hers herself him himself his how how's I I'd I'll I'm I've if in into is it it's its itself just let's may maybe me might mine many more  must my myself of oh on once only ok or other ought our ours ourselves out over own she she'd she'll she's should so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was we we'd we'll we're we've were what what's what’s when whenever when's where whereas wherever where's whether which while who whoever who's whose whom why way ways why's will with within would yes yet you you'd you'll you're you've your yours yourself yourselves - _ . < > : ; " ' """
        stopwordslist = stopwords.split(" ")
        querylist = find.split(" ")
        find = ""
        for queryword in querylist:
            flag = 0
            for stopword in stopwordslist:
                if queryword == stopword:
                    flag = 1
                    break
            if flag == 1:
                pass
            elif flag == 0:
                find = find +" "+queryword
        find = find.strip()
        print("find ",find)
        dataset = WebContent.objects.filter(webpage_keywords__icontains=find)
        paginator = Paginator(dataset, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        end = time()
        total_time = round(end - start, 3)
        return render(request, "result.html",
                      {"page_obj": page_obj, "paginator": paginator, "total_time": total_time, "query": query,
                       "data": find})
    else:
        find = request.session['q']

        query = find
        stopwords = """a about above actually after again against all almost also although always am an and any are as at be became become because been before being below between both but by can could did do does doing down during each either else few for from further had has have having he he'd he'll hence he's her here here's hers herself him himself his how how's I I'd I'll I'm I've if in into is it it's its itself just let's may maybe me might mine many more  must my myself of oh on once only ok or other ought our ours ourselves out over own she she'd she'll she's should so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was we we'd we'll we're we've were what what's what’s when whenever when's where whereas wherever where's whether which while who whoever who's whose whom why way ways why's will with within would yes yet you you'd you'll you're you've your yours yourself yourselves - _ . < > : ; " ' """
        stopwordslist = stopwords.split(" ")
        querylist = find.split(" ")
        find = ""
        for queryword in querylist:
            flag = 0
            for stopword in stopwordslist:
                if queryword == stopword:
                    flag = 1
                    break
            if flag == 1:
                pass
            elif flag == 0:
                find = find + " " + queryword
        find = find.strip()
        print("find ", find)



        dataset = WebContent.objects.filter(webpage_keywords__icontains=find)
        paginator = Paginator(dataset, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        end = time()
        total_time = round(end - start, 3)
        return render(request, "result.html",
                      {"page_obj": page_obj, "paginator": paginator, "total_time": total_time, "query": query,
                       "data": find})


def ajax(request):
    query = request.GET.get('q')
    qs = Keywords.objects.filter(kname__istartswith=query)[0:10]
    if qs:
        output = "<ul>"
        for page in qs:
            output = output + "<li>" + page.kname.strip().lower() + "</li>"
        output = output + "</ul>"
        print("output: " , output)
    else:
        output = " "
    return HttpResponse(output)


# --------------------------------------------------------------------------------------
# ***************************studytool*************************************************
# --------------------------------------------------------------------------------------


import numpy
import pandas
from pandas import Index

left = []
right = []
sequence = []
m1in = []
m1out = []
m2in = []
m2out = []
Total_ET = 0
ITM1 = 0
ITM2 = 0
m2ideolTime = []
pum1 = 0
pum2 = 0
responseData = ""


def n_jobs_on_two_machiens(request):
    return render(request, "n_jobs_on_two_machiens.html")


def cal_n_jobs_on_two_machiens(request):


    def emptydata():
        global left, right, sequence, m1in, m1out, m2in, m2out, Total_ET, ITM1, ITM2, m2ideolTime
        left = []
        right = []
        sequence = []
        m1in = []
        m1out = []
        m2in = []
        m2out = []
        Total_ET = 0
        ITM1 = 0
        ITM2 = 0
        m2ideolTime = []
        pum1 = 0
        pum2 = 0

    # J = '"A" "B" "C" "D" "E" "F" "G" "H" "I"'
    j = request.GET.get('j')
    m1t = request.GET.get('m1t')
    m2t = request.GET.get('m2t')
    m1data1 = m1t
    m2data2 = m2t
    Jobs = [str(x) for x in j.split(",")]
    m1data = [eval(x) for x in m1data1.split(",")]
    m2data = [eval(x) for x in m2data2.split(",")]

    M1 = pandas.Series(m1data, Jobs)
    M2 = pandas.Series(m2data, Jobs)

    data = {"M1": M1, "M2": M2}
    dataFrame = pandas.DataFrame(data)

    def cal_sequence():
        for i in Jobs:
            m1Min = int(M1.min())
            m2Min = int(M2.min())
            m1CorrospondingValues = []
            m2CorrospondingValues = []
            M1CorrospondingValues = numpy.array(m1CorrospondingValues)
            M2CorrospondingValues = numpy.array(m2CorrospondingValues)

            if m1Min < m2Min:
                m1duplicate = list(M1[M1 == m1Min].index)
                for i in m1duplicate:
                    m1CorrospondingValues.append(int(M2.get(key=i)))
                Dseries = pandas.Series(m1CorrospondingValues, m1duplicate)
                smallestValue = Dseries.min()
                smallestValueIndex = (Dseries[Dseries == smallestValue].index[0])
                left.append(smallestValueIndex)
                M1.drop(smallestValueIndex, inplace=True)
                M2.drop(smallestValueIndex, inplace=True)

            elif m2Min < m1Min:
                m2duplicate = list(M2[M2 == m2Min].index)
                for i in m2duplicate:
                    m2CorrospondingValues.append(M1.get(key=i))
                Dseries = pandas.Series(m2CorrospondingValues, m2duplicate)
                smallestValue = Dseries.min()
                smallestValueIndex = (Dseries[Dseries == smallestValue].index[0])
                right.append(smallestValueIndex)
                M1.drop(smallestValueIndex, inplace=True)
                M2.drop(smallestValueIndex, inplace=True)
            elif m1Min == m2Min:
                m1smallestValueIndex = (M1[M1 == m1Min].index[0])
                m1CValue = M2.get(key=m1smallestValueIndex)
                m2smallestValueIndex = (M2[M2 == m2Min].index[0])
                m2CValue = M1.get(key=m2smallestValueIndex)
                if m1CValue < m2CValue:
                    left.append(m1smallestValueIndex)
                    M1.drop(m1smallestValueIndex, inplace=True)
                    M2.drop(m1smallestValueIndex, inplace=True)
                    # newDataFrame=dataFrame.drop(m1smallestValueIndex,axis=0,inplace=True)
                elif m2CValue < m1CValue:
                    right.append(m2smallestValueIndex)
                    M1.drop(m2smallestValueIndex, inplace=True)
                    M2.drop(m2smallestValueIndex, inplace=True)
                    # newDataFrame=dataFrame.drop(m2smallestValueIndex,axis=0,inplace=True)
                elif m1CorrospondingValues == m2CorrospondingValues:
                    if m1smallestValueIndex < m2smallestValueIndex:
                        left.append(m1smallestValueIndex)
                        M1.drop(m1smallestValueIndex, inplace=True)
                        M2.drop(m1smallestValueIndex, inplace=True)
                        # newDataFrame=dataFrame.drop(smallestValueIndex,axis=0,inplace=True)
                    elif m2smallestValueIndex < m1smallestValueIndex:
                        right.append(m2smallestValueIndex)
                        M1.drop(m2smallestValueIndex, inplace=True)
                        M2.drop(m2smallestValueIndex, inplace=True)
                        # newDataFrame=dataFrame.drop(smallestValueIndex,axis=0,inplace=True)
                    elif m1smallestValueIndex == m2smallestValueIndex:
                        left.append(m1smallestValueIndex)
                        M1.drop(m1smallestValueIndex, inplace=True)
                        M2.drop(m1smallestValueIndex, inplace=True)
                        # newDataFrame=dataFrame.drop(smallestValueIndex,axis=0,inplace=True)

        right.reverse()
        print("type of dataframe is :", type(dataFrame))
        print(dataFrame)
        global sequence, responseData
        sequence = left + right

        print("Sequence : ", left + right)

    def ideolTime_m1():
        global m1in, m1out
        for i in range(len(Jobs)):
            m1in.append(0)
            m1out.append(0)
            if i == 0:
                m1in[i] = 0
                out = sequence[i]
                index = Jobs.index(out)
                m1out[i] = m1data[index]
            else:
                m1in[i] = m1out[i - 1]
                out = sequence[i]
                index = Jobs.index(out)
                m1out[i] = m1out[i - 1] + m1data[index]

    def ideolTime_m2():
        global m2in, m2out
        for i in range(len(Jobs)):
            m2in.append(0)
            m2out.append(0)
            if i == 0:
                m2in[i] = m1out[i]
                out = sequence[i]
                index = Jobs.index(out)
                m2out[i] = m2in[i] + m2data[index]
            else:
                if m2out[i - 1] > m1out[i]:
                    m2in[i] = m2in[i] + m2out[i - 1]
                    out = sequence[i]
                    index = Jobs.index(out)
                    m2out[i] = m2in[i] + m2data[index]
                elif m1out[i] > m2out[i - 1]:
                    m2in[i] = m1out[i]
                    out = sequence[i]
                    index = Jobs.index(out)
                    m2out[i] = m2in[i] + m2data[index]
                elif m1out[i] == m2out[i - 1]:
                    m2in[i] = m1out[i]
                    out = sequence[i]
                    index = Jobs.index(out)
                    m2out[i] = m2in[i] + m2data[index]

        global Total_ET
        Total_ET = m2out[-1]

    def Cal_ideolTimeM1():
        global ITM1
        ITM1 = m2out[-1] - m1out[-1]
        print("The Ideol time for machien M1 :", ITM1)

    def Cal_ideolTimeM2():
        global ITM2
        for i in range(len(Jobs)):
            m2ideolTime.append(0)
            if i == 0:
                m2ideolTime[0] = m1out[i]
            elif m2in[i] > m2out[i - 1]:
                m2ideolTime[i] = m2in[i] - m2out[i - 1]
        for i in range(len(m2ideolTime)):
            global ITM2
            ITM2 = ITM2 + m2ideolTime[i]
        print("The Ideol time for machien M2 :", ITM2)

    def PUM1():
        global pum1
        pum1 = ((Total_ET - ITM1) / Total_ET) * 100
        print("percentage utilization of machiene m1 :", pum1, "%")

    def PUM2():
        global pum2
        pum2 = ((Total_ET - ITM2) / Total_ET) * 100
        print("percentage utilization of machiene m1 :", pum2, "%")

    def outputData():
        cal_sequence()
        ideolTime_m1()
        ideolTime_m2()

        print(dataFrame)
        Cal_ideolTimeM1()
        Cal_ideolTimeM2()
        # print()
        PUM1()
        PUM2()
        print()
        print()

    def sendResponse():
        global responseData, sequence, m1in, m1out, m2in, m2out, ITM1, ITM2
        dictionary = {"m1in": m1in, "m1out": m1out, "m2in": m2in, "m2out": m2out}
        dataFrameFinal = pandas.DataFrame(dictionary, sequence)
        responseData = ""
        responseData = responseData + "<label id='givenDataHeading'> Given Data </label>"
        responseData = responseData + "<table id='givenData' border='1' cellspacing='5'><tr><th><tr><th>Jobs</th><th>M1</th><th>M2</th></tr>"
        for ind in dataFrame.index:  # showing dataframe data
            responseData = responseData + "<tr><td>"
            responseData = responseData + ind
            responseData = responseData + "</td><td>"
            m1 = str(dataFrame["M1"][ind])
            responseData = responseData + m1 + "</td><td>"
            m2 = str(dataFrame["M2"][ind])
            responseData = responseData + m2 + "</td></tr>"
        responseData = responseData + "</table><br>"
        responseData = responseData + "<label id='sequenceTableHeading'>Job Sequence for the given problem will be</label>"
        responseData = responseData + "<table id='sequenceTable' border='1' cellspacing='5'><tr><th width='25'> jobs </th>"
        print(sequence)
        for seq in sequence:  # showing sequence
            responseData = responseData + "<td width='25'>" + seq + "</td>"
        responseData = responseData + "</tr></table> <br>"
        responseData = responseData + "<label id='TableToCalculateIdleTimeForBothMachinesHeading'>Table to calculate Idle time for both machines</label><br>"
        responseData = responseData + "<table id='TableToCalculateIdleTimeForBothMachines' border='1'><th>Jobs</th><th>M1in</th><th>M1out</th><th>M2in</th><th>M2out</th>"
        for ind in dataFrameFinal.index:  # table to calculate idil time
            responseData = responseData + "<tr><td>" + ind + "</td>"
            m1in = str(dataFrameFinal["m1in"][ind])
            responseData = responseData + "<td>" + m1in + "</td>"
            m1out = str(dataFrameFinal["m1out"][ind])
            responseData = responseData + "<td>" + m1out + "</td>"
            m2in = str(dataFrameFinal["m2in"][ind])
            responseData = responseData + "<td>" + m2in + "</td>"
            m2out = str(dataFrameFinal["m2out"][ind])
            responseData = responseData + "<td>" + m2out + "</td>"
        responseData = responseData + "</tr></table><br>"
        responseData = responseData + "<label id='IdleTimeForMachineM1'>" + "Idle time for Machine M1 = " + str(
            ITM1) + "</label><br>"
        responseData = responseData + "<label id='IdleTimeForMachineM2'>" + "Idle time for Machine M2 = " + str(
            ITM2) + "</label><br>"
        responseData = responseData + "<label id='PercentageUtilizationofMachineM1'>" + "Percentage Utilization of Machine M1 = " + str(
            pum1) + "%" + "</label><br>"
        responseData = responseData + "<label id='PercentageUtilizationofMachineM2'>" + "Percentage Utilization of Machine M2 = " + str(
            pum2) + "%" + "</label><br>"

    emptydata()
    outputData()
    sendResponse()

    return HttpResponse(responseData)


# ------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------PDF-----------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------

def getPdf(request):

    j = request.GET.get('txt11')
    m1t = request.GET.get('txt12')
    m2t = request.GET.get('txt13')
    m1data1 = m1t
    m2data2 = m2t
    Jobs = [str(x) for x in j.split(",")]
    m1data = [eval(x) for x in m1data1.split(",")]
    m2data = [eval(x) for x in m2data2.split(",")]

    M1 = pandas.Series(m1data, Jobs)
    M2 = pandas.Series(m2data, Jobs)
    data = {"M1": M1, "M2": M2}
    dataFrame = pandas.DataFrame(data)


    def emptydata():
        global left, right, sequence, m1in, m1out, m2in, m2out, Total_ET, ITM1, ITM2, m2ideolTime
        left = []
        right = []
        sequence = []
        m1in = []
        m1out = []
        m2in = []
        m2out = []
        Total_ET = 0
        ITM1 = 0
        ITM2 = 0
        m2ideolTime = []
        pum1 = 0
        pum2 = 0


    def cal_sequence():
        for i in Jobs:
            m1Min = int(M1.min())
            m2Min = int(M2.min())
            m1CorrospondingValues = []
            m2CorrospondingValues = []
            M1CorrospondingValues = numpy.array(m1CorrospondingValues)
            M2CorrospondingValues = numpy.array(m2CorrospondingValues)

            if m1Min < m2Min:
                m1duplicate = list(M1[M1 == m1Min].index)
                for i in m1duplicate:
                    m1CorrospondingValues.append(int(M2.get(key=i)))
                Dseries = pandas.Series(m1CorrospondingValues, m1duplicate)
                smallestValue = Dseries.min()
                smallestValueIndex = (Dseries[Dseries == smallestValue].index[0])
                left.append(smallestValueIndex)
                M1.drop(smallestValueIndex, inplace=True)
                M2.drop(smallestValueIndex, inplace=True)

            elif m2Min < m1Min:
                m2duplicate = list(M2[M2 == m2Min].index)
                for i in m2duplicate:
                    m2CorrospondingValues.append(M1.get(key=i))
                Dseries = pandas.Series(m2CorrospondingValues, m2duplicate)
                smallestValue = Dseries.min()
                smallestValueIndex = (Dseries[Dseries == smallestValue].index[0])
                right.append(smallestValueIndex)
                M1.drop(smallestValueIndex, inplace=True)
                M2.drop(smallestValueIndex, inplace=True)
            elif m1Min == m2Min:
                m1smallestValueIndex = (M1[M1 == m1Min].index[0])
                m1CValue = M2.get(key=m1smallestValueIndex)
                m2smallestValueIndex = (M2[M2 == m2Min].index[0])
                m2CValue = M1.get(key=m2smallestValueIndex)
                if m1CValue < m2CValue:
                    left.append(m1smallestValueIndex)
                    M1.drop(m1smallestValueIndex, inplace=True)
                    M2.drop(m1smallestValueIndex, inplace=True)
                    # newDataFrame=dataFrame.drop(m1smallestValueIndex,axis=0,inplace=True)
                elif m2CValue < m1CValue:
                    right.append(m2smallestValueIndex)
                    M1.drop(m2smallestValueIndex, inplace=True)
                    M2.drop(m2smallestValueIndex, inplace=True)
                    # newDataFrame=dataFrame.drop(m2smallestValueIndex,axis=0,inplace=True)
                elif m1CorrospondingValues == m2CorrospondingValues:
                    if m1smallestValueIndex < m2smallestValueIndex:
                        left.append(m1smallestValueIndex)
                        M1.drop(m1smallestValueIndex, inplace=True)
                        M2.drop(m1smallestValueIndex, inplace=True)
                        # newDataFrame=dataFrame.drop(smallestValueIndex,axis=0,inplace=True)
                    elif m2smallestValueIndex < m1smallestValueIndex:
                        right.append(m2smallestValueIndex)
                        M1.drop(m2smallestValueIndex, inplace=True)
                        M2.drop(m2smallestValueIndex, inplace=True)
                        # newDataFrame=dataFrame.drop(smallestValueIndex,axis=0,inplace=True)
                    elif m1smallestValueIndex == m2smallestValueIndex:
                        left.append(m1smallestValueIndex)
                        M1.drop(m1smallestValueIndex, inplace=True)
                        M2.drop(m1smallestValueIndex, inplace=True)
                        # newDataFrame=dataFrame.drop(smallestValueIndex,axis=0,inplace=True)

        right.reverse()
        print("type of dataframe is :", type(dataFrame))
        print(dataFrame)
        global sequence, responseData
        sequence = left + right

        print("Sequence : ", left + right)

    def ideolTime_m1():
        global m1in, m1out
        for i in range(len(Jobs)):
            m1in.append(0)
            m1out.append(0)
            if i == 0:
                m1in[i] = 0
                out = sequence[i]
                index = Jobs.index(out)
                m1out[i] = m1data[index]
            else:
                m1in[i] = m1out[i - 1]
                out = sequence[i]
                index = Jobs.index(out)
                m1out[i] = m1out[i - 1] + m1data[index]
        print("M1in",m1in)
        print("m1outin",m1out)

    def ideolTime_m2():
        global m2in, m2out
        for i in range(len(Jobs)):
            m2in.append(0)
            m2out.append(0)
            if i == 0:
                m2in[i] = m1out[i]
                out = sequence[i]
                index = Jobs.index(out)
                m2out[i] = m2in[i] + m2data[index]
            else:
                if m2out[i - 1] > m1out[i]:
                    m2in[i] = m2in[i] + m2out[i - 1]
                    out = sequence[i]
                    index = Jobs.index(out)
                    m2out[i] = m2in[i] + m2data[index]
                elif m1out[i] > m2out[i - 1]:
                    m2in[i] = m1out[i]
                    out = sequence[i]
                    index = Jobs.index(out)
                    m2out[i] = m2in[i] + m2data[index]
                elif m1out[i] == m2out[i - 1]:
                    m2in[i] = m1out[i]
                    out = sequence[i]
                    index = Jobs.index(out)
                    m2out[i] = m2in[i] + m2data[index]

        global Total_ET
        Total_ET = m2out[-1]

    def Cal_ideolTimeM1():
        global ITM1
        ITM1 = m2out[-1] - m1out[-1]
        print("The Ideol time for machien M1 :", ITM1)

    def Cal_ideolTimeM2():
        global ITM2
        for i in range(len(Jobs)):
            m2ideolTime.append(0)
            if i == 0:
                m2ideolTime[0] = m1out[i]
            elif m2in[i] > m2out[i - 1]:
                m2ideolTime[i] = m2in[i] - m2out[i - 1]
        for i in range(len(m2ideolTime)):
            global ITM2
            ITM2 = ITM2 + m2ideolTime[i]
        print("The Ideol time for machien M2 :", ITM2)

    def PUM1():
        global pum1
        pum1 = ((Total_ET - ITM1) / Total_ET) * 100
        print("percentage utilization of machiene m1 :", pum1, "%")

    def PUM2():
        global pum2
        pum2 = ((Total_ET - ITM2) / Total_ET) * 100
        print("percentage utilization of machiene m1 :", pum2, "%")

    def outputData():
        cal_sequence()
        ideolTime_m1()
        ideolTime_m2()

        print(dataFrame)
        Cal_ideolTimeM1()
        Cal_ideolTimeM2()
        # print()
        PUM1()
        PUM2()
        print()
        print()

    def sendResponse():
        global responseData, sequence, m1in, m1out, m2in, m2out, ITM1, ITM2
        dictionary = {"m1in": m1in, "m1out": m1out, "m2in": m2in, "m2out": m2out}
        dataFrameFinal = pandas.DataFrame(dictionary, sequence)
        responseData = ""

    emptydata()
    outputData()
    sendResponse()
    print("m1in",m1in)
    print("m2in",m2in)
    mylist = zip(Jobs,m1data,m2data)
    group = zip(sequence,m1in,m1out,m2in,m2out)
    data = {"mylist":mylist,"sequences":sequence,"group":group,"ITM1":ITM1,"ITM2":ITM2,"pum1":pum1,"pum2":pum2}
    pdf = render_to_pdf('pdf.html',data)
    return HttpResponse(pdf, content_type='application/pdf')


# ------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------Game Theory---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------
def gameTheory(request):
    return render(request,"GameTheory.html")

game=numpy.array([])
total_rows = 0
total_coloums = 0
responseData = ""
method = ""


def gametheory(request):
    global game,total_rows,total_coloums,method
    lists = []
    method = request.GET.get('method')
    total_rows = int(request.GET.get('number_of_rows'))
    total_coloums = int(request.GET.get('number_of_coloumns'))
    data = request.GET.get('data')
    data = data.strip()
    values = [ int(x)  for x in data.split(" ")]
    for i in range(int(total_rows)):
        lists.append([])

    for list in lists:
        for j in range(int(total_coloums)):
          list.append(values[j])
        del values[0:int(total_coloums)]

    game = numpy.array(lists)
    print(game)
    print("number_of_rows",game.shape[0])
    print("number_of_coloumns",game.shape[1])

    def display_matrix():
        global game,total_rows,total_coloums,responseData

        print("ram krishna hari")
        responseData = responseData + "<table>"
        try:
            for i in range(total_rows + 1):
                responseData = responseData + "<tr>"
                for j in range(total_coloums + 1):
                    if i == 0 and j == 0:
                        responseData = responseData + "<td>A\B</td>"
                    elif i == 0 and j != 0:
                        responseData = responseData + "<td>B" + str(j) + "</td>"
                    elif j == 0 and i != 0:
                        responseData = responseData + "<td>A" + str(i) + "</td>"
                    elif i != 0 and j != 0:
                        responseData = responseData + "<td>" + str(game[i - 1][j - 1]) + "</td>"

                responseData = responseData + "</tr>"
            responseData = responseData + "</table><br>"

        except :print()


    def check(result):
        counter = 0
        for value in result:
            if value == True:
                counter = counter + 1
        if len(result) == counter:
            return True
        else:
            return False


    def pureStrategy():
        global game , total_rows , total_coloums , responseData
        responseData = responseData + "<b>Find solution of game theory problem using pure startegy method </b><br>"
        display_matrix()
        responseData = responseData +"<b>Solution : </b><br>"
        display_matrix()
        responseData = responseData + "we apply maxmin and minmax principal to analyze the game <br> "
        minValues = numpy.amin(game, axis=1)
        maxValues = numpy.amax(game, axis=0)
        MaxMin = minValues.max()
        MinMax = maxValues.min()
        responseData = responseData + " Now we will find minimum value of each row <br>"
        responseData = responseData + " Minimum value of each row is : "+str(minValues)+"<br>"
        responseData = responseData + " So MaxMin is : "+str(MaxMin)+"<br>"
        responseData = responseData + "Now we will find maximum value of each column <br>"
        responseData = responseData + " Maximum value of each column is : "+ str(maxValues) + "<br>"
        responseData = responseData + " So MinMax is : "+str(MinMax)+"<br>"

        values_of_game = []
        if MaxMin == MinMax:
            responseData = responseData + "MaxMin and MinMax are same . So saddle point is exist ."
            result = numpy.where(minValues == MaxMin)
            index_of_MaxMin = result[0]
            result = numpy.where(maxValues == MinMax)
            index_of_MinMax = result[0]
            if (len(index_of_MaxMin) > 1) & (len(index_of_MinMax) > 1):
                for i in index_of_MaxMin:
                    for j in index_of_MinMax:
                        values_of_game.append(game[i, j])
                strategy_A = game[i]
                for l in range(strategy_A.size):
                    if l == j :
                        strategy_A[l] = 1
                    else:
                        strategy_A[l] =0
                strategy_B = game[:,j]
                for m in range(strategy_B.size) :
                    if m == i:
                        strategy_B[m] = 1
                    else:strategy_B[m] = 0

                print('values of game', values_of_game)
                print("optimal strategy for player A is : ", i)
                print("optimal strategy for player B is : ", j)
                vog = values_of_game[0]
                responseData = responseData + "<h5>values of game" + str(vog)+"</h5>"
                responseData = responseData + "<h5>optimal strategy for player A is : "+str(strategy_A)+"<h5>"
                responseData = responseData + "<h5>optimal strategy for player B is : "+ str(strategy_B)+"<br><br><h5>"
            elif len(index_of_MaxMin) > 1:
                for i in index_of_MaxMin:
                    values_of_game.append(game[i, index_of_MinMax])

                strategy_A = game[i]
                for l in range(strategy_A.size):
                    if l == index_of_MinMax[0]:
                        strategy_A[l] = 1
                    else:
                        strategy_A[l] = 0
                strategy_B = game[:, index_of_MinMax[0]]
                for m in range(strategy_B.size):
                    if m == i:
                        strategy_B[m] = 1
                    else:
                        strategy_B[m] = 0

                print('values of game', values_of_game[0])
                print("optimal strategy for player A is : ", i)
                print("optimal strategy for player B is : ", index_of_MinMax)
                vog = values_of_game[0]
                responseData = responseData + "<h5>values of game" + str(vog)+"</h5>"
                responseData = responseData + "<h5>optimal strategy for player A is : "+str(strategy_A)+"<h5>"
                responseData = responseData + "<h5>optimal strategy for player B is : "+ str(strategy_B)+"<br><br><h5>"
            elif len(index_of_MinMax) > 1:
                for j in index_of_MinMax:
                    values_of_game.append(game[index_of_MaxMin, j])
                vog = values_of_game[0]

                strategy_A = game[index_of_MaxMin[0]]
                for l in range(strategy_A.size):
                    if l == j:
                        strategy_A[l] = 1
                    else:
                        strategy_A[l] = 0
                strategy_B = game[:, j]
                for m in range(strategy_B.size):
                    if m == index_of_MaxMin[0]:
                        strategy_B[m] = 1
                    else:
                        strategy_B[m] = 0

                print('values of game', values_of_game[0])
                print("optimal strategy for player A is : ", index_of_MaxMin)
                print("optimal strategy for player B is : ", j)
                responseData = responseData + "<h5>values of game" + str(vog)+"</h5>"
                responseData = responseData + "<h5>optimal strategy for player A is : "+str(strategy_A)+"<h5>"
                responseData = responseData + "<h5>optimal strategy for player B is : "+ str(strategy_B)+"<br><br><h5>"
            elif (len(index_of_MaxMin) == 1) & (len(index_of_MinMax) == 1):
                values_of_game.append(game[index_of_MaxMin, index_of_MinMax])
                vog = values_of_game[0]
                strategy_A = game[index_of_MaxMin[0]]
                for l in range(strategy_A.size):
                    if l == index_of_MinMax[0]:
                        strategy_A[l] = 1
                    else:
                        strategy_A[l] = 0
                strategy_B = game[:, index_of_MinMax[0]]
                for m in range(strategy_B.size):
                    if m == index_of_MaxMin[0]:
                        strategy_B[m] = 1
                    else:
                        strategy_B[m] = 0

                print('values of game', values_of_game[0])
                print("optimal strategy for player A is : ", index_of_MaxMin)
                print("optimal strategy for player B is : ", index_of_MinMax)
                responseData = responseData + "<h5>values of game : " + str( vog )+"</h5>"
                responseData = responseData + "<h5>optimal strategy for player A is : "+str(strategy_A)+"<h5>"
                responseData = responseData + "<h5>optimal strategy for player B is : "+ str(strategy_B)+"<br><br><h5>"
        else:
            print(
                "There is no saddle point in given problem therefore given problem can not be solve by Pure Strategy meyhod.")
            print("Use another method to solve the problem.")
            responseData = responseData + "There is no saddle point in given problem therefore given problem can not be solve by Pure Strategy meyhod. <br>"
            responseData = responseData + "Use another method to solve the problem.<br><br><br>"




    def algebric_method():
        global game ,total_rows,total_coloums,responseData
        responseData = responseData + "<b>Now we will solve problem by using algebric method</b><br>"
        a11 = game[0][0]
        a12 = game[0][1]
        a21 = game[1][0]
        a22 = game[1][1]
        result = ((a11 * a22) - (a12 * a21)) / ((a11 + a22) - (a12 + a21))
        x = (a22 - a12) / ((a11 + a22) - (a12 + a21))
        y = (a22 - a21) / ((a11 + a22) - (a12 + a21))
        responseData = responseData + "x = (a22 - a12) / ((a11 + a22) - (a12 + a21))<br>"
        responseData = responseData + "x = ("+str(a22)+" -"+ str(a12)+") / (("+str(a11)+" + "+str(a22)+") - ("+str(a12)+" + "+str(a21)+"))<br>"
        responseData = responseData + "x = "+str(x)+"<br>"
        responseData = responseData + "y = (a22 - a21) / ((a11 + a22) - (a12 + a21))<br>"
        responseData = responseData + "y = ("+str(a22)+" -"+ str(a21)+") / (("+str(a11)+" + "+str(a22)+") - ("+str(a12)+" + "+str(a21)+"))<br>"
        responseData = responseData + "y = "+str(y)+"<br>"
        responseData = responseData + "Value of game = ((a11 * a22) - (a12 * a21)) / ((a11 + a22) - (a12 + a21))<br>"
        responseData = responseData + "Value of game = (("+str(a11)+" * "+str(a22) + ") - ("+str(a12)+" * "+ str(a21)+")) / (("+str(a11)+" + "+str(a22)+") - ("+str(a12)+" + "+str(a21)+"))<br>"
        responseData = responseData + "Value of game = " + str(result)
        responseData = responseData + "<br>So , <br><h5>Optimal strategy for player A is : "+str(x) +" </h5>"
        responseData = responseData + "<h5>Optimal strategy for player B is : " + str(y) + " </h5>"
        responseData = responseData + "<h5>Value of game is : " + str(result) + " </h5><br><br><br><br><br>"
        print("Optimal strategy for player A is : ", x)
        print("Optimal strategy for player B is : ", y)
        print("Value of game is : ", result)

    def reduce_rows():
        flag = 0
        global game, total_rows,responseData ,total_coloums
        display_matrix()
        print("now we will reduce rows by using dominance rule")
        print(game)
        if game.size == 1 :
            pass
        elif game.shape[0] == 1 :
            pass
        else:
            responseData =responseData + "now we will reduce rows by using dominance rule <br>"
            # display_matrix()
        if game.shape[0] != 1 :
            for i in range(total_rows):
                try:
                    for j in range(total_rows):
                        if i == j:
                            pass
                        else:
                            result = game[i] <= game[j]
                            r = check(result)
                            if r == True:

                                responseData = responseData + " values of row no." + str(
                                    i + 1) + " are smaller than values  row no. " + str(j + 1) + " <br>"
                                responseData = responseData + "so we delete row no." + str(i + 1) + "<br>"
                                total_rows = total_rows - 1
                                game = numpy.delete(game, i, axis=0)
                                flag = 1

                                print("after delete row no." + str(i + 1) + " matrix is: ")
                                responseData = responseData + "after delete row no. " + str(
                                    i + 1) + " payoff matrix is: <br>"
                                print(game)
                                # display_matrix()
                                reduce_rows()

                            else:
                                print(str(i + 1) + " th row's values are greater than  " + str(j + 1) + "th rows")
                                responseData = responseData + " values of row no. " + str(
                                    i + 1) + " are greater than values of row no. " + str(j + 1) + "<br>"
                except:
                    print()
        else:
            responseData = responseData + "there is only one row so , we con not reduce it.<br>"


        if game.size == 1:
            return "done"

        elif flag == 0:
            return "not_reduce_rows"
        elif flag == 1:
            return "reduce_rows"

    def reduce_columns():
        flag = 0
        display_matrix()
        global game, total_coloums,total_rows,responseData
        print("now we will reduce columns by using dominance rule")
        print(game)
        if game.size == 1:
            pass
        elif game.shape[1] == 1:
            pass
        else:
            responseData = responseData + "now we will reduce columns by using dominance rule <br>"
            # display_matrix()
        if game.shape[1] != 1:
            for i in range(total_coloums):
                for j in range(total_coloums):
                    if i == j:
                        pass
                    else:
                        try:
                            result = game[:, [i]] >= game[:, [j]]
                            r = check(result)
                            if r == True:
                                responseData = responseData + " values of column no. " + str(
                                    i + 1) + " are greater than values of column no." + str(j + 1) + " <br> "
                                print(str(i + 1) + "th column's values are greater than  " + str(j + 1) + "th column ")
                                game = numpy.delete(game, i, axis=1)
                                total_coloums = total_coloums - 1
                                flag = 1
                                responseData = responseData + "so , we delete column no. " + str(i + 1) + " <br>"
                                responseData = responseData + "after delete column no. " + str(
                                    i + 1) + " payoff matrix is <br> "
                                print("so , we delete " + str(i + 1) + "th column ")
                                print("after delete " + str(i + 1) + "th column matrix is ")
                                print(game)
                                # display_matrix()
                                reduce_columns()

                            else:
                                responseData = responseData + "values of column no. " + str(
                                    i + 1) + " are smaller than values of column no. " + str(j + 1) + "<br>"
                                print(str(i + 1) + " th column values are smaller than " + str(j + 1) + "th column  ")
                        except:
                            print()
        else:
            responseData = responseData + "now there is only one column so , we can not reduce it.<br>"
        if game.size == 1:
            # print("Value of game is c:", game)
            return "done"
        elif flag == 0:
            return "not_reduce_columns"
        elif flag == 1:
            return "reduce_columns"

    def avg_rows():
        flag = 0
        display_matrix()
        global game, total_coloums,total_rows,responseData
        if game.size <= 2:
            pass
        elif game.shape[0] <= 2:
            pass
        else:
            responseData = responseData + "now we will reduce rows by taking avarage of two rows dominance rule <br>"
            display_matrix()
        # print("further we can not eliminate rows and columns")
        # print("now we can solve this problem by using mixed strategy method")
        if game.shape[0] > 2:
            try:
                for i in range(total_rows):
                    for j in range(total_rows):
                        if i == j:
                            pass
                        elif game.shape[0] > 2:
                            a = game[i] + game[j]
                            a = a / 2

                            # responseData = responseData + "avarage of row no. " + str(i + 1) + " and " + str(j + 1) + " is :"
                            # responseData = responseData + "<table><tr>"
                            # for x in range(a.size):
                            #     responseData = responseData + "<td>" + str(a[x]) + "</td>"
                            # responseData = responseData + "</tr></table><br>"
                            responseData = responseData + "<br>avarage of row no. " + str(i + 1) + " and " + str(j + 1) + " is : " + str(a)+"<br>"
                            for k in range(total_rows):
                                if k == i or k == j:

                                    pass
                                else:
                                    result = game[k] <= a
                                    r = check(result)

                                    if r == True:
                                        responseData = responseData +"values of row no. "+str(k+1)+" : "+ str(game[k])+"<br>"
                                        responseData = responseData + " values of row no. " + str(k+1) +" are less than or equal to avarage of no. "+ str(i+1) +" and "+ str(j+1) +" rows <br>"
                                        responseData = responseData +"so , we delete row no." + str(k+1) +"<br>"
                                        game = numpy.delete(game, k, axis=0)
                                        total_rows = total_rows - 1
                                        responseData = responseData +" after ,  delete row no." + str(k+1) +" payoff matrix is : <br>"
                                        display_matrix()
                                        flag = 1
                                        avg_rows()
                                    else:
                                        # display_matrix()
                                        responseData = responseData +"values of row no. "+str(k+1)+" : "+ str(game[k])+"<br>"
                                        responseData = responseData + " values of row no. " + str(k+1) +" are not less than or equal to avarage of no. " + str(i+1) +" and "+ str(j+1) +" rows <br>"

            except:
                print()

        if game.size == 1:
            # print("Value of game is :", game)
            return "done"
        elif flag == 0:
            return "not_reduce_rows_by_avg"
        elif flag == 1:
            return "reduce_rows_by_avg"

    def avg_columns():
        display_matrix()
        flag = 0
        global game, total_rows,total_coloums ,responseData
        if game.size <= 2:
            pass
        elif game.shape[1] <= 2:
            pass
        else:
            responseData = responseData + "now we will reduce column by taking avarage of two columns dominance rule <br>"
            # display_matrix()

        if game.shape[1] > 2 :
            try:
                for i in range(total_coloums):
                    for j in range(total_coloums):
                        if i == j:
                            pass
                        elif game.shape[1] > 2:
                            a = game[:, i] + game[:, j]
                            a = a / 2
                            responseData = responseData + "<br>avarage of column no. " + str(i + 1) + " and " + str(j + 1) + " is : " + str(a)+"<br>"
                            for k in range(total_coloums):

                                if k == i or k == j:
                                    pass
                                else:

                                    result = game[:, k] >= a
                                    r = check(result)


                                    if r == True:
                                        responseData = responseData +"values of column no. "+str(k+1)+" : "+ str(game[k])+"<br>"
                                        responseData = responseData + " values of column no. " + str(k + 1) + " are greater than or equal to avarage of no. " + str(i + 1) + " and " + str(j + 1) + " columns <br>"
                                        responseData = responseData + "so , we delete column no." + str(k + 1) + "<br>"
                                        game = numpy.delete(game, k, axis=1)
                                        total_coloums = total_coloums - 1
                                        responseData = responseData +" after ,  delete column no." + str(k+1) +" payoff matrix is : <br>"
                                        display_matrix()
                                        flag = 1
                                        avg_columns()
                                    else:
                                        responseData = responseData + "values of column " + str(k+1) +" : " + str(game[:,k]) +"<br>"
                                        responseData = responseData + " values of column no. " + str(k+1) +" are not greater than or equal to avarage of no. " + str(i+1) +" and "+ str(j+1) +" coloums  <br>"

            except:
                print()

        if game.size == 1:
            # print("Value of game is :", game)
            return "done"
        elif flag == 0:
            return "not_reduce_columns_by_avg"
        elif flag == 1:
            return "reduce_columns_by_avg"

    def algebric():
        global game, responseData
        z = 0
        question = "Find solution of game theory problem  using algebric  method <br>"
        responseData = responseData + "<b>"+question+"</b>"
        display_matrix()
        responseData = responseData +"<b>Solution : </b> <br> "
        if game.shape[0] == 2 and game.shape[1] == 2:
            algebric_method()
        else:
            while z != 1:
                a = reduce_rows()
                b = reduce_columns()
                if a == "reduce_rows" or b == "reduce_columns" or a == "done" or b == "done":
                    while a == "reduce_rows" or b == "reduce_columns" or a == "done" or b == "done":
                        if a == "done" or b == "done":
                            print("gameTheory", game)
                            responseData = responseData + " <h5>so value of game is : " + str(game[0][0]) + "</h5>"
                            responseData = responseData + " <h5>Solution by using algebric method size of  row and column  must be 2,<br> so further solution is not possible .</h5>"
                            return "done"
                        a = reduce_rows()
                        b = reduce_columns()

                if a == "not_reduce_rows" or b == "not_reduce_columns":
                    c = avg_rows()
                    d = avg_columns()
                    while c == "reduce_rows_by_avg" or d == "reduce_columns_by_avg" or c == "done" or d == "done":
                        if c == "done" or d == "done":
                            print("gameTheory", game)
                            responseData = responseData + " <h5>so value of game is : " + str(game[0][0]) + "</h5>"
                            responseData = responseData + " <h5>so value of game is : " + str(game[0][0]) + "</h5>"
                            responseData = responseData + " <h5>Solution by using algebric method size of row and column must be 2, <br>so further solution is not possible.</h5>"
                            return
                        c = avg_rows()
                        d = avg_columns()

                a = reduce_rows()
                b = reduce_columns()
                c = avg_rows()
                d = avg_columns()

                if a == "not_reduce_rows" and b == "not_reduce_columns" and c == "not_reduce_rows_by_avg" and d == "not_reduce_columns_by_avg":
                    if game.shape[0] == 2 and game.shape[1] == 2:
                        algebric_method()
                    if game.shape[0] > 2 or game.shape[1] > 2:
                        print(game)
                        display_matrix()
                        responseData = responseData + "<h5>Only 2*2 matrix is solved by algebric method.<br>So this problem can not solve by algebric method <br> This problem can be solve by  another method.</h5>"
                        print("Only 2*2 matrix is solved by algebric method.")
                    z = 1
                else:
                    z = 0

    def dominance():
        z = 0
        question = "<b>Find solution of game theory problem  using dominance  method</b><br>"
        global game, responseData
        responseData = responseData + "<b>" + question + "</b>"
        display_matrix()
        responseData = responseData + "<b>Solution : </b> <br> "
        while z != 1:
            a = reduce_rows()
            b = reduce_columns()
            if a == "reduce_rows" or b == "reduce_columns" or a == "done" or b == "done":
                while a == "reduce_rows" or b == "reduce_columns" or a == "done" or b == "done":
                    if a == "done" or b == "done":
                        print("gameTheory", game)
                        responseData = responseData + " <h5>so value of game is : " + str(game[0][0]) + "</h5>"
                        return "done"
                    a = reduce_rows()
                    b = reduce_columns()
            if a == "not_reduce_rows" or b == "not_reduce_columns":
                c = avg_rows()
                d = avg_columns()
                while c == "reduce_rows_by_avg" or d == "reduce_columns_by_avg" or c == "done" or d == "done":
                    if c == "done" or d == "done":
                        print("gameTheory", game)
                        responseData = responseData + " <h5>so value of game is : " + str(game[0][0]) + "</h5>"
                        return
                    c = avg_rows()
                    d = avg_columns()

            a = reduce_rows()
            b = reduce_columns()
            c = avg_rows()
            d = avg_columns()

            if a == "not_reduce_rows" and b == "not_reduce_columns" and c == "not_reduce_rows_by_avg" and d == "not_reduce_columns_by_avg":
                responseData = responseData +"<h5> Further we can not reduce rows and columns .<br>So this problem can not solve by dominance method <br> This problem can be solve by  another method.</h5>"

                z = 1
            else:
                z = 0


    def arithmetic_method() :
        global game , total_rows, total_coloums ,responseData
        a11 = int(game[0][0])
        a12 = int(game[0][1])
        a21 = int(game[1][0])
        a22 = int(game[1][1])
        row_oddment_of_1st_row = abs(a21 - a22)
        row_oddment_of_2nd_row = abs(a11 - a12)
        column_oddment_of_1st_column = abs(a12 - a22)
        column_oddment_of_2nd_column = abs(a11 - a21)
        A1 = row_oddment_of_1st_row / (row_oddment_of_1st_row + row_oddment_of_2nd_row)
        A2 = row_oddment_of_2nd_row / (row_oddment_of_1st_row + row_oddment_of_2nd_row)
        B1 = column_oddment_of_1st_column / (column_oddment_of_1st_column + column_oddment_of_2nd_column)
        B2 = column_oddment_of_2nd_column / (column_oddment_of_1st_column + column_oddment_of_2nd_column)
        values_of_game = (a11 * column_oddment_of_1st_column + a12 * column_oddment_of_2nd_column)/(row_oddment_of_1st_row + row_oddment_of_2nd_row)
        responseData = responseData + "<b>Now we will find row oddments and column oddments</b> <br>"
        responseData = responseData + "<table><tbody><thead><tr><th> A/B </th><th> B1 </th><th>B2</th><th>row oddemts </th></tr></thead>"
        responseData = responseData +"<tr><th>A1</th><td>"+str(a11)+"</td><td>"+str(a12)+"</td><td>"+str(row_oddment_of_1st_row)+"</td></tr>"
        responseData = responseData +"<tr><th>A2</th><td>"+str(a21)+"</td><td>"+str(a22)+"</td><td>"+str(row_oddment_of_2nd_row)+"</td></tr>"
        responseData = responseData +"<tr><th>columns oddemts</th><td>"+str(column_oddment_of_1st_column)+"</td><td>"+str(column_oddment_of_2nd_column)+"</td><td></td></tr></tbody></table><br>"
        responseData = responseData + "<b>Now we will find probabilities of player A and B ,</b><br>"
        responseData = responseData + "P(A1) = "+str(row_oddment_of_1st_row)+"/("+str(row_oddment_of_1st_row)+"+"+str(row_oddment_of_2nd_row)+")<br>"
        responseData = responseData + "P(A1) = "+ str(A1) +"<br>"
        responseData = responseData + "P(A2) = "+str(row_oddment_of_2nd_row)+"/("+str(row_oddment_of_1st_row)+"+"+str(row_oddment_of_2nd_row)+")<br>"
        responseData = responseData + "P(A2) = " + str(A2) + "<br>"
        responseData = responseData + "P(B1) = "+str(column_oddment_of_1st_column)+"/("+str(column_oddment_of_1st_column)+"+"+str(column_oddment_of_2nd_column)+")<br>"
        responseData = responseData + "P(B1) = " + str(B1) + "<br>"
        responseData = responseData + "P(B2) = "+str(column_oddment_of_2nd_column)+"/("+str(column_oddment_of_1st_column)+"+"+str(column_oddment_of_2nd_column)+")<br>"
        responseData = responseData + "P(B2) = " + str(B2) + "<br>"
        responseData = responseData + "<b> Now we will find value of game </b><br>"
        responseData = responseData + "value of game is : ("+str(a11)+" * "+str(column_oddment_of_1st_column)+" + "+str(a12)+" * "+str(column_oddment_of_2nd_column) +")/("+str(column_oddment_of_1st_column) +" + "+ str(column_oddment_of_2nd_column)+")<br>"
        responseData = responseData + "Value of game is : "+str(values_of_game)+"<br>"
        responseData = responseData + "<b>Now we will find strategies of player A ,</b><br>"
        responseData = responseData + "Strategies of player A : "+"[ "+str(row_oddment_of_1st_row)+"/"+str(row_oddment_of_1st_row + row_oddment_of_2nd_row)+" , "+str(row_oddment_of_2nd_row)+"/"+str(row_oddment_of_1st_row + row_oddment_of_2nd_row)+" ]<br>"
        responseData = responseData + "<b> Now we will find strategies of player B ,</b><br>"
        responseData = responseData + "Strategies of player B : "+"[ "+str(column_oddment_of_1st_column)+"/"+str(row_oddment_of_1st_row + row_oddment_of_2nd_row)+" , "+str(column_oddment_of_2nd_column)+"/"+str(row_oddment_of_1st_row + row_oddment_of_2nd_row)+" ]<br><br>"

    def arithmetic():
        global game, responseData
        question = "<b>Find solution of game theory problem  using arithmetic  method</b> <br>"
        responseData = responseData + question
        display_matrix()
        responseData = responseData + "<b>Solution : </b> <br> "

        if game.shape[0] == 2 and game.shape[1] == 2 :
            arithmetic_method()
        else:
            z = 0
            while z != 1:
                a = reduce_rows()
                b = reduce_columns()
                if a == "reduce_rows" or b == "reduce_columns" or a == "done" or b == "done":
                    while a == "reduce_rows" or b == "reduce_columns" or a == "done" or b == "done":
                        if a == "done" or b == "done":
                            print("gameTheory", game)
                            responseData = responseData + " <h5>so value of game is : " + str(game[0][0]) + "</h5>"
                            responseData = responseData + " <h5>Solution by using arithmetic method size of  row and column  must be 2,<br> so further solution is not possible .</h5>"
                            return "done"
                        a = reduce_rows()
                        b = reduce_columns()

                if a == "not_reduce_rows" or b == "not_reduce_columns":
                    c = avg_rows()
                    d = avg_columns()
                    while c == "reduce_rows_by_avg" or d == "reduce_columns_by_avg" or c == "done" or d == "done":
                        if c == "done" or d == "done":
                            print("gameTheory", game)
                            responseData = responseData + " <h5>so value of game is : " + str(game[0][0]) + "</h5>"
                            responseData = responseData + " <h5>so value of game is : " + str(game[0][0]) + "</h5>"
                            responseData = responseData + " <h5>Solution by using arithmetic method size of row and column must be 2, <br>so further solution is not possible.</h5>"
                            return
                        c = avg_rows()
                        d = avg_columns()

                a = reduce_rows()
                b = reduce_columns()
                c = avg_rows()
                d = avg_columns()

                if a == "not_reduce_rows" and b == "not_reduce_columns" and c == "not_reduce_rows_by_avg" and d == "not_reduce_columns_by_avg":
                    if game.shape[0] == 2 and game.shape[1] == 2:
                        arithmetic_method()
                    if game.shape[0] > 2 or game.shape[1] > 2:
                        print(game)
                        display_matrix()
                        responseData = responseData + "<h5>Only 2*2 matrix is solved by arithmetic method.<br>So this problem can not solve by algebric method <br> This problem can be solve by  another method.</h5>"
                        print("Only 2*2 matrix is solved by algebric method.")
                    z = 1
                else:
                    z = 0


    def emptydata() :
        global game,total_rows,total_coloums,responseData,method
        game = numpy.array([])
        total_rows = 0
        total_coloums =0
        method = " "

    def eraseResponseData() :
        global responseData
        responseData = " "

    def main():
       global method
       if method == "PureStrategy" :
           eraseResponseData()
           pureStrategy()
           emptydata()
       elif method == "Dominance" :
           eraseResponseData()
           dominance()
           emptydata()
       elif method == "Algebric" :
           eraseResponseData()
           algebric()
           emptydata()
       elif method == "Arithmetic" :
           eraseResponseData()
           arithmetic()
           emptydata()

    main()
    return HttpResponse(responseData)