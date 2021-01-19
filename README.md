# Pizza Sales Prediction
The purpose of the project is to forecast future sales of different pizza companies.

## Before you run the project
Before you run the project, I recommend you to create a virtual environment to install the necessary packages used in the project and run the project in this environment.
After you created a virtual environmnet, run the `$ pip install -r requirements.txt` command on the terminal to install packages easily.
```
Flask==1.1.2
Flask-Sqlalchemy==2.4.4
Flask-Migrate==2.5.3
Flask-Login==0.5.0
WTForms==2.3.3
Flask-WTF==0.14.3
email-validator==1.1.2
Werkzeug==1.0.1
statsmodels==0.12.1
pandas==1.2.0
numpy==1.19.5
xlrd==2.0.1
openpyxl==3.0.5
```
You need to create a database to store the necessary tables used in the project.
I have implemented the project using PostgreSQL but you can use any other RDBMS to run this project on.
You need to specify your database credentials to provide a connection between the app and the database in line 14 of the `app.py` file:
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'dialect+driver://username:password@host:port/database'
```
For detailed information about the database connection, you can check this [page](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format).
If the connection provided successfully, the necessary tables should have been created after running these commands on the terminal:
```
$ flask db init
$ flask db migrate
$ flask db upgrade
```
You can check your database to see if the tables are created or not to be sure that your connection is successful.
And also, a new directory called `migrations` should have been created in your working directory.
Please be sure that your dataset file, in this case excel file, is in the same directory with the `app.py` file.

## Run the project
Now, you should be able to run the project using `$ flask run` command on the terminal and navigate through `http://127.0.0.1:5000` address on your browser.
To create a new task, you need to register and log in using the `Register` and `Login` tabs at the right top of the page.
Then, the `New Task` tab will be appearing at the left top of the page.
After you created a new task, you will be able to start this task to make predictions and see the results.

**Note:** I have no previous knowledge and experience about the Front-End part, that's why I couldn't be able to do it.
