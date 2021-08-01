from pymongo import MongoClient
import gridfs
import os
from bson.objectid import ObjectId

# initializing database
client = MongoClient(port=27017)
db = client.home_surveillance  # database new
# code for storing image in a database



class Images():
    def __init__(self):
        self.fs = gridfs.GridFS(db)
        self.imageRel = db.imageRel
        self.imageInd = 0

# empty the direcotry
    def clearDirectory(self,dir):
        dir = 'static/images'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))



    # module for retriving image file from a database
    def getImages(self,filename):
        data = db.fs.files.find({'filname': filename})
        indexList = []
        for doc in data:
            id = doc['_id']
            indexList.append(id)

        print(len(indexList))

        for i in range(len(indexList)):
            outputdata = self.fs.get(indexList[0]).read()
            location = 'static/images/'+'image'+str(i+1)+'.jpeg'
            output = open(location,'wb')
            output.write(outputdata)
            output.close()

        return indexList

# for getting a single image
    def getImages2(self,myId,name):     
        self.clearDirectory('static/images')
        outputdata = self.fs.get(ObjectId(myId)).read()
        location = 'static/images/'+ name +'.jpeg'
        output = open(location,'wb')
        output.write(outputdata)
        output.close()

     
    def storeImage(self, path, filename):

        file = path+filename

        with open(file, 'rb') as f:
            contents = f.read()
        #
        self.fs.put(contents,filname = filename)
        data = db.fs.files.find_one({'filname': filename})
        self.imageInd= data['_id']
        print(self.imageInd)



    def insertDataToDb(self,path,tempfile,name,relation,address,phone, filename,encodings):
        self.storeImage(path= path,filename= tempfile)
        index = self.imageInd
        name_=name
        while True:
            if (self.imageRel.find_one({'name':name_})):
                print('try with different name')
                name_ = input("Enter a new name:")
            else:
                break
                
        data = {
            '_id':index,
            'name': name_,
            'relation': relation,
            'address': address,
            'phone': phone,
            'encodings':encodings
                        

            }
        
        self.imageRel.insert_one(data)
        self.imageInd=0
        
    def queryData(self,name):
        data = self.imageRel.find({'name':name})
        index = 0
        out = {}
        for doc in data:
            index = doc['_id']
            out = dict(list(doc.items())[1:5])

            # print(type(myid))
        if index:
            self.getImages2(myId= index,name= name)
            return out
        else:
            print("Result Not found")

    def deleteData(self, name):
        data = self.imageRel.find({'name':name})
        myId = 0
        for doc in data:
            myId = doc['_id']
            print(myId)
        if myId:
            self.fs.delete(ObjectId(myId))
            self.imageRel.delete_one( {'_id':ObjectId(myId)  })
        else:
            print('no image found')



