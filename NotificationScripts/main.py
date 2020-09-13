from functions import textMessage, emailMessage
import datetime as dt
import pymongo

def main():
    pw="hack"
    user="Liam-Pilarski"
    connectionURL = f"mongodb+srv://{user}:{pw}@tempcheck.cfwko.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connectionURL)
    mydb=client["LeptonData"]
    mainCollection=mydb["DATA"]
    profileCollection=mydb["Profile"]


    all_documents = mainCollection.find()
    for document in all_documents:
        #Get all of the classrooms 
        message = "Current Status: \n"
        for count, person in enumerate(document["PeopleData"]):
            if person[1] > 36:
                message+=f"\nPerson({count}) has an above average temperature"
        if document["NumbOfPeople"] > 25:
            message+="\n Too many people{0}".format(document["NumbOfPeople"])

        #Find Profile with same ID
        CameraID = document["CameraID"]
        prof = profileCollection.find_one({"CameraID":CameraID})
        print(prof)
        textMessage(CameraID, [prof["phone1"],prof["phone2"]])
        emailMessage(CameraID, [prof["email1"],prof["email2"]])
    
if __name__ == "__main__":
    while True:
        if dt.datetime.now().hour%1 == 0:
            main()
