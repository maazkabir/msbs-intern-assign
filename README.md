# msbs-intern-assign
Intern Assignment Developer Task 

File Details:
Due to Google API limits I have 3 files
Developer Task #23.xlsx---> Contains all 103 keywords
Developer Task #23 reduced.xlsx ---> Contains 9 keywords
Developer Task #23 fifty.xlsx ----> Contains 50 keywords
app.py---> Main python file built using flask


Requirements:
Flask- pip install flask
mysql local database
pip install mysql.connector
pip install flask_excel
pip install requests
Imports- pandas,json,jsonify (included with flask)


Create a database named 'search'
Create a table/schema named 'searchdata_table'
mysql username:root or whatever your username is in mysql
mysql password:msbs123 or whatever your password is in mysql
Go to app.py and set the database credentials
save changes

Open a terminal go the the msbs-intern directory and type 
python app.py

Open browser go to the flask url usually http://127.0.0.1:5000
Follow the instructions


Some details of how I implemented the problem
I used the google custom search api to fetch the first 10 results of the google search and I then used advanced python to traverse through the json response sent by the google api. I implemented the project using flask and mysql. 

What the tool does:

1.The tool reads the keywords from the excel file

2.Searches the google search engine using apis for the keyword related search query data and stores the json response

3.Searches the JSON response for the futuremarketinsights url and then stores the keyword,page rank ,url , search related data into the my sql database

4.If no search results were found then the data is not stored in the database only those keywords whose data exists i.e which are found on google first page 

5.Only 10 results maybe fetched at a time from google api hence I have only traversed the first 10 results for more results I'll have to pay i.e enable billing and fetch more

6.Database Schema is 

index  | keyword | rank |  title | link

7. Only 100 query/requests can be done in a single day using the google api because for more we have to pay google. Hence I've reduced the keywords in the excel file to 10-20 so that the limits are not exceeded
