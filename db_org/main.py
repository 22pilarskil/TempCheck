import pymongo
import bcrypt
import datetime as dt

#MongoDB Pwd and User

pw="hack"
user="Liam-Pilarski"

#CameraID
moduleNumb = "7934017"
castedNumb = b"%a" % moduleNumb
CameraID = bcrypt.hashpw(castedNumb, bcrypt.gensalt(12))

#Current Room Status(infected(Trye) or not(False))
CRS = True

#People Data, every 5 seconds, we just append that list, we just append it with the date of today(Month, Day), not seconds because then it will take up too much 
#[35, False] = temperature, is infected
all_people = [[35, False]]
NumbOfPeople = len(all_people)

now = dt.datetime.now()
year = '{:02d}'.format(now.year)
month = '{:02d}'.format(now.month)
day = '{:02d}'.format(now.day)

PeopleData = {f"{year}-{month}-{day}":all_people}
print(PeopleData)
final = {
    "CameraID":CameraID,
    "CRS":CRS,
    "PeopleData":PeopleData,
    "NumbOfPeople":NumbOfPeople
}

# Connect to Database
connectionURL = f"mongodb+srv://{user}:{pw}@tempcheck.cfwko.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = pymongo.MongoClient(connectionURL)
mydb=client["LeptonData"]
mainCollection=mydb["DATA"]

mainCollection.insert_one(final)


