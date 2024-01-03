import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("../kapi-c9b42-firebase-adminsdk-cejkv-f2d05ee407.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://kapi-c9b42-default-rtdb.firebaseio.com/"
})

ref=db.reference("PromotedPerson")

data={
    "321655":
        {
            "name": "Murtaza Hassan",
            "surname": "Robotics",   
        }
   
}

for key,value in data.items():
    ref.child(key).set(value)