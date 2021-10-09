import firebase_admin,os,time,requests
from firebase_admin import credentials
from firebase_admin import storage

def sendnotify(texti,texto,userid):
    url = "https://notify-api.line.me/api/notify"
    payload = {'message': "{} \nProcess:{}".format(userid,texti)}


    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Bearer z6fZ4QX8RI3fmDJvMMzZs4n5nXj7lZo4BaoR3wLGMzS'
    }
    requests.request("POST", url, headers=headers, data = payload)
try:
    len(data)
    #from botest.course2 import data
except:
    try:
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'coursecollection-57642.appspot.com'
            })
        
        bucket = storage.bucket()
        blob = bucket.blob('course.py')
        blob.download_to_filename(os.path.join(os.path.dirname(__file__),'course2.py'))
        time.sleep(1.5)
        
        from botest.course2 import data #as tmpdata
        # data=[]
        # data.extend(tmpdata)
        sendnotify('#已更新課程清單','#已更新課程清單','Server')
    except Exception as e:
        sendnotify(e,'null','Server')
try:
    len(tdata)
    #from botest.teanum import tdata
except:
    try:
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'coursecollection-57642.appspot.com'
            })
        
        bucket = storage.bucket()
        blob = bucket.blob('teanum.py')
        blob.download_to_filename(os.path.join(os.path.dirname(__file__),'teanum.py'))
        time.sleep(1.5)
        from botest.teanum import tdata #as tmptdata
        # tdata={}
        # tdata=dict(tmptdata)
        sendnotify('#已更新教師名單','#已更新教師名單','Server')
    except Exception as e:
        sendnotify(e,'null','Server')
import re



def print_key_cat_time(leng,cat,time):
    info = "課程類別:\n{}\n\n時間:(僅列出包含於以下時段的課程)".format(cat)
    for t in time:
        info += "\n"+t.upper()
    info += "\n\n共有 {} 筆資料\n🔔小技巧 : 在以下頁面中\n點按課程名稱👉顯示教學大綱\n點按教師姓名👉顯示教學評價".format(leng)  
    return info
def print_key_cat(leng,cat):
    info = "課程類別:\n{}\n\n共有 {} 筆資料\n🔔小技巧 : 在以下頁面中\n點按課程名稱👉顯示教學大綱\n點按教師姓名👉顯示教學評價".format(cat,leng)
    return info


def print_result(result):
    resultt=[]
    for i in result:
        
        resultt.append(i['subnam'])
        resultt.append(i['teanam'])
        resultt.append("http://newdoc.nccu.edu.tw/teaschm/1101/statisticAll.jsp-tnum={}.htm".format(i['teanum']))
        #print("學 分 數: ",i['subpoint'])
        #print("上課地點: ",i['subclassroom'])
        #print("  ",i['subclassroom'][:2],":"," http://classroom.nccu.edu.tw/work/buildingtable.php?bdnumber={}".format(i['subclassroom'][-6:-3]))
        #print("   教室 :"," http://classroom.nccu.edu.tw/work/detail.php?number={}".format(i['subclassroom'][-6:]))
        #print("授課語言: ",i['langtpe'])
        #print("開課單位: ",i['subgde'])
        #print("必 選 修: ",i['tpe3'])
        #print("核心通識: ",i['core'])
        #print("異動資訊: ",i['info'].split(":")[1])
        #print("備    註: ",i['note'].split(":")[1])
        #print("通識類別: ",i['lmtkindchi'])
        resultt.append("http://newdoc.nccu.edu.tw/teaschm/{}{}/schmPrv.jsp-yy={}&smt={}&num={}&gop={}&s={}.html".format(i['y'],i['s'],i['y'],i['s'],i['subnum'][0:6],i['subnum'][6:8],i['subnum'][8]))
        resultt.append('{} {} {}'.format(i['subctime'],i['tpe3'],i['subpoint']))
        resultt.append(i['subnum'])
    return resultt




