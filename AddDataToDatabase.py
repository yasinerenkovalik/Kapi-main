import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("kapi-c9b42-firebase-adminsdk-cejkv-f2d05ee407.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://kapi-c9b42-default-rtdb.firebaseio.com/"
})

ref=db.reference("PromotedPerson")

data={
    "321654":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
"424242":
        {
            "name": "Yasin Eren Kovalık",
            "major": "BackEndk",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key,value in data.items():
    ref.child(key).set(value)