# PlasticDB
Database for storing sinilator testing resalts

##Settup
Clone the repository
Go to the code directory
Run 'python makeDb.py'

##Run
Go to the code directory
Run 'python debug.py'

##Architecture
The app consistes of a python module containing a flask app. The app and db objects from it are minipulated for running
###debug.py
Imports app from Server and runs it with debug.
###makeDb.py
Imports db from Server and runs create_all() on it
###__init__.py
Creates flask app and db, dose inisilization
###models.py
The sql models. These objects are used for storing the samples events and messurement. Columns not prograticly generated are past in throught the __init__() function
###routes.py
Contails the apps routes. Documentation is in the file
###base.html
Base for template file, if you need to and javascript librares or css do it inside the head tag of the file.
###other html files
These are the verius templates for displying data.

##Adding more field
If you need to add more files folow these instructions
1. Update models. You will need to add more columns in the space above the __init__ function. You will also need to change the __init__ function's peramitors. *Make sure to update this everywhere the function is called.* This will mostly be in the routes.py file

2. Update the form. Add more feilds to the creation form. A howto of bootstrap forms is avalible at http://www.w3schools.com/bootstrap/bootstrap_forms_inputs.asp set the name peramiter to the name of the column
3. Update the routes. In the if statement that sees if request.method == 'POST' there is a sections that gets variables and sets them equal to form['name']. Add more of these.

4. Deleat the database.db file (THIS WILL DEALTE ALL WORK BACK IT UP!!!!!!)

5. Run makeDb.py

##Pushing to server
1. Commit and push changes
2. SSH to server with account lhc
3. cd to PlasticDB
4. run ./stop.sh
5. run git pull
6. run mysql -u root -p
7. enter password
8. run DROP DATABASE PlasticDB;
9. run CREATE DATABASE PlasticDB;
10. run quit;
11. You should now be back in bash
12. cd to code
13. run python makeDB.py
14. cd ..
15. run ./start.sh