def sp_course(search,time):
    result = []
    if len(time) == 0:
        if '語文' in search:
            for i in data:
                if i['lmtkindchi'] == '中文通識' or i['lmtkindchi'] == '外文通識':
                    result.append(i)
            info = print_key_cat(len(result),'語文通識(中文+外文)')
        elif '中文' in search:
            for i in data:
                if i['lmtkindchi'] == '中文通識':
                    result.append(i)
            info = print_key_cat(len(result),'中文通識')
        elif '外文' in search:
            for i in data:
                if i['lmtkindchi'] == '外文通識':
                    result.append(i)
            info = print_key_cat(len(result),'外文通識')
        elif '人文' in search:
            flag = True
            if '核' in search:
                flag=False
            for i in data:
                if '人文' in i['lmtkindchi'] and (i['core'] == '是' or flag):
                    result.append(i)
            if flag:
                info = print_key_cat(len(result),'人文通識')
            else:
                info = print_key_cat(len(result),'人文核心通識')
        elif '自然' in search:
            flag = True
            if '核' in search:
                flag=False
            for i in data:
                if '自然' in i['lmtkindchi'] and (i['core'] == '是' or flag):
                    result.append(i)
            if flag:
                info = print_key_cat(len(result),'自然通識')
            else:
                info = print_key_cat(len(result),'自然核心通識')
        elif '社會' in search:
            flag = True
            if '核' in search:
                flag=False
            for i in data:
                if '社會' in i['lmtkindchi'] and (i['core'] == '是' or flag):
                    result.append(i)
            if flag:
                info = print_key_cat(len(result),'社會通識')
            else:
                info = print_key_cat(len(result),'社會核心通識')
        elif '資訊' in search:
            flag = True
            for i in data:
                if '資訊' in i['lmtkindchi']:
                    result.append(i)
            info = print_key_cat(len(result),'資訊通識')
        elif '一般' in search:
            for i in data:
                if '社會' in i['lmtkindchi'] or '自然' in i['lmtkindchi'] or '人文' in i['lmtkindchi'] or '資訊' in i['lmtkindchi'] or '跨領域' in i['lmtkindchi']:
                    result.append(i)
            info = print_key_cat(len(result),'一般通識(自然+人文+社會+資訊)')
        elif '跨領域' in search:
            for i in data:
                if '跨領域' in i['lmtkindchi']:
                    result.append(i)
            info = print_key_cat(len(result),'跨領域通識')
        else:
            flag = True
            if '核' in search:
                flag=False
            for i in data:
                if ('通識' in i['lmtkindchi'] or '跨領域' in i['lmtkindchi']) and (i['core'] == '是' or flag):
                    result.append(i)
            if flag:
                info = print_key_cat(len(result),'通識(自然+人文+社會+資訊+中文+外文)')
            else:
                info = print_key_cat(len(result),'核心通識(自然+人文+社會)')
    else:
        text=[]
        for i in time:
            text.append("{}[{}]+(?=[一二三四五六日]|$)".format(i[0],i[1:].upper()))
        ress = '|'.join(text)
        cotime = re.compile(ress)
        if '語文' in search:
            for i in data:
                if (i['lmtkindchi'] == '中文通識' or i['lmtkindchi'] == '外文通識') and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i) 
            info = print_key_cat_time(len(result),'語文通識(中文+外文)',time)
        elif '中文' in search:
            for i in data:
                if i['lmtkindchi'] == '中文通識' and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            info = print_key_cat_time(len(result),'中文通識',time)
        elif '外文' in search:
            for i in data:
                if i['lmtkindchi'] == '外文通識' and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            info = print_key_cat_time(len(result),'外文通識',time)
        elif '人文' in search:
            flag = True
            if '核' in search:
                flag=False
            for i in data:
                if '人文' in i['lmtkindchi'] and (i['core'] == '是' or flag) and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            if flag:
                info = print_key_cat_time(len(result),'人文通識',time)
            else:
                info = print_key_cat_time(len(result),'人文核心通識',time)
        elif '自然' in search:
            flag = True
            if '核' in search:
                flag=False
            for i in data:
                if '自然' in i['lmtkindchi'] and (i['core'] == '是' or flag) and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            if flag:
                info = print_key_cat_time(len(result),'自然通識',time)
            else:
                info = print_key_cat_time(len(result),'自然核心通識',time)
        elif '社會' in search:
            flag = True
            if '核' in search:
                flag=False
            for i in data:
                if '社會' in i['lmtkindchi'] and (i['core'] == '是' or flag) and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            if flag:
                info = print_key_cat_time(len(result),'社會通識',time)
            else:
                info = print_key_cat_time(len(result),'社會核心通識',time)
        elif '資訊' in search:
            flag = True
            for i in data:
                if '資訊' in i['lmtkindchi'] and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            info = print_key_cat_time(len(result),'資訊通識',time)
        elif '一般' in search:
            for i in data:
                if ('社會' in i['lmtkindchi'] or '自然' in i['lmtkindchi'] or '人文' in i['lmtkindchi'] or '資訊' in i['lmtkindchi'] or '跨領域' in i['lmtkindchi']) and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            info = print_key_cat_time(len(result),'一般通識(自然+人文+社會+資訊)',time)
        elif '跨領域' in search:
            for i in data:
                if '跨領域' in i['lmtkindchi'] and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            info = print_key_cat_time(len(result),'跨領域通識',time)            
        else:
            flag = True
            if '核' in search:
                flag=False
            for i in data:
                if ('通識' in i['lmtkindchi'] or '跨領域' in i['lmtkindchi']) and (i['core'] == '是' or flag) and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            if flag:
                info = print_key_cat_time(len(result),'通識(自然+人文+社會+資訊+中文+外文)',time)
            else:
                info = print_key_cat_time(len(result),'核心通識(自然+人文+社會)',time)
    return [info,result]




