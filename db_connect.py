from pymongo import MongoClient
client = MongoClient(port=27017)

db= client.home_surveillance #database new


data2= {
    'name':'Elon Musk',
    'encodings':[10.25,12.35,13.25,15.25]

}
appData= db.appData
# result= appData.insert_one(data2)

# x = appData.find_one()
# print(x)
myList=[]
for x in appData.find({},{ "_id": 0 }):
  myList.append(x)

print(myList[0]['encodings'])

arr=[0,1,2,3]
data3={
    'name':'Umesh',
    'encodings':arr
}
appData.insert_one(data3)

# array =



# tutorial = db.tutorial
# result = tutorial.insert_one(tutorial1)
# tutorial1 = {
#  "title": "Working With JSON Data in Python",
#      "author": "Lucas",
#      "contributors": [
#          "Aldren",
#          "Dan",
#          "Joanna"
#      ],
#      "url": "https://realpython.com/python-json/"
#  }
# tutorial = db.tutorial
# result = tutorial.insert_one(tutorial1)

# ****************************************************************new method


# from mongoengine import connect
# connect(db="home_surveillance", host="localhost", port=27017)
#
# from mongoengine import Document, ListField, StringField, URLField
#
# class Tutorial2(Document):
#     title = StringField(required=True, max_length=70)
#     author = StringField(required=True, max_length=20)
#     contributors = ListField(StringField(max_length=20))
#     url = URLField(required=True)
#

# tutorial1 = Tutorial2(
#     title="Beautiful Soup: Build a Web Scraper With Python",
#     author="Martin",
#     contributors=["Aldren", "Geir Arne", "Jaya", "Joanna", "Mike"],
#     url="https://realpython.com/beautiful-soup-web-scraper-python/"
# )
#
# tutorial1.save()  # Insert the new tutorial


