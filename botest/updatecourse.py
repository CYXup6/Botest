import firebase_admin,os,requests,re,time
from firebase_admin import credentials
from firebase_admin import storage
from django.http import HttpResponse
sessionget=requests.session()
def sendnotify(texti,texto,userid):
	url = "https://notify-api.line.me/api/notify"
	payload = {'message': "{} \n傳送了 :{} \n回應了 :{}".format(userid,texti,texto)}

	headers = {
	  'Content-Type': 'application/x-www-form-urlencoded',
	  'Authorization': 'Bearer z6fZ4QX8RI3fmDJvMMzZs4n5nXj7lZo4BaoR3wLGMzS'
	}
	requests.request("POST", url, headers=headers, data = payload)

try:
	from botest.searchco2 import tdata
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
		sendnotify('#更新教師名單失敗',e,'Server')
try:
    from botest.searchco2 import data
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
		sendnotify('#更新課程清單失敗',e,'Server')

def getnum(name):
	url = 'http://sgnweb.nccu.edu.tw/AddressBook/AddressBook/SearchStaff'
	data2 = {
		'keyword':name
	}
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Content-Length': '26',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Host': 'sgnweb.nccu.edu.tw',
		'Origin':'http://sgnweb.nccu.edu.tw',
		'Referer': 'http://sgnweb.nccu.edu.tw/AddressBook/AddressBook/SearchStaff',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
	}
	return requests.post(url,data=data2,headers=headers)