def search_co(search):
    gde=""
    tea=False
    if "軍訓" in search:
        search = search.replace("軍訓","軍事訓練")
    time = re.findall('[一,二,三,四,五,六,日][1-8a-hA-H]+',search)
    is_cate = False
    category = ['中文通識','中文通',
                '外文通','外文通識',
                '語文通識', 
                '人文核','人文通識','人文核通','人文通','人文核心通識',
                '自然核','自然通識','自然核通','自然通','自然核心通識',
                '社會核','社會通識','社會核通','社會通','社會核心通識',
                '資訊通識','資訊通',
                '核心通識','核通','一般通識','一般通','通識課程','通識','跨領域','跨領域通識']
    for w in category:
        if w in search:
            is_cate=True
            break
    result = []
    if search =="":
        info = "查無課程資訊, 請重新輸入" 
    elif is_cate:
        tmp = sp_course(search,time)
        info = tmp[0]
        result = tmp[1]
    elif len(time)==0:
        subject = search.strip(" ")
        for i in data:
            if subject in i['subnam']:
                result.append(i)
            if subject in i['subgde']:
                gde=subject
            if subject in i['teanam']:
                tea=True
        info = "課程名稱:\n{}\n\n共有 {} 筆資料\n🔔小技巧 : 在以下頁面中\n點按課程名稱👉顯示教學大綱\n點按教師姓名👉顯示教學評價".format(subject,len(result))
    else:
        subject1 = search.split(time[0])[0].strip(" ")
        subject2 = search.split(time[-1])[1].strip(" ")
        text=[]
        for i in time:
            text.append("{}[{}]+(?=[一二三四五六日]|$)".format(i[0],i[1:].upper()))
        ress = '|'.join(text)
        cotime = re.compile(ress)
        if subject1=="" and subject2=="":
            for i in data:
                if cotime.search(i['subctime'])!=None:
                    result.append(i)
            info = "時間:(僅列出包含於以下時段的課程)"
            for t in time:
                info += "\n"+t.upper()
            info += "\n\n共有 {} 筆資料\n🔔小技巧 : 在以下頁面中\n點按課程名稱👉顯示教學大綱\n點按教師姓名👉顯示教學評價".format(len(result))  
        else:
            for i in data:
                if ((subject1 in i['subnam'] and subject1 != "") or (subject2 in i['subnam'] and subject2 != "")) and (cotime.search(i['subctime'])!=None or i['subctime']=='未定或彈性'):
                    result.append(i)
            info = "課程名稱:\n{} {}\n\n時間:(僅列出包含於以下時段的課程)".format(subject1,subject2)
            for t in time:
                info += "\n"+t.upper()
            info += "\n\n共有 {} 筆資料\n🔔小技巧 : 在以下頁面中\n點按課程名稱👉顯示教學大綱\n點按教師姓名👉顯示教學評價".format(len(result))  
    resultt = print_result(result)

    return [info,resultt,gde,tea]  
