from __future__ import print_function
import pyrebase as pyfire
from decouple import config

fire_config = {
	"apiKey": config('apiKey'),
    "authDomain": config('authDomain'),
    "databaseURL": config('databaseURL'),
    "projectId": config('projectId'),
    "storageBucket": config('storageBucket'),
    "messagingSenderId": config('messagingSenderId')
}

class FirebaseDB():
	def __init__(self):
		fire = pyfire.initialize_app(fire_config)
		self.db = fire.database()

	def new_model(self,name):
		self.db.child(name)
		print("A new model created - %s" %name)
		return name

	def push_new(self,model_name,data):
		self.db.child(model_name).push(data)

	def get_all(self, model_name):
		data = self.db.child(model_name).get()
		print(data.val())

#fdb = FirebaseDB()
#model = fdb.new_model("gps-data")
#fdb.push_new(model, "{ 'con':'hello2','help6':'one'}")
#fdb.get_all(model)
