import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def update(user,course,db):
	doc_ref = db.collection('linebotuser').document(user)
	if doc_ref.get().exists:
	    doc_ref.update({
	        "course":firestore.ArrayUnion([course])
	    })
	else:
	    doc_ref.set({
	        "course":[course]
	    })
"""doc_ref = db.collection('linebot').document('coursecollection')
    doc = doc_ref.get().to_dict()
    if user in doc:
        doc_ref.update({
        user:firestore.ArrayUnion([course])
        })
    else:
        doc_ref.update({
        user:[course]
        })"""
def remove(user,course,db):
	doc_ref = db.collection('linebotuser').document(user)
	doc = doc_ref.get().to_dict()
	if course in doc["course"]:
		doc_ref.update({
        "course":firestore.ArrayRemove([course])
        })
	else:
		pass


"""doc_ref = db.collection('linebot').document('coursecollection')
    doc = doc_ref.get().to_dict()
    if course in doc[user]:
        doc_ref.update({
        user:firestore.ArrayRemove([course])
        })
    else:
        pass"""
def get(user,db):
	doc_ref = db.collection('linebotuser').document(user)
	doc = doc_ref.get().to_dict()
	if doc:
		if len(doc["course"])!=0:
			return doc["course"]
		else:
			return ['nocourse']
	else:
		return ['nocourse']


""" doc_ref = db.collection('linebot').document('coursecollection')
    doc = doc_ref.get().to_dict()
    if user in doc:
        if len(doc[user])!=0:
            return doc[user]
		else:
            return ['nocourse']
    else:
        return ['nocourse']"""

def removeall(user,db):
	doc_ref = db.collection('linebotuser').document(user)
	try:
	    doc_ref.update({
	        "course":[]
	    })
	except:
	    pass
"""doc_ref = db.collection('linebot').document('coursecollection')
    doc_ref.update({user:[]})"""

def init(user,name,db):
	doc_ref = db.collection('linebotuser').document(user)
	if doc_ref.get().exists:
	    pass
	else:
	    doc_ref.set({
	        "course":[],
	        "info":{
	        "name":name,
	        "status":False,
	        }
	    })