def flexm(output,npage):
    output[1]=output[1][((npage-1)*300):]
    aa={
      "type": "carousel",
      "contents": []
        }
    counter = 0
    if len(output[1])/6/5%1==0:
        num_of_page = int(len(output[1])/6/5)
    else:
        num_of_page = int(len(output[1])/6/5)+1
    more = False
    if num_of_page>10:
        more = True
        num_of_page=10
    for i in range(num_of_page):
        cc= {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "spacing": "lg"
            }
        }
        for t in range(5):
            if counter==len(output[1])/6:
                break
            if 'False' in output[1][(counter*6)+2]:
                cc["body"]["contents"].append(
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "text",
                                    "text": output[1][counter*6],
                                    "weight": "bold",
                                    "style": "normal",
                                    "action": {
                                      "type": "uri",
                                      "label": "action",
                                      "uri": output[1][(counter*6)+3]
                                    },
                                    "wrap": True,
                                  },
                                  {
                                    "type": "text",
                                    "text": output[1][(counter*6)+1],
                                    "color": "#757575",
                                    "action": {
                                      "type": "postback",
                                      "data": "teamorefromnet&0&"+output[1][(counter*6)+1]
                                    },
                                    "wrap": True,
                                  },
                                  {
                                    "type": "text",
                                    "text": output[1][(counter*6)+4],
                                    "color": "#757575",
                                    
                                  } 
                                ],
                                "spacing": "sm",
                                "flex": 2,
                              },
                              {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                              {
                                "type": "button",
                                "action": {
                                  "type": "postback",
                                  "label": "Detail",
                                  "data": '{}&{}'.format(npage,output[1][(counter*6)+5])
                                },
                                "color": "#5edfff",
                                "style": "primary",
                                "height": "sm"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "postback",
                                  "label": "收藏",
                                  "data": 'save&{}'.format(output[1][(counter*6)+5])
                                },
                                "color": "#ffa0d2",
                                "style": "primary",
                                "height": "sm"
                              }],
                                "flex": 1
                              }
                            ]
                          },
                        )
            else:
                cc["body"]["contents"].append(
                              {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": output[1][counter*6],
                                        "weight": "bold",
                                        "style": "normal",
                                        "action": {
                                          "type": "uri",
                                          "label": "action",
                                          "uri": output[1][(counter*6)+3]
                                        },
                                        "wrap": True,
                                      },
                                      {
                                        "type": "text",
                                        "text": output[1][(counter*6)+1],
                                        "color": "#757575",
                                        "action": {
                                          "type": "uri",
                                          "label": "action",
                                          "uri": output[1][(counter*6)+2],
                                        },
                                        "wrap": True,
                                      },
                                      {
                                        "type": "text",
                                        "text": output[1][(counter*6)+4],
                                        "color": "#757575",
                                        
                                      } 
                                    ],
                                    "spacing": "sm",
                                    "flex": 2,
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                  {
                                    "type": "button",
                                    "action": {
                                      "type": "postback",
                                      "label": "Detail",
                                      "data": '{}&{}'.format(npage,output[1][(counter*6)+5])
                                    },
                                    "color": "#5edfff",
                                    "style": "primary",
                                    "height": "sm"
                                  },
                                  {
                                    "type": "button",
                                    "action": {
                                      "type": "postback",
                                      "label": "收藏",
                                      "data": 'save&{}'.format(output[1][(counter*6)+5])
                                    },
                                    "color": "#ffa0d2",
                                    "style": "primary",
                                    "height": "sm"
                                  }],
                                    "flex": 1
                                  }
                                ]
                              },
                            )
            if (counter+1)%5!=0 and counter+1!=len(output[1])/6:
                cc["body"]["contents"].append(      {
                        "type": "separator"
                      })

            counter+=1
        aa["contents"].append(cc)
    return [aa,more]                

