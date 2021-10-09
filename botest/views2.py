from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi,WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import FollowEvent,MessageEvent, PostbackEvent,StickerSendMessage,PostbackTemplateAction, TextSendMessage,FlexSendMessage,TemplateSendMessage,MessageTemplateAction,URITemplateAction,ButtonsTemplate
import requests
from bs4 import BeautifulSoup as bs
import re
from botest import database,schedule,quickreply
from botest import searchco2 as searchco
import firebase_admin
from firebase_admin import credentials,firestore
import os
import time
import random

# Create your views here..
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
key = 890118
def sendnotify(texti,texto,userid,event):
	delay=(int(time.time()*1000)-event.timestamp)/1000
	url = "https://notify-api.line.me/api/notify"
	profile = line_bot_api.get_profile(userid)
	payload = {'message': "{} \n(delay:{}s) \n傳送了 :{} \n回應了 :{}".format(profile.display_name,delay,texti,texto)}
	headers = {
	  'Content-Type': 'application/x-www-form-urlencoded',
	  'Authorization': 'Bearer z6fZ4QX8RI3fmDJvMMzZs4n5nXj7lZo4BaoR3wLGMzS'
	}
	requests.request("POST", url, headers=headers, data = payload)
def errorsendnotify(texti,texto,userid):
	url = "https://notify-api.line.me/api/notify"
	payload = {'message': "{} \n傳送了 :{} \n回應了 :{}".format(userid,texti,texto)}

	headers = {
	  'Content-Type': 'application/x-www-form-urlencoded',
	  'Authorization': 'Bearer z6fZ4QX8RI3fmDJvMMzZs4n5nXj7lZo4BaoR3wLGMzS'
	}
	requests.request("POST", url, headers=headers, data = payload)
def wakeup(req):
	return HttpResponse("Server is running...")
def encrypt(src):
    return ''.join([chr(ord(x)^key)for x in src]).encode('utf-8').hex()
def decrypt(src):
    return ''.join([chr(ord(x)^key) for x in bytes.fromhex(src).decode('utf-8')])
