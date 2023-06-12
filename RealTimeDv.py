import urllib
import urllib.parse
from tkinter import *
from tkinter import font
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

DataList = []
url = 'swopenapi.seoul.go.kr'
api_key = '45776f564262626937304e77454758'
query = '/api/subway/' + api_key + '/xml/realtimeStationArrival/0/30/'


def InitRealTime(frame):
    inputBox = Entry(frame)
    inputBox.pack()
    inputBox.place(x=60, y=10)
    button = Button(frame, text='검색', command=lambda : Search(inputBox.get()))
    button.pack()
    button.place(x=220, y=10)
    SnameLabel = Label(frame, text='역 이름')
    SnameLabel.pack()
    SnameLabel.place(x=10, y=10)
    RTRenderText(frame)


def Search(LineName):
    RTRnderTexts.configure(state='normal')
    RTRnderTexts.delete(0.0, END)

    import http.client
    conn = http.client.HTTPConnection(url)
    conn.request("GET", query + quote_plus(LineName))

    req = conn.getresponse()

    global DataList
    DataList.clear()

    if req.status == 200:
        strXml = req.read().decode('utf-8')
        #print(strXml)
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(strXml)
        itemElements = tree.iter('row')
        #print(itemElements)

        for item in itemElements:
            updown = item.find('updnLine')
            LineNm = item.find('trainLineNm')
            Sname = item.find('statnNm')
            Ordkey = item.find('ordkey')
            Tstatus = item.find('btrainSttus')
            DT = item.find('barvlDt')
            RTime = item.find('recptnDt')
            ArMsg = item.find('arvlMsg2')
            ArStatus = item.find('arvlCd')
            DataList.append((updown.text, LineNm.text, Sname.text, Ordkey.text, Tstatus.text,
                             DT.text, RTime.text, ArMsg.text, ArStatus.text))

        print(DataList)

        for i in range(len(DataList)):
            RTRnderTexts.insert(INSERT, '상하행 : ')
            RTRnderTexts.insert(INSERT, DataList[i][0])
            RTRnderTexts.insert(INSERT, ' 도착지 방면 : ')
            RTRnderTexts.insert(INSERT, DataList[i][1])
            RTRnderTexts.insert(INSERT, '\n')
            RTRnderTexts.insert(INSERT, '지하철 역명 : ')
            RTRnderTexts.insert(INSERT, DataList[i][2])
            RTRnderTexts.insert(INSERT, '[')
            RTRnderTexts.insert(INSERT, DataList[i][4])
            RTRnderTexts.insert(INSERT, ']')
            RTRnderTexts.insert(INSERT, '\n')
            RTRnderTexts.insert(INSERT, '열차 도착 예정 시간 : ')
            RTRnderTexts.insert(INSERT, DataList[i][5])
            RTRnderTexts.insert(INSERT, '초')
            RTRnderTexts.insert(INSERT, '\n')
            RTRnderTexts.insert(INSERT, '도착 정보 생성 시간 : ')
            RTRnderTexts.insert(INSERT, DataList[i][6])
            RTRnderTexts.insert(INSERT, '\n')
            RTRnderTexts.insert(INSERT, '현재 상태 : ')
            RTRnderTexts.insert(INSERT, DataList[i][7])
            RTRnderTexts.insert(INSERT, '\n')
            RTRnderTexts.insert(INSERT, '도착 코드 : ')
            # (0:진입, 1:도착, 2:출발, 3:전역출발, 4:전역진입, 5:전역도착, 99:운행중)
            if DataList[i][8] == '0':
                RTRnderTexts.insert(INSERT, '진입')
            elif DataList[i][8] == '1':
                RTRnderTexts.insert(INSERT, '도착')
            elif DataList[i][8] == '2':
                RTRnderTexts.insert(INSERT, '출발')
            elif DataList[i][8] == '3':
                RTRnderTexts.insert(INSERT, '전역출발')
            elif DataList[i][8] == '4':
                RTRnderTexts.insert(INSERT, '전역진입')
            elif DataList[i][8] == '5':
                RTRnderTexts.insert(INSERT, '전역도착')
            elif DataList[i][8] == '99':
                RTRnderTexts.insert(INSERT, '운행중')
            else:
                RTRnderTexts.insert(INSERT, '알수 없음')
            RTRnderTexts.insert(INSERT, '\n')
            RTRnderTexts.insert(INSERT, '\n')

    RTRnderTexts.configure(state='disabled')

def RTRenderText(frame):
    global RTRnderTexts



    RTRnderTextScrollbar = Scrollbar(frame)
    RTRnderTextScrollbar.pack()
    RTRnderTextScrollbar.place(x=375, y=20)

    RTTempFont = font.Font(frame, size=10, family='Consolas')
    RTRnderTexts = Text(frame, width=49, height=36, borderwidth=12, relief='ridge'
                       , yscrollcommand=RTRnderTextScrollbar.set)

    RTRnderTexts.pack()
    RTRnderTexts.place(x=10, y=50)
    RTRnderTextScrollbar.configure(command=RTRnderTexts.yview)
    RTRnderTextScrollbar.pack(side=RIGHT, fill=BOTH)



    '''for i in maps:
        mapping = {
            '상하행': i.findtext('updnLine'),
            '도착지방면': i.findtext('trainLineNm'),
            '지하철역명': i.findtext('statnNm'),
            '도착예정열차순번': i.findtext('ordkey'),
            '열차종류': i.findtext('btrainSttus'),
            '열차도착예정시간' : i.findtext('barvlDt'),
            '현재시간' : i.findtext('recptnDt'),
            '도착메세지' : i.findtext('arvlMsg2'),
            '도착상태' : i.findtext('arvlCd')
        }
        LiveStation.append(mapping)

    print(LiveStation)'''

'''root = Tk()
root.geometry('600x600')
root.title("Subway Data")
InitRealTime(root)
root.mainloop()'''