def detailinfo(num):
    num = num.split('&')[1]
    for i in data:
        if num==i['subnum']:
            break

    result=[]    
    result.append(i['subnam'])
    result.append(i['subnum'])
    result.append(i['teanam'])
    result.append('{}'.format(i['subctime']))
    result.append(i['subpoint'])
    result.append(i['subclassroom'])
    result.append(i['langtpe'])
    result.append(i['subgde'])
    result.append(i['tpe3'])
    result.append(i['core'])
    result.append(i['lmtkindchi'])
    result.append(i['note'].split("＠備註:")[1])
    result.append(i['info'].split("＠異動資訊:")[1])
    result.append("http://newdoc.nccu.edu.tw/teaschm/{}{}/schmPrv.jsp-yy={}&smt={}&num={}&gop={}&s={}.html".format(i['y'],i['s'],i['y'],i['s'],i['subnum'][0:6],i['subnum'][6:8],i['subnum'][8]))
    result.append("http://newdoc.nccu.edu.tw/teaschm/1101/statisticAll.jsp-tnum={}.htm".format(i['teanum']))
    result.append("https://selectcourse.nccu.edu.tw/remain/genDetail.aspx?course={}".format(i['subnum']))
    #result.append("http://classroom.nccu.edu.tw/work/buildingtable.php?bdnumber={}".format(i['subclassroom'][-6:-3]))
    result.append(i['subseturl'])
    result.append(i['pay'])
    result.append(i['smtQty'])
    result.append(i['gdeTpe']) 
    result.append(i['tranTpe']) 
    output={
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": result[0],
                    "size": "lg",
                    "weight": "bold",
                    "contents": [],
                    "wrap": True,
                    "color": "#393e46"
                  },
                  {
                    "type": "text",
                    "text": "科目代碼: {}".format(result[1]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "教師姓名: {}".format(result[2]),
                    "color": "#0984e3",
                    "size": "md",
                    "wrap": True,
                  },
                  {
                    "type": "text",
                    "text": "上課時間: {}".format(result[3]),
                    "color": "#0984e3",
                    "size": "md",
                    "wrap": True,
                  },
                  {
                    "type": "text",
                    "text": " 學 分 數 : {}".format(result[4]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "上課地點: {}".format(result[5]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "開課單位: {}".format(result[7]),
                    "color": "#0984e3",
                    "size": "md",
                    "wrap": True,
                  },
                  {
                    "type": "text",
                    "text": "必/選修別: {}".format(result[8]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "separator"
                  },
                  {
                    "type": "text",
                    "text": "授課語言: {}".format(result[6]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "核心通識: {}".format(result[9]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "通識類別: {}".format(result[10]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "收費: {}".format(result[17]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "得充抵通識: {}".format(result[19]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "選課方式: {}".format(result[20]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "[{}]".format(result[18]),
                    "color": "#0984e3",
                    "size": "md"
                  },
                  {
                    "type": "separator"
                  },
                  {
                    "type": "text",
                    "text": "備註: ",
                    "color": "#00adb5",
                    "size": "md"
                  },
                  {
                    "type": "text",
                    "text": "{}\n{}".format(result[11],result[12]),
                    "color": "#000000",
                    "wrap": True
                  }
                ],
                "spacing": "md"
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "button",
                        "action": {
                          "type": "uri",
                          "label": "課程大綱",
                          "uri": result[13]
                        },
                        "style": "primary",
                        "color": "#64c4ed",
                        "height": "sm"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "uri",
                          "label": "教師評價",
                          "uri": result[14]
                        },
                        "color": "#64c4ed",
                        "style": "primary",
                        "height": "sm"
                      }
                    ],
                    "spacing": "md"
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "button",
                        "action": {
                          "type": "uri",
                          "label": "選課餘額",
                          "uri": result[15]
                        },
                        "style": "primary",
                        "color": "#64c4ed",
                        "height": "sm"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "uri",
                          "label": "選課設定",
                          "uri": result[16]
                        },
                        "color": "#64c4ed",
                        "style": "primary",
                        "height": "sm"
                      }
                    ],
                    "spacing": "md"
                  },
                  {
                    "type": "button",
                    "action": {
                    "type": "postback",
                    "label": "收藏課程❤️",
                    "data": 'save&{}'.format(result[1]),
                  },
                    "gravity": "center",
                    "color": "#ffa0d2",
                    "style": "primary",
                    "height": "sm"
                  }
                ],
                "spacing": "md"
              }
            }
    if 'False' in result[14]:
        output['footer']['contents'][0]['contents'][1].update({"action": {
                                            "type": "postback",
                                            "label": "教師評價",
                                            "data": "teamorefromnet&0&"+result[2]
                                        }})
    return output

