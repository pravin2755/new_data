import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# client = MongoClient('hostname', 27017)          #ANOTHER WAY TO CONNECT MONGODB
mydb = myclient["test_db"]
mycoll = mydb['col1']

# print(myclient.list_database_names())                 #it is used for list of database name !!!!
#
# db_list=myclient.list_database_names()
#
# for i in db_list:
#     print(i)


# _________________________________________________many insert _________________________________________!!!

# mydict = {'username': 'pravin', 'first_name': 'pravinsinh', 'last_name': 'gohil', 'email': 'pravin@gmail.com',
#           'password1': 'shivay@27', 'password2': 'shivay@27'}
# x = mycoll.insert_one(mydict)  # it is used for insert one record or document(dict).
#
# mylist = [
#     {'username': 'jaimin', 'first_name': 'jaiminkumar', 'last_name': 'patel', 'email': 'jaimin@gmail.com',
#      'password1': 'shivay@27', 'password2': 'shivay@27'},
#     {'username': 'jaydip', 'first_name': 'jaydipkumar', 'last_name': 'ghusar', 'email': 'jaidip@gmail.com',
#      'password1': 'shivay@27', 'password2': 'shivay@27'},
#     {'username': 'hardik', 'first_name': 'hardikkumar', 'last_name': 'ghusar', 'email': 'hardik@gmail.com',
#      'password1': 'shivay@27', 'password2': 'shivay@27'},
#     {'username': 'mahendra', 'first_name': 'mahendrasinh', 'last_name': 'jadeja', 'email': 'mahendra@gmail.com',
#      'password1': 'shivay@27', 'password2': 'shivay@27'},
#
# ]
# x = mycoll.insert_many(mylist)              # it used for insert (add)to the database more than one records.

# ________________________________________________SELECTED COLUMN DATA DISPLAY ______________________________!!!!
# z = mycoll.find_one({}, {'_id': 0, 'username': 1, 'first_name': 1})  # it is used for which
# print(z)
# for y in mycoll.find({}, {'username': 0}):
#     print(y)

# ___________________________________________________SELECTED DOCUMENT GETS __________________________________!!!!!

# myquery = { "username": { "$gt": "p" } }
# mydoc = mycoll.find(myquery)
# print(mydoc)
# for i in mydoc:
#     print(i)

# __________________________________________________SHORTING DATA _____________________________________________!!!!!

# mydoc = mycoll.find().sort("username")
#
# for x in mydoc:
#   print(x)
#


# mydoc = mycoll.find().sort("username",-1)     # SHORTING IN DESCENDING ORDER
# for x in mydoc:
#   print(x)

# __________________________________________________DELETE  DOCUMENT_______________________________________!!!!!!
# mycoll.delete_one({'username':'pravin'})     # DELETE ONE DOCUMENT.


# myquery = { "username": {"$regex": "^h"} }
#
# x = mycoll.delete_many(myquery)             # DELETE MORE THAN ONE DOCUMENTS.
#
# print(x.deleted_count, "documents deleted")

# x = mycoll.delete_many({})


# _________________________________________________DELETE COLLECTION________________________________________!!!!!


# mycoll.drop()
#
# x=mycoll.find().limit(5)
# for i in x:
#     print(x)

# ________________________________________________UPDATE______________________________________________________!!!!!

    # myquery = { "username": "jaydip" }
    # newvalues = { "$set": { "email": "jb@gmail.com  " } }
    #
    # mycoll.update_one(myquery, newvalues)


# _____________________________________________aggregate______________________________________________________!!!!!

pipeline=[{"$sort":{"username":1}},{"$limit":2}]
datda=mydb.col1.aggregate(pipeline)
print(datda)
for i in datda:
    print(i)