def update(req):
	try:
		urlpath=req.path.split('/')
		sem=urlpath[2]
		recurl='https://linecourse.herokuapp.com/updatecourse/'+sem+'/'
		if len(urlpath)==3:
			filepath = os.path.join(os.path.dirname(__file__),'processingdata.py') 
			file=open(filepath,'w',encoding='utf-8')
			file.write('[]')
			file.close()
			filepath = os.path.join(os.path.dirname(__file__),'donecourse.py') 
			file=open(filepath,'w',encoding='utf-8')  
			file.write('[]')
			file.close()
			sendnotify('#更新資料開始','#建立暫存檔','Server')
			try:
				requests.get(recurl+'0',timeout=3)
			except:
				pass
		elif len(urlpath)==4:
			numcrawl=urlpath[3] 
			if numcrawl=='finish':
				try: 
					filepath = os.path.join(os.path.dirname(__file__),'donecourse.py') 
					file=open(filepath,'r',encoding='utf-8')
					donedata=eval(file.read())
					file.close()
				except:
					sendnotify('#更新資料失敗','@第'+numcrawl+'筆資料失敗','Server')
				donedata.sort(key = lambda s: s['subnum'])   
				if (not len(firebase_admin._apps)):
					cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
					firebase_admin.initialize_app(cred)
				bucket = storage.bucket('coursecollection-57642.appspot.com')
				blob = bucket.blob('teanum.py')
				blob.upload_from_filename(os.path.join(os.path.dirname(__file__),'teanum.py'))
				
				file = open(os.path.join(os.path.dirname(__file__),'course2.py'),'w',encoding="utf-8")
				file.write('data='+str(donedata))
				file.close()

				if (not len(firebase_admin._apps)):
					cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
					firebase_admin.initialize_app(cred)
				
				bucket = storage.bucket('coursecollection-57642.appspot.com')
				blob = bucket.blob('course.py') 
				blob.upload_from_filename(os.path.join(os.path.dirname(__file__),'course2.py'))
				data=donedata
				sendnotify('#資料更新完成'+time.ctime(),'總課程數:'+str(len(data)),'Server')
			else:
				#sendnotify('#更新資料中...','開始建立暫存檔','Server')
				try:
					filepath = os.path.join(os.path.dirname(__file__),'processingdata.py') 
					file=open(filepath,'r',encoding='utf-8')
					rawdata=eval(file.read())
					file.close()
				except:
					sendnotify('#更新資料失敗','@第'+numcrawl+'筆資料失敗','Server')
				if int(numcrawl) == 28:
					url='https://es.nccu.edu.tw/course/zh-TW/:sem={}%20未定或彈性%20/'.format(sem[-4:])
				elif int(numcrawl) < 28 and int(numcrawl)>=0:
					url='https://es.nccu.edu.tw/course/zh-TW/:sem={}%20:week={}%20:dsec={}%20/'.format(sem[-4:],int(int(numcrawl)/4)+1,int(numcrawl)%4+1)
				#sendnotify('#更新資料中...','開始抓資料','Server')
				res=sessionget.get(url)
				tmpdata=[]
				#sendnotify('#更新資料中...','開始整理資料','Server')
				for i in eval(res.text):
					if i not in rawdata:
						tmpdata.append(i)
						rawdata.append(i)
				#sendnotify('#更新資料中...','開始回存檔案','Server')
				filepath = os.path.join(os.path.dirname(__file__),'processingdata.py') 
				file=open(filepath,'w',encoding='utf-8')
				file.write(str(rawdata))
				file.close()
				filepath = os.path.join(os.path.dirname(__file__),'tmpcourse.py') 
				file=open(filepath,'w',encoding='utf-8')
				file.write(str(tmpdata))
				file.close()
				time.sleep(5) 
				sendnotify('#更新資料中...','#已完成課程'+str(int(numcrawl)+1)+'/29','Server')
				try:
					requests.get(recurl+numcrawl+'/updatea',timeout=3) 
				except:
					pass
		elif len(urlpath)==5:
			numcrawl=urlpath[3]
			key=urlpath[4]
			if key=='updatea': 
				try: 
					filepath = os.path.join(os.path.dirname(__file__),'donecourse.py') 
					file=open(filepath,'r',encoding='utf-8')
					donedata=eval(file.read())
					file.close()
				except:
					sendnotify('#更新資料失敗','@第'+numcrawl+'筆資料失敗','Server')
				try:
					filepath = os.path.join(os.path.dirname(__file__),'tmpcourse.py') 
					file=open(filepath,'r',encoding='utf-8')
					tmpdata=eval(file.read())
					file.close()
				except:
					sendnotify('#更新資料失敗','@第'+numcrawl+'筆資料失敗','Server')
				try:
					filepath = os.path.join(os.path.dirname(__file__),'teanum.py') 
					file=open(filepath,'r',encoding='utf-8')
					tdata=eval(file.read().split('=')[1])
					file.close()
				except:
					sendnotify('#更新資料失敗','@第'+numcrawl+'筆資料失敗','Server')
				noc=0
				for i in tmpdata:
					teanum=False
					if '、' in i['teaNam']:
						for t in i['teaNam'].split('、'):
							try:
								teanum = tdata[t]
								if '、' in teanum:
									teanum=False
								break
							except:
								pass
						if teanum==False:
							for t in i['teaNam'].split('、'):
								if noc<=7:
									time.sleep(0.5)
									try:	
										noc+=1
										raise Exception("學校通訊錄網站失效")
										result = getnum(t).text
										sn = re.findall("(?<=c\" data-name=\").+?(?=\")",result)
										teanum=sn[0][0:6] 
										tdata.update({t:teanum})
										sendnotify('#新增教師:',t+teanum,'Server')
										break
									except:
										teanum=False
										sendnotify('#新增教師(找不到代碼):',i['teaNam'],'Server')
								else:
									teanum=False
									sendnotify('#新增教師(待查詢代碼):',i['teaNam'],'Server')
									break

					else:
						try:
							teanum = tdata[i['teaNam']]
							if '、' in teanum:
								teanum=False
						except:
							if noc<=7:
								time.sleep(0.5)
								try:	
									noc+=1
									raise Exception("學校通訊錄網站失效")
									result = getnum(i['teaNam']).text
									sn = re.findall("(?<=c\" data-name=\").+?(?=\")",result)
									teanum=sn[0][0:6]
									tdata.update({i['teaNam']:teanum})
									sendnotify('#新增教師:',i['teaNam']+teanum,'Server')
								except:
									teanum=False
									sendnotify('#新增教師(找不到代碼):',i['teaNam'],'Server')
							else:
								teanum=False
								sendnotify('#新增教師(待查詢代碼):',i['teaNam'],'Server')
					donedata.append({'y': i['y'],
						 's': i['s'],
						 'subnum': i['subNum'],
						 'subnam': i['subNam'],
						 'teanam': i['teaNam'],
						 'subpoint': i['subPoint'],
						 'subctime': i['subTime'],
						 'subetime': i['subTime'],
						 'subclassroom': i['subClassroom'],
						 'langtpe': i['langTpe'],
						 'subgde': i['subGde'],
						 'tpe3': i['subKind'],
						 'core': i['core'],
						 'info': i['info'],
						 'note': i['note'],
						 'teanum': teanum,
						 'subseturl': i['subSetUrl'],
						 'lmtkindchi': i['lmtKind'],
						 'pay': i['pay'],
						 'smtQty': i['smtQty'],
						 'gdeTpe': i['gdeTpe'],
						 'tranTpe': i['tranTpe'],
						 },
						 )
				filepath = os.path.join(os.path.dirname(__file__),'donecourse.py') 
				file=open(filepath,'w',encoding='utf-8')
				file.write(str(donedata))
				file.close()
				file = open(os.path.join(os.path.dirname(__file__),'teanum.py'),'w',encoding = 'utf8')
				file.write('tdata = '+str(tdata))
				file.close()    
				sendnotify('#更新資料中...','#已完成教師'+str(int(numcrawl)+1)+'/29','Server')
				if int(numcrawl) == 28:
					try:
						requests.get(recurl+'finish',timeout=3)
					except:
						pass
				elif int(numcrawl) < 28 and int(numcrawl)>=0:
					try:
						requests.get(recurl+str(int(numcrawl)+1),timeout=3)
					except:
						pass
		return HttpResponse("Update Completed.")
	except Exception as e:
		sendnotify('#更新過程發生錯誤',e,'Server')
		return HttpResponse("Update Error.")