def search_num(search):
    result=[]
    for i in data:
        if i['subnum'] in search:
            result.append(i)
    resultt = print_result(result)

    return [1,resultt]  
def flexm_num(output,npage):
    if(len(output[1])>((npage-1)*300)):
        output[1]=output[1][((npage-1)*300):]
    aa={
      "type": "carousel",
      "contents": []
        }
    counter = 0
    if len(output[1])/6/5%1==0:
        num_of_page = int(len(output[1])/6/5)
    else:
        num_of_page = int(len(output[1])/6/5)+1
    more = False
    if num_of_page>10:
        more = True
        num_of_page=10
    for i in range(num_of_page):
        cc= {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "spacing": "lg"
            }
        }
        for t in range(5):
            if counter==len(output[1])/6:
                break
            if 'False' in output[1][(counter*6)+2]:
                cc["body"]["contents"].append(
                              {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": output[1][(counter*6)+5],
                                    
                                      },                                    
                                      {
                                        "type": "text",
                                        "text": output[1][counter*6],
                                        "weight": "bold",
                                        "style": "normal",
                                        "action": {
                                          "type": "uri",
                                          "label": "action",
                                          "uri": output[1][(counter*6)+3]
                                        },
                                        "wrap": True,
                                      },
                                      {
                                        "type": "text",
                                        "text": output[1][(counter*6)+1],
                                        "color": "#757575",
                                        "action": {
                                            "type": "postback",
                                            "data": "teamorefromnet&0&"+output[1][(counter*6)+1]
                                        },
                                        "wrap": True,
                                      },
                                      {
                                        "type": "text",
                                        "text": output[1][(counter*6)+4],
                                        "color": "#757575",
                                        
                                      } 
                                    ],
                                    "spacing": "sm",
                                    "flex": 2,
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                  {
                                    "type": "button",
                                    "action": {
                                      "type": "postback",
                                      "label": "Detail",
                                      "data": '{}&{}'.format(npage,output[1][(counter*6)+5])
                                    },
                                    "color": "#5edfff",
                                    "style": "primary",
                                    "height": "sm"
                                  },
                                  {
                                    "type": "button",
                                    "action": {
                                      "type": "postback",
                                      "label": "刪除",
                                      "data": 'delete&{}&{}'.format(output[1][(counter*6)+5],output[1][counter*6]+output[1][(counter*6)+1]+output[1][(counter*6)+4])
                                    },
                                    "color": "#f35588",
                                    "style": "primary",
                                    "height": "sm"
                                  }
                                  ],
                                  "spacing": "sm",
                                    "flex": 1
                                  }
                                ]
                              },
                            )    
            else:
                cc["body"]["contents"].append(
                              {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": output[1][(counter*6)+5],
                                    
                                      },
                                      {
                                        "type": "text",
                                        "text": output[1][counter*6],
                                        "weight": "bold",
                                        "style": "normal",
                                        "action": {
                                          "type": "uri",
                                          "label": "action",
                                          "uri": output[1][(counter*6)+3]
                                        },
                                        "wrap": True,
                                      },
                                      {
                                        "type": "text",
                                        "text": output[1][(counter*6)+1],
                                        "color": "#757575",
                                        "action": {
                                          "type": "uri",
                                          "label": "action",
                                          "uri": output[1][(counter*6)+2],
                                        },
                                        "wrap": True,
                                      },
                                      {
                                        "type": "text",
                                        "text": output[1][(counter*6)+4],
                                        "color": "#757575",
                                        
                                      } 
                                    ],
                                    "spacing": "sm",
                                    "flex": 2,
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                  {
                                    "type": "button",
                                    "action": {
                                      "type": "postback",
                                      "label": "Detail",
                                      "data": '{}&{}'.format(npage,output[1][(counter*6)+5])
                                    },
                                    "color": "#5edfff",
                                    "style": "primary",
                                    "height": "sm"
                                  },
                                  {
                                    "type": "button",
                                    "action": {
                                      "type": "postback",
                                      "label": "刪除",
                                      "data": 'delete&{}&{}'.format(output[1][(counter*6)+5],output[1][counter*6]+output[1][(counter*6)+1]+output[1][(counter*6)+4])
                                    },
                                    "color": "#f35588",
                                    "style": "primary",
                                    "height": "sm"
                                  }
                                  ],
                                  "spacing": "sm",
                                    "flex": 1
                                  }
                                  
                                ]
                              },
                            )
            if (counter+1)%5!=0 and counter+1!=len(output[1])/6:
                cc["body"]["contents"].append(      {
                        "type": "separator"
                      })
            
            counter+=1
        aa["contents"].append(cc)
    return [aa,more] 
