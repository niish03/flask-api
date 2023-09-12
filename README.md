Live API : https://flask-api-0x4q.onrender.com/

Selenium Python used to scrap the data.

Run bot.py file to automate all the process and store it into the database
Add A ENV FIle
URI = < / DatabaseURL / >

IT will Search on the data:

District: मुंबई उपनगर
Taluka: अंधेरी
Village: बांद्रा
Select Year: 2023
Enter Doc/Property/CTS/Survey no/Reg. Year: 2023

* It Will automate the process of captcha reading
* Store Data into Dataframe
* Pre Process the data
* Clean Data
* Translate Data from Marathi To English
* Store into database




# flask-api

Add A ENV FIle
URI = < / DatabaseURL / >

install requirement file using 
pip3 install requirements.txt
Technologies Used:
Flask
PostgreSql

# Run Code

Run code using python3 flaskAPI.py

Endpoints:

#  GET / 

It Will fetch all the data which is scrapped.
Filter can be applied by query params 
1) name = Somani
2) search = Other Information 


name will search both on buyer name as well as seller name
search params will search results from Other Informations Column


#  GET /year/{year}

It Will Fetch all the relevent year documents


#  GET /doc/{doc_number}

It Will Fetch all the relevent documents with related doc_number

