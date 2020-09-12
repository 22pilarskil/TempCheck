import pymongo
import bcrypt

#Assign Global Variables
pw="assimo11!"
user="Zayn-Rekhi"
module = "12312371203"
ModuleNumb = b"%a" % module
HashedModuleNumb = bcrypt.hashpw(ModuleNumb, bcrypt.gensalt(12))
IsSick = False
#Create/Connect to Database
connectionURL = f"mongodb+srv://{user}:{pw}@tempcheck.cfwko.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = pymongo.MongoClient(connectionURL)
mydb=client["LeptonData"]
mainCollection=mydb["DATA"]


mainCollection.insert_one({
    "AllPeople":[[1,38.5,False,0.60]], 
    "MODULEID":HashedModuleNumb,
    "IsSick":IsSick,
})