def search_time(search):
    result=["",0]
    for i in data:
        if i['subnum'] in search:
            result[0]+=(i['subctime'])
            result[1]+=float(i['subpoint'])
    return result

def search_unit(search):
    result=[]
    for i in data:
        if search in i['subgde']:
            result.append(i)
    resultt = print_result(result)

    return ["開課單位:\n{}\n\n共有 {} 筆資料\n🔔小技巧 : 在以下頁面中\n點按課程名稱👉顯示教學大綱\n點按教師姓名👉顯示教學評價".format(search,len(result)),resultt]  

def search_tea(search):
    result=[]
    for i in data:
        if search in i['teanam']:
            result.append(i)
    resultt = print_result(result)

    return ["授課教師:\n{}\n\n共有 {} 筆資料\n🔔小技巧 : 在以下頁面中\n點按課程名稱👉顯示教學大綱\n點按教師姓名👉顯示教學評價".format(search,len(result)),resultt]  

def search_onlytea(search):
    result=[]
    for i in tdata.keys():
        if search in i:
            result.append(i)
            result.append(tdata[i])
    return [len(result),result]

def flexm_tea(output,npage):
    output[1]=output[1][((npage-1)*100):]
    aa={
      "type": "carousel",
      "contents": []
        }
    counter = 0
    if len(output[1])/2/5%1==0:
        num_of_page = int(len(output[1])/2/5)
    else:
        num_of_page = int(len(output[1])/2/5)+1
    more = False
    if num_of_page>10:
        more = True
        num_of_page=10
    for i in range(num_of_page):
        cc= {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "spacing": "lg"
            }
        }
        for t in range(5):
            if counter==len(output[1])/2:
                break
            if '、' in output[1][(counter*2)+1]:
                cc["body"]["contents"].append(
                          {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "{}".format(output[1][counter*2]),
                                        "weight": "bold",
                                        "size": "xl",
                                        "align": "center"
                                      },
                                      {
                                        "type": "button",
                                        "action": {
                                          "type": "postback",
                                          "label": "教學評價",
                                          "data": "teamorefromnet&0&"+output[1][counter*2]
                                        },
                                        "height": "md",
                                        "color": "#ffd369",
                                        "style": "primary"
                                      }
                                    ],
                                    "spacing": "xs"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "button",
                                        "action": {
                                          "type": "postback",
                                          "label": "Profile",
                                          "data": "teadetail&{}&{}".format(output[1][counter*2],output[1][(counter*2)+1])
                                        },
                                        "height": "sm",
                                        "color": "#5edfff",
                                        "style": "primary"
                                      },
                                      {
                                        "type": "button",
                                        "action": {
                                          "type": "message",
                                          "label": "開課課程",
                                          "text": "{}".format(output[1][counter*2])
                                        },
                                        "height": "sm",
                                        "color": "#50d890",
                                        "style": "primary"
                                      }
                                    ],
                                    "spacing": "sm"
                                  }
                                ],
                                "spacing": "xxl"
                              }
                            ,
                        )
            else:
                cc["body"]["contents"].append(
                              {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "text",
                                            "text": "{}".format(output[1][counter*2]),
                                            "weight": "bold",
                                            "size": "xl",
                                            "align": "center"
                                          },
                                          {
                                            "type": "button",
                                            "action": {
                                              "type": "uri",
                                              "label": "教學評價",
                                              "uri": "http://newdoc.nccu.edu.tw/teaschm/1101/statisticAll.jsp-tnum={}.htm".format(output[1][(counter*2)+1])
                                            },
                                            "height": "md",
                                            "color": "#ffd369",
                                            "style": "primary"
                                          }
                                        ],
                                        "spacing": "xs"
                                      },
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "button",
                                            "action": {
                                              "type": "postback",
                                              "label": "Profile",
                                              "data": "teadetail&{}&{}".format(output[1][counter*2],output[1][(counter*2)+1])
                                            },
                                            "height": "sm",
                                            "color": "#5edfff",
                                            "style": "primary"
                                          },
                                          {
                                            "type": "button",
                                            "action": {
                                              "type": "message",
                                              "label": "開課課程",
                                              "text": "{}".format(output[1][counter*2])
                                            },
                                            "height": "sm",
                                            "color": "#50d890",
                                            "style": "primary"
                                          }
                                        ],
                                        "spacing": "sm"
                                      }
                                    ],
                                    "spacing": "xxl"
                                  }
                                ,
                            )
            if (counter+1)%5!=0 and counter+1!=len(output[1])/2:
                cc["body"]["contents"].append(      {
                        "type": "separator"
                      })

            counter+=1
        aa["contents"].append(cc)
    return [aa,more]