def getnum(name):
	url = 'http://sgnweb.nccu.edu.tw/AddressBook/AddressBook/SearchStaff'
	data = {
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
	return requests.post(url,data=data,headers=headers)
def search(req,name):
	try:
		result = getnum(decrypt(name)).text
	except:
		return HttpResponseForbidden()
	teacher=[]
	person={}
	sw = re.findall("(?<=c\" data-name=\").+?(?=\")",result)
	sb = re.findall("(?<=ted\">).+?(?=<\/)",result)
	for i in range(len(sw)):
	    person['name']=sw[i][6:]
	    person['feedback']='http://newdoc.nccu.edu.tw/teaschm/1101/statisticAll.jsp-tnum={}.htm'.format(sw[i][0:6])
	    person['detail1'] = sb[2*i]
	    person['detail2'] = sb[2*i+1]
	    teacher.append(person)
	    person={}
	if len(sw) == 0:
		return HttpResponseForbidden()
	return render(req,"index.html",locals())

@csrf_exempt
def callback(request):
	try:
		if request.method == 'POST':
			signature = request.META['HTTP_X_LINE_SIGNATURE']
			body = request.body.decode('utf-8')
			try:
				events = parser.parse(body, signature)
			except InvalidSignatureError:
				return HttpResponseForbidden()
			except LineBotApiError:
				return HttpResponseBadRequest()

			for event in events:
				if isinstance(event, MessageEvent):
					if event.message.type=='sticker':
						if(random.randint(0,1)):
							pid='11537'
							sid=str(random.randint(52002734,52002773))
						else:
							pid='11538'
							sid=str(random.randint(51626494,51626533))		
						sticker_message = StickerSendMessage(
						    package_id=pid,
						    sticker_id=sid
						)
						line_bot_api.reply_message(event.reply_token, sticker_message)
						sendnotify("#貼圖","#貼圖",event.source.user_id,event)
						return HttpResponse()
					checktime=int(time.time())
					try:
						if int(event.message.text) <=checktime and int(event.message.text)>=checktime-300:
							if (not len(firebase_admin._apps)):
								cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
								firebase_admin.initialize_app(cred)
							db = firestore.client()
							database.removeall(event.source.user_id,db)
							line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='👌成功刪除所有課程')])
							sendnotify(event.message.text,'👌成功刪除所有課程',event.source.user_id,event)
							return HttpResponse()
					except:
						pass
					if event.message.text=='[我的課程清單]':
						if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
						db = firestore.client()
						result = database.get(event.source.user_id,db)
						if(result[0]=='nocourse'):
							line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您未收藏任何課程'))
							sendnotify(event.message.text,'您未收藏任何課程',event.source.user_id,event)
							return HttpResponse()
						output = searchco.search_num(result)
						if(len(output[1])==0):
							line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您未收藏任何課程'))
							sendnotify(event.message.text,'您未收藏任何課程',event.source.user_id,event)
							return HttpResponse()
						flex_content = searchco.flexm_num(output,1)
						if flex_content[1]:
							flex_message = FlexSendMessage(
								alt_text='查詢結果',
								contents=flex_content[0],
								quick_reply={"items": [
									    	quickreply.list_next_page(1),
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    }
							)
						else:
							flex_message = FlexSendMessage(
								alt_text='查詢結果',
								contents=flex_content[0],
								quick_reply={"items": [
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    }
							)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify(event.message.text,'#顯示收藏清單',event.source.user_id,event)
					elif event.message.text=='[教師評價查詢]':		
						text1="[評價查詢功能說明]\n"
						text2="🔎查詢教師評價\n請在姓名前加上@\n範例：「@詹XX」\n(可模糊查詢)"
						flex_message=FlexSendMessage(
							alt_text='查詢結果',
							contents={
							  "type": "bubble",
							  "body": { 
							    "type": "box",
							    "layout": "vertical",
							    "contents": [
							      {
							        "type": "text",
							        "text": "🔗🔗相關資訊🔗🔗",
							        "weight": "bold",
							        "align": "center"
							      },
							      {
							        "type": "button",
							        "action": {
							          "type": "uri",
							          "label": "🔎教師聯絡資訊",
							          "uri": "https://moltke.nccu.edu.tw/staffinfoqry_SSO/query.jsp"
							        },
							        "color": "#49beb7",
							        "style": "primary"
							      }
							    ],
							    "spacing": "md",
							  }
							}
						)
						line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=text1+text2),flex_message])
						sendnotify(event.message.text,'#顯示教師查詢說明',event.source.user_id,event)
					elif event.message.text=='[課程查詢]':		
						text1="[課程查詢功能說明]\n🔎以時間查詢：「五234」、「一12345678」、「二234三5678e四c」...\n(將列出包含於以上時段的課程)\n\n🔎以課程名稱查詢：「經濟學」、「服務」、「體育」、「Economics」...\n\n🔎以課程類別查詢：「人文通」、「核通」、「跨領域」、「自然核」、「中文通識」...\n"
						text2="\n\n⭐以上查詢方式均可搭配時間複合查詢:\n「經濟學五234cd5678」、「核通二567三234」、「一5678ef 自然通」...\n\n🔎以開課系級查詢：「資科一」、「經濟四」、「地政二」...\n\n🔎以授課教師查詢：「銘峰」、「蔡彥」、「郭」、「林」..."
						text3="\n\n🔔提醒: 在查詢結果頁面中,點擊課程名稱或教師姓名,即可顯示課程大綱或教師評價(不須進入detail)"
						flex_message=FlexSendMessage(
							alt_text='查詢結果',
							contents={
							  "type": "bubble",
							  "body": {
							    "type": "box",
							    "layout": "vertical",
							    "contents": [
							      {
							        "type": "text",
							        "text": "🔗🔗相關資訊🔗🔗",
							        "weight": "bold",
							        "align": "center"
							      },
							      {
							        "type": "button",
							        "action": {
							          "type": "uri",
							          "label": "🔎必修科目表查詢",
							          "uri": "https://aca.nccu.edu.tw/zh/%E8%AA%B2%E5%8B%99%E7%B5%84/%E8%AA%B2%E7%A8%8B%E8%B3%87%E8%A8%8A"
							        },
							        "color": "#49beb7",
							        "style": "primary"
							      },
							      {
							        "type": "button",
							        "action": {
							          "type": "uri",
							          "label": "🔎選課資訊",
							          "uri": "https://aca.nccu.edu.tw/zh/%E8%A8%BB%E5%86%8A%E7%B5%84/%E9%81%B8%E8%AA%B2%E8%A8%8A%E6%81%AF/"
							        },
							        "color": "#49beb7",
							        "style": "primary"
							      }
							    ],
							    "spacing": "md",
							  }
							}
						)
						line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=text1+text2+text3),flex_message])
						sendnotify(event.message.text,'#顯示課程查詢說明',event.source.user_id,event)
					elif event.message.text=='[整合課表]':
						if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
						db = firestore.client()
						result = database.get(event.source.user_id,db)
						output = searchco.search_time(result)
						stime = re.findall('[一,二,三,四,五][1-8a-gA-G]+',output[0])
						numlist = {
							"一":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
							"二":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
					        "三":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
				            "四":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
				            "五":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
				        }
						if(result[0]=='nocourse'):
							pass
						else:
							for t in stime:
								for i in t[1:]:
									numlist[t[0]][i]+=1
									if(numlist[t[0]][i]>=10):
										numlist[t[0]][i]=10
						flex_message=FlexSendMessage(
							alt_text='查詢結果',
							contents=schedule.schedule_template(numlist,output[1]),
							quick_reply={"items": [
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    }
						)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify(event.message.text,"#顯示時間分配表",event.source.user_id,event)
					elif event.message.text=='[意見回饋]':		
						text1="[意見回饋]\n若您有任何問題, 請以 $ 為開頭留下您的意見, 範例：「$如何開啟收藏清單」\n或填寫以下問卷"
						flex_message=FlexSendMessage(
							alt_text='查詢結果',
							contents={
							  "type": "bubble",
							  "body": {
							    "type": "box",
							    "layout": "vertical",
							    "contents": [
							      {
							        "type": "text",
							        "text": "🔗🔗相關資訊🔗🔗",
							        "weight": "bold",
							        "align": "center"
							      },
							      {
							        "type": "button",
							        "action": {
							          "type": "uri",
							          "label": "意見調查問卷",
							          "uri": "https://www.surveycake.com/s/8mYYr"
							        },
							        "color": "#49beb7",
							        "style": "primary"
							      },
							    ],
							    "spacing": "md",
							  }
							}
						)
						line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=text1),flex_message])
						sendnotify(event.message.text,'#顯示線上客服',event.source.user_id,event)
					elif event.message.text[0]=='$':		
						text1="已收到您的意見, 謝謝!!"
						line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text1))
						sendnotify(event.message.text,'#客服回覆',event.source.user_id,event)
					elif('@' not in event.message.text):
						output = searchco.search_co((event.message.text).replace('\n',''))
						if len(output[1])==0:
							if output[3]:
								output = searchco.search_tea((event.message.text).replace('\n',''))
								flex_content = searchco.flexm(output,1)
								flex_message = FlexSendMessage(
									alt_text='查詢結果',
									contents=flex_content[0],
								)
								line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=output[0]),flex_message])
								sendnotify(event.message.text,output[0],event.source.user_id,event)
							else:
								if len(output[2])==0:
									line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=output[0])])
									sendnotify(event.message.text,output[0],event.source.user_id,event)
								else:
									line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=output[0],quick_reply={"items": [quickreply.searchby_gde(output[2])]})])
									sendnotify(event.message.text,output[0]+output[2],event.source.user_id,event)
						else:
							flex_content = searchco.flexm(output,1)
							if flex_content[1]:
								flex_content[0]["contents"][0].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
					                            {
					                            "type": "button",
					                            "action": {
					                              "type": "postback",
					                              "label": "↓↓顯示更多課程",
					                              "data": '0&1&{}'.format((event.message.text).replace('\n',''))
					                            },
					                            "style": "primary",
					                            "color": "#905c44",
					            				"height": "sm",

					                          }
					                        ]
					                      }}
									)
								flex_content[0]["contents"][9].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
				                            {
				                            "type": "button",
				                            "action": {
				                              "type": "postback",
				                              "label": "↓↓顯示更多課程",
				                              "data": '0&1&{}'.format((event.message.text).replace('\n',''))
				                            },
				                            "style": "primary",
				                            "color": "#905c44",
				            				"height": "sm",

				                          }
				                        ]
				                      }}
									)
								if len(output[2])!=0:
									flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],
									    quick_reply={"items": [
									    	quickreply.searchby_gde(output[2])
									    	]
									    }
										
								)
								else:
									flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],	
								)
							else:
								if len(output[2])!=0:
									flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],
									    quick_reply={"items": [
									    	quickreply.searchby_gde(output[2])
									    	]
									    }
										
								)
								else:
									flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],
								)
							line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=output[0]),flex_message])
							sendnotify(event.message.text,output[0],event.source.user_id,event)
					elif '@:::::' in event.message.text:
						if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
						db = firestore.client()
						if 'Add' in event.message.text:
							database.update(event.source.user_id,event.message.text.split('Add')[1],db)
						elif 'Delete' in event.message.text:
							database.remove(event.source.user_id,event.message.text.split('Delete')[1],db)
						else:
							result = database.get(event.source.user_id,db)
							resultt = '\n'.join(result)
							line_bot_api.reply_message(event.reply_token, TextSendMessage(text=resultt))
					else:
						output = searchco.search_onlytea((event.message.text).replace('@','')) 
						if output[0]:
							flex_content = searchco.flexm_tea(output,1)
							if flex_content[1]:
								flex_content[0]["contents"][0].update(
										{"footer": {
					                        "type": "box",
					                        "layout": "vertical",
					                        "contents": [
						                            {
						                            "type": "button",
						                            "action": {
						                              "type": "postback",
						                              "label": "↓↓顯示更多教師",
						                              "data": 'teamore&1&{}'.format((event.message.text).replace('@',''))
						                            },
						                            "style": "primary",
						                            "color": "#905c44",
						            				"height": "sm",

						                          }
						                        ]
						                      }}
										)
								flex_content[0]["contents"][9].update(
										{"footer": {
					                        "type": "box",
					                        "layout": "vertical",
					                        "contents": [
					                            {
					                            "type": "button",
					                            "action": {
					                              "type": "postback",
					                              "label": "↓↓顯示更多教師",
					                              "data": 'teamore&1&{}'.format((event.message.text).replace('@',''))
					                            },
					                            "style": "primary",
					                            "color": "#905c44",
					            				"height": "sm",

					                          }
					                        ]
					                      }}
										)
								flex_message = FlexSendMessage(
										    alt_text='查詢結果',
										    contents=flex_content[0],
										    quick_reply={"items": [
									    	quickreply.teafromnet((event.message.text).replace('@',''))
									    	]
									    }
										    
											
									)
							else:
								flex_message = FlexSendMessage(
											    alt_text='查詢結果',
											    contents=flex_content[0],
											    quick_reply={"items": [
									    	quickreply.teafromnet((event.message.text).replace('@',''))
									    	]
									    }
										)
							line_bot_api.reply_message(event.reply_token, flex_message)
							sendnotify(event.message.text,"#顯示教師資訊(有在本學期課表內)",event.source.user_id,event)
						else:
							result = getnum((event.message.text).replace('@','')).text
							sn = re.findall("(?<=c\" data-name=\").+?(?=\")",result)
							if len(sn) == 0:
								line_bot_api.reply_message(event.reply_token, TextSendMessage(text='查無教師資訊,請重新輸入'))
								sendnotify(event.message.text,"#顯示教師資訊(沒有在本學期課表內)(找不到)",event.source.user_id,event)
							else:
								teacher=[]
								output=[]
								repeat=[]
								for i in range(len(sn)):
									if sn[i][6:]+sn[i][0:6] in repeat:
										continue
									teacher.append(sn[i][6:])		
									teacher.append(sn[i][0:6])
									repeat.append(sn[i][6:]+sn[i][0:6])
								output.append(len(teacher))
								output.append(teacher)
								flex_content = searchco.flexm_tea(output,1)
								if flex_content[1]:
									flex_content[0]["contents"][0].update(
											{"footer": {
						                        "type": "box",
						                        "layout": "vertical",
						                        "contents": [
							                            {
							                            "type": "button",
							                            "action": {
							                              "type": "postback",
							                              "label": "↓↓顯示更多教師",
							                              "data": 'teamorefromnet&1&{}'.format((event.message.text).replace('@',''))
							                            },
							                            "style": "primary",
							                            "color": "#905c44",
							            				"height": "sm",

							                          }
							                        ]
							                      }}
											)
									flex_content[0]["contents"][9].update(
											{"footer": {
						                        "type": "box",
						                        "layout": "vertical",
						                        "contents": [
						                            {
						                            "type": "button",
						                            "action": {
						                              "type": "postback",
						                              "label": "↓↓顯示更多教師",
						                              "data": 'teamorefromnet&1&{}'.format((event.message.text).replace('@',''))
						                            },
						                            "style": "primary",
						                            "color": "#905c44",
						            				"height": "sm",

						                          }
						                        ]
						                      }}
											)
									flex_message = FlexSendMessage(
											    alt_text='查詢結果',
											    contents=flex_content[0],
											    
												
										)
								else:
									flex_message = FlexSendMessage(
												    alt_text='查詢結果',
												    contents=flex_content[0],
											)
								
								line_bot_api.reply_message(event.reply_token, flex_message)
								sendnotify(event.message.text,"#顯示教師資訊(沒有在本學期課表內)",event.source.user_id,event)
				if isinstance(event, PostbackEvent):
					if (event.postback.data).split('&')[0] == '0':
						output = searchco.search_co((event.postback.data).split('&')[2])
						flex_content = searchco.flexm(output,int((event.postback.data).split('&')[1])+1)
						if flex_content[1]:
							flex_content[0]["contents"][0].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
					                            {
					                            "type": "button",
					                            "action": {
					                              "type": "postback",
					                              "label": "↓↓顯示更多課程",
					                              "data": '0&{}&{}'.format(int((event.postback.data).split('&')[1])+1,(event.postback.data).split('&')[2])
					                            },
					                            "style": "primary",
					                            "color": "#905c44",
					            				"height": "sm",

					                          }
					                        ]
					                      }}
									)
							flex_content[0]["contents"][9].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
				                            {
				                            "type": "button",
				                            "action": {
				                              "type": "postback",
				                              "label": "↓↓顯示更多課程",
				                              "data": '0&{}&{}'.format(int((event.postback.data).split('&')[1])+1,(event.postback.data).split('&')[2])
				                            },
				                            "style": "primary",
				                            "color": "#905c44",
				            				"height": "sm",

				                          }
				                        ]
				                      }}
									)
							flex_message = FlexSendMessage(
						    alt_text='查詢結果',
						    contents=flex_content[0],
							)
						else:
							flex_message = FlexSendMessage(
						    alt_text='查詢結果',
						    contents=flex_content[0],
							)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify("#點擊 ↓↓顯示更多課程","#顯示 "+(event.postback.data).split('&')[2]+" 的第"+str(int((event.postback.data).split('&')[1])+1)+"頁",event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'list':
						if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
						db = firestore.client()
						result = database.get(event.source.user_id,db)
						if(result[0]=='nocourse'):
							line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您未加入任何課程'))
							sendnotify("#點擊 收藏清單的下一頁",'您未加入任何課程',event.source.user_id,event)
							return HttpResponse()
						output = searchco.search_num(result)
						if(len(output[1])==0):
							line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您未加入任何課程'))
							sendnotify("#點擊 收藏清單的下一頁",'您未加入任何課程',event.source.user_id,event)
							return HttpResponse()
						flex_content = searchco.flexm_num(output,int((event.postback.data).split('&')[1])+1)
						if flex_content[1]:
							flex_message = FlexSendMessage(
							    alt_text='查詢結果',
							    contents=flex_content[0],
							    quick_reply={"items": [
									    	quickreply.list_next_page(int((event.postback.data).split('&')[1])+1),
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    }
							)
						else:
							flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],
									    quick_reply={"items": [
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    }
									    
										
							)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify("#點擊 收藏清單的下一頁",'#顯示下一頁',event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'delete':
						if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
						db = firestore.client()
						database.remove(event.source.user_id,event.postback.data.split('&')[1],db)
						line_bot_api.reply_message(event.reply_token, TextSendMessage(text='成功刪除課程#'+event.postback.data.split('&')[2],quick_reply={"items": [
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    }))
						sendnotify("#點擊 刪除",'成功刪除課程#'+event.postback.data.split('&')[2],event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'save':
						if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
						db = firestore.client()
						database.update(event.source.user_id,event.postback.data.split('&')[1],db)
						line_bot_api.reply_message(event.reply_token, TextSendMessage(text='成功加入課程#'+event.postback.data.split('&')[1]))
						sendnotify("#點擊 收藏",'成功加入課程#'+event.postback.data.split('&')[1],event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'code':
						if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
						db = firestore.client()
						result = database.get(event.source.user_id,db)
						if(result[0]=='nocourse'):
							line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您未加入任何課程'))
							sendnotify("#點擊 輸出課程代碼",'您未加入任何課程',event.source.user_id,event)
							return HttpResponse()
						resultt = '\n'.join(result)
						text="🔔將以下課程代碼複製, 並貼在選課系統內的登記清單, 即可完成選課登記👍 \n\n👇選課系統👇\nhttps://selectcourse.nccu.edu.tw/regcourse/"
						line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=text),TextSendMessage(text=resultt,quick_reply={"items": [
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    })])
						sendnotify("#點擊 輸出課程代碼",resultt,event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'delall':
						password=int(time.time())
						line_bot_api.reply_message(event.reply_token, TextSendMessage(text='⚠️輸入 '+ str(password) +"\n以刪除所有收藏課程\n(5分鐘內有效)",quick_reply={"items": [
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    }))
						sendnotify("#點擊 刪除所有課程",'⚠️輸入 '+ str(password) +"\n以刪除所有收藏課程\n(5分鐘內有效)",event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'sche':
						if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
						db = firestore.client()
						result = database.get(event.source.user_id,db)
						output = searchco.search_time(result)
						stime = re.findall('[一,二,三,四,五][1-8a-gA-G]+',output[0])
						numlist = {
							"一":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
							"二":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
					        "三":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
				            "四":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
				            "五":{"A":0,"B":0,"1":0,"2":0,"3":0,"4":0,"C":0,"D":0,"5":0,"6":0,"7":0,"8":0,"E":0,"F":0,"G":0},
				        }
						if(result[0]=='nocourse'):
							pass
						else:
							for t in stime:
								for i in t[1:]:
									numlist[t[0]][i]+=1
									if(numlist[t[0]][i]>=10):
										numlist[t[0]][i]=10
						flex_message=FlexSendMessage(
							alt_text='查詢結果',
							contents=schedule.schedule_template(numlist,output[1]),
							quick_reply={"items": [
									    	quickreply.fav_option1,
									    	quickreply.fav_option2,
									    	quickreply.fav_option3
									    	]
									    }
						)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify("#點擊 顯示時間分配表","#顯示時間分配表",event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'gde':
						output = searchco.search_unit((event.postback.data).split('&')[1])
						flex_content = searchco.flexm(output,1)
						if flex_content[1]:
							flex_content[0]["contents"][0].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
					                            {
					                            "type": "button",
					                            "action": {
					                              "type": "postback",
					                              "label": "↓↓顯示更多課程",
					                              "data": 'gdemore&1&{}'.format((event.postback.data).split('&')[1])
					                            },
					                            "style": "primary",
					                            "color": "#905c44",
					            				"height": "sm",

					                          }
					                        ]
					                      }}
									)
							flex_content[0]["contents"][9].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
				                            {
				                            "type": "button",
				                            "action": {
				                              "type": "postback",
				                              "label": "↓↓顯示更多課程",
				                              "data": 'gdemore&1&{}'.format((event.postback.data).split('&')[1])
				                            },
				                            "style": "primary",
				                            "color": "#905c44",
				            				"height": "sm",

				                          }
				                        ]
				                      }}
									)
							flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],
									    
										
								)
						else:
							flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],
								)
						line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=output[0]),flex_message])
						sendnotify("#點擊 想以開課單位"+(event.postback.data).split('&')[1]+"查詢",output[0],event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'gdemore':
						output = searchco.search_unit((event.postback.data).split('&')[2])
						flex_content = searchco.flexm(output,int((event.postback.data).split('&')[1])+1)
						if flex_content[1]:
							flex_content[0]["contents"][0].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
					                            {
					                            "type": "button",
					                            "action": {
					                              "type": "postback",
					                              "label": "↓↓顯示更多課程",
					                              "data": 'gdemore&{}&{}'.format(int((event.postback.data).split('&')[1])+1,(event.postback.data).split('&')[2])
					                            },
					                            "style": "primary",
					                            "color": "#905c44",
					            				"height": "sm",

					                          }
					                        ]
					                      }}
									)
							flex_content[0]["contents"][9].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
				                            {
				                            "type": "button",
				                            "action": {
				                              "type": "postback",
				                              "label": "↓↓顯示更多課程",
				                              "data": 'gdemore&{}&{}'.format(int((event.postback.data).split('&')[1])+1,(event.postback.data).split('&')[2])
				                            },
				                            "style": "primary",
				                            "color": "#905c44",
				            				"height": "sm",

				                          }
				                        ]
				                      }}
									)
							flex_message = FlexSendMessage(
							    alt_text='查詢結果',
							    contents=flex_content[0],
							)
						else:
							flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],
									    
										
							)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify("#點擊 ↓↓顯示更多課程(開課單位)","#顯示更多課程",event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'teamore':
						output = searchco.search_onlytea((event.postback.data).split('&')[2])
						flex_content = searchco.flexm_tea(output,int((event.postback.data).split('&')[1])+1)
						if flex_content[1]:
							flex_content[0]["contents"][0].update(
										{"footer": {
					                        "type": "box",
					                        "layout": "vertical",
					                        "contents": [
						                            {
						                            "type": "button",
						                            "action": {
						                              "type": "postback",
						                              "label": "↓↓顯示更多教師",
						                              "data": 'teamore&{}&{}'.format(int((event.postback.data).split('&')[1])+1,(event.postback.data).split('&')[2])
						                            },
						                            "style": "primary",
						                            "color": "#905c44",
						            				"height": "sm",

						                          }
						                        ]
						                      }}
										)
							flex_content[0]["contents"][9].update(
										{"footer": {
					                        "type": "box",
					                        "layout": "vertical",
					                        "contents": [
					                            {
					                            "type": "button",
					                            "action": {
					                              "type": "postback",
					                              "label": "↓↓顯示更多教師",
					                              "data": 'teamore&{}&{}'.format(int((event.postback.data).split('&')[1])+1,(event.postback.data).split('&')[2])
					                            },
					                            "style": "primary",
					                            "color": "#905c44",
					            				"height": "sm",

					                          }
					                        ]
					                      }}
										)
							flex_message = FlexSendMessage(
										    alt_text='查詢結果',
										    contents=flex_content[0],
										    
											
									)
						else:
							flex_message = FlexSendMessage(
											    alt_text='查詢結果',
											    contents=flex_content[0],
										)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify("#點擊 ↓↓顯示更多教師","#顯示更多教師",event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'teadetail':
						exp=[]
						try:
							expurl="http://newdoc.nccu.edu.tw/teaschm/teaexp/teaExp.jsp-tnum={}.htm".format((event.postback.data).split('&')[2])
							expreq=requests.get(expurl)
							expreq.encoding="big5"
							exp=re.findall(r"(?<=<tr><td>).+?(?=[^、\u4E00-\u9FFF])",expreq.text)[0].split("、")
						except:
							pass
						"""teaurl="https://moltke.nccu.edu.tw/staffinfoqry_SSO/query.staffinfoqry"
						teareq=requests.session()
						teadata={
						    "unit":"",
						    "unit-search":"",
						    "qrystr":"{}".format((event.postback.data).split('&')[1])
						}
						result=teareq.get(url=teaurl)
						result=teareq.post(url=teaurl,data=teadata)
						teacontent=result.text
						nameTmp=re.findall(r"(?<=name\">)\s*.+\s*(?=<)",teacontent) 
						try:
							name=re.findall(r"[^\s]+",nameTmp[0])
						except:
							line_bot_api.reply_message(event.reply_token, TextSendMessage(text='查無教師資訊'))
							sendnotify("#點擊 教師資訊detail","查無教師資訊({})".format((event.postback.data).split('&')[1]),event.source.user_id,event)
							return HttpResponse()"""
						teacontent=""
						website=re.findall(r"(?<=<a href=\").+?(?=\" class=\"website\")",teacontent)
						unit=re.findall(r"(?<=相關資訊\">).+(?=<)",teacontent)
						title=re.findall(r"(?<=title\">).+?(?=<)",teacontent)
						email=re.findall(r"(?<=mailto:).+?(?=\")",teacontent)
						tel=re.findall(r"tel:0229393091p[0-9]+",teacontent)
						flex_message = FlexSendMessage(
										    alt_text='查詢結果',
										    contents=searchco.teadetail((event.postback.data).split('&')[1],website,unit,title,email,tel,exp),
										    
											
									)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify("#點擊 教師資訊detail","顯示教師資訊({})".format((event.postback.data).split('&')[1]),event.source.user_id,event)
						return HttpResponse()
					if (event.postback.data).split('&')[0] == 'teamorefromnet':
						result = getnum((event.postback.data).split('&')[2]).text
						sn = re.findall("(?<=c\" data-name=\").+?(?=\")",result)
						teacher=[]
						output=[]
						repeat=[]
						for i in range(len(sn)):
							if sn[i][6:]+sn[i][0:6] in repeat:
								continue
							teacher.append(sn[i][6:])		
							teacher.append(sn[i][0:6])
							repeat.append(sn[i][6:]+sn[i][0:6])
						output.append(len(teacher))
						output.append(teacher)
						flex_content = searchco.flexm_tea(output,int((event.postback.data).split('&')[1])+1)
						if flex_content[1]:
							flex_content[0]["contents"][0].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
					                            {
					                            "type": "button",
					                            "action": {
					                              "type": "postback",
					                              "label": "↓↓顯示更多教師",
					                              "data": 'teamorefromnet&{}&{}'.format(int((event.postback.data).split('&')[1])+1,(event.postback.data).split('&')[2])
					                            },
					                            "style": "primary",
					                            "color": "#905c44",
					            				"height": "sm",
				                          }
					                        ]
					                      }}
									)
							flex_content[0]["contents"][9].update(
									{"footer": {
				                        "type": "box",
				                        "layout": "vertical",
				                        "contents": [
				                            {
				                            "type": "button",
				                            "action": {
				                              "type": "postback",
				                              "label": "↓↓顯示更多教師",
				                              "data": 'teamorefromnet&{}&{}'.format(int((event.postback.data).split('&')[1])+1,(event.postback.data).split('&')[2])
				                            },
				                            "style": "primary",
				                            "color": "#905c44",
				            				"height": "sm",
			                          }
				                        ]
				                      }}
									)
							flex_message = FlexSendMessage(
									    alt_text='查詢結果',
									    contents=flex_content[0],
									    
										
								)
						else:
							flex_message = FlexSendMessage(
										    alt_text='查詢結果',
										    contents=flex_content[0],
									)
						
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify("#點擊 ↓↓顯示更多教師","#顯示教師資訊(沒有在本學期課表內)(下一頁)",event.source.user_id,event)		
						return HttpResponse()
					else:

						flex_message = FlexSendMessage(
							    alt_text='查詢結果',
							    contents=searchco.detailinfo(event.postback.data)
							)
						line_bot_api.reply_message(event.reply_token, flex_message)
						sendnotify("#點擊 課程detail","顯示課程資訊({})".format(event.postback.data.split('&')[1]),event.source.user_id,event)
						return HttpResponse()
				if isinstance(event,FollowEvent):
					if (not len(firebase_admin._apps)):
							cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),'serviceAccount.json'))
							firebase_admin.initialize_app(cred)
					db = firestore.client()
					profile = line_bot_api.get_profile(event.source.user_id)
					database.init(event.source.user_id,profile.display_name,db)
					sendnotify("# {} 加入好友".format(profile.display_name),"#加入資料庫",event.source.user_id,event)
				# if isinstance(event,UnfollowEvent):
				# 	profile = line_bot_api.get_profile(event.source.user_id)
				# 	sendnotify("# {} 封鎖好友".format(profile.display_name),"#掰掰!",event.source.user_id,event)
			return HttpResponse()
		else:
			return HttpResponseBadRequest()
	except Exception as e:
		errorsendnotify('#使用者發生錯誤',e,'Server')
		return HttpResponse()
