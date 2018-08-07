
#A Flask Tool to query the keyword taken from excel files get the keywords rank and return an excel file with the data
#AUTHOR: MAAZ KABIR
#CREATED FOR MSBS-INTERN-ASSIGN
from flask import Flask, request, jsonify, json
import pandas as pd
import requests
import flask_excel as excel
import mysql.connector


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Please <a href="/upload">Click Here</a> to Upload a File to Start Querying The Search Terms'


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

         #DATABASE CONNECTION ESTABLISHMENT
         #SET THESE PARAMETERS AS PER YOUR DATABASE SPECIFICATIONS

         mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         passwd="maaz97",
         database="search"
         )

         mycursor = mydb.cursor()
         #SQL INSERT QUERY
         sql = "INSERT INTO `searchdata_table`(`keyword`, `rank`, `title`, `link`) VALUES (%s, %s, %s, %s)"
        
        
      
        #EXTRACTING DATA FROM EXCEL
           
         global data
         data=request.get_dict(field_name='file')
         data1=data["Identify the google organic search positions for each of the following search terms for the domain www.futuremarketinsights.com"]
         #STORING KEYWORDS IN KEYWORDS DICT
         keywords=[]
         for y in data1:
           keywords.append(y)
         keywords.pop(0)
         keywords.remove('Search Term')
         #CALLING GOOGLE CUSTOM SEARCH API FOR EACH KEYWORD IN THE EXCELFILE/DICT USING LOCATION AS INDIA
         for y in keywords:
            response = requests.get('https://www.googleapis.com/customsearch/v1?key=AIzaSyDThHlOVC7q-UngD_SGMzBVhyLk4JlGhOw&cx=018172089552795822638:cmhhfeciqt8&q={}&gl=in'.format(y))
            #r=json.dumps(response.text)
            #CREATING A PARSABLE JSON FROM THE RESPONSE FROM GOOGLE API
            jd=json.loads(response.text)
            print("hello {} bye".format(y))
            #jd1=eval(jd)
            i=0
            if "items" not in jd:
            	return '<h3>:( Oops Exceeded Daily Google API Limits Try Again at 12:00 AM Pacific Standard Time [Max 100 Queries/Day]</h3>'
            for x in jd["items"]:
            	#CHECKING IF THE LINK CONTAINS FUTUREMARKETINSGIHTS 
                

                if "futuremarketinsights" in jd["items"][i]["link"]:
                    print(jd["items"][i]["title"])
                    #ASSIGNING VALUES TO QUERY AND WRITING TO DATABASE
                    val = (y,i+1,jd["items"][i]["title"],jd["items"][i]["link"])
                    mycursor.execute(sql, val)
                    mydb.commit()    
                    #COMMITING ALL CHANGES AND EMPTYING JD ARRAY
                    jd.clear()
                    break

                #INCREMENTING i FOR RANK CALCULATIONS SINCE GOOGLE HAS DEPRECATED RANK API WE HAVE TO DO IT MANUALLY    
                i+=1
                
                #SINCE AT MAX 10 RESULTS CAN BE FETCHED WITH THE GOGOLE FREE API FOR MORE BILLING IS REQUIRED 
                #IF THE KEYWORD IS NOT FOUND IN THE RESULTS WE ENTER THE DATA NOT AVAILABLE INTO THE DATABASE FOR THAT KEYWORD
                 
                if i>=10:
                    #ASSIGNING VALUES TO QUERY AND WRITING TO DATABASE
                    val = (y,0,"no title available","no link available")
                    mycursor.execute(sql, val)
                    mydb.commit()    
                    #COMMITING ALL CHANGES AND EMPTYING JD ARRAY
                    jd.clear()
                    break
         #PRINTING THE NEWLY INSERTED RECORDS IN THE CONSOLE FOR MAKING SURE DATA WAS INSERTED 
         mycursor.execute("SELECT * FROM `searchdata_table`")
         rows = mycursor.fetchall()
         print('Total Row(s):', mycursor.rowcount)
         for row in rows:
           print(row)

         return '<h2>Successfully Completed all the operations Please <a href="/export">Click here</a> To Download the Search Results Excel File</h2><p>P.S: 0 Rank , Title/Link Unavailable Means That the Result wasn\'t found in the search results from google Check the Code Comments/GIT Readme for more details </p>'
        #THE TEMPLATE FOR UPLOADING AND DOWNLOADING A FILE      
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Upload an excel file to start querying on google search(csv, xls, xlsx)</h1>
    <p>The Process takes 5-10 secs to execute please don't refresh the page until it finishes</p>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''


@app.route("/export", methods=['GET'])
def export_records():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="maaz97",
    database="search"
    )
    #DATABASE CONNECTION SAME AS ABOVE
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM `searchdata_table`")
    rows = mycursor.fetchall()
 
    print('Total Row(s):', mycursor.rowcount)
    for row in rows:
        print(row)
    mycursor.execute("SELECT * FROM `searchdata_table`")
    query_sets  = mycursor.fetchall()
    return excel.make_response_from_array(query_sets, "xls",
                                          file_name="searchdata_results")
#CREATING A RESPONSE FROM DICT IN THE FORM OF AN EXCEL FILE THAT CAN BE DOWNLOADED

if __name__ == "__main__":
    excel.init_excel(app)
    app.run()