def teadetail(name,website,unit,title,email,tel,exp):
    template=[]
    template.append(
        {
        "type": "image",
        "url": "https://img.icons8.com/cotton/64/000000/name--v2.png",
        "size": "xxs"
      }
    )
    template.append(
        {
        "type": "separator"
      }
    )
    template.append(
        {
        "type": "text",
        "text": "{}".format(name),
        "weight": "bold",
        "size": "xl",
      }
    )
    template.append(
        {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://img.icons8.com/carbon-copy/100/000000/star.png"
          },
          {
            "type": "text",
            "text": "職稱:",
            "color": "#fe6845"
          }
        ],
        "spacing": "md"
      }
    )
    tmpu=""
    tmpt=""
    for i in range(min(len(unit),len(title))):
        if unit[i] == tmpu and title[i] == tmpt:
            continue
        tmpu=unit[i]
        tmpt=title[i]
        template.append(
        {
        "type": "text",
        "text": "> {} {}".format(unit[i],title[i]),
        "wrap": True
      }
    )
    if len(exp)!=0:
        template.append(
                {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "icon",
                    "url": "https://img.icons8.com/ios/50/000000/strength.png"
                  },
                  {
                    "type": "text",
                    "text": "專長:",
                    "color": "#fe6845"
                  }
                ],
                "spacing": "md"
              }
            )
        for i in exp:
            template.append(
                {
                    "type": "text",
                    "text": "> {}".format(i),
                    "wrap": True,
                }
            )
    if len(tel)!=0:
        template.append(
                {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "icon",
                    "url": "https://img.icons8.com/wired/64/000000/phone-not-being-used.png"
                  },
                  {
                    "type": "text",
                    "text": "分機:",
                    "color": "#fe6845"
                  }
                ],
                "spacing": "md"
              }
            )
        tmp=[]
        for i in tel:
            if i in tmp:
                continue
            tmp.append(i)
            template.append(
                {
                    "type": "text",
                    "text": "> {} (Click to call)".format(i.split('p')[1]),
                    "wrap": True,
                    "action": {
                      "type": "uri",
                      "label": "action",
                      "uri": "{}".format(i)
                    },
                  }
            )

    if len(email)!=0:
        template.append(
            {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://img.icons8.com/ios/64/000000/email-open.png"
              },
              {
                "type": "text",
                "text": "電子郵件:",
                "color": "#fe6845"
              }
            ],
            "spacing": "md"
          }
        )
        tmp=[]
        for i in email:
            if i in tmp:
                continue
            tmp.append(i)
            template.append(
                {
                "type": "text",
                "text": "> {} \n   (Click to send)".format(i),
                "wrap": True,
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": "mailto:{}".format(i)
                },

              }
            )
    if len(website)!=0:
        template.append(
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "icon",
                    "url": "https://img.icons8.com/dotty/100/000000/internet.png"
                  },
                  {
                    "type": "text",
                    "text": "個人網站:",
                    "color": "#46b3e6"
                  }
                ],
                "spacing": "md"
              }
        )
        tmp=[]
        for i in website:
            if i in tmp:
                continue
            tmp.append(i)
            template.append(
                {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "前往",
                  "uri": i
                },
                "height": "sm",
                "style": "primary",
                "color": "#46b3e6"
              }
            )
      

      
    
    return {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": template,
    "spacing": "md"
  }
}
