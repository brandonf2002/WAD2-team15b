# WAD2-team15b
Web App Development 2 team project. 

## How to run:
Clone this repository to your local workspace.

Create new python 3 virtual enviroment, then enter your new directory and run the command:
```
pip install -r requirements.txt
```
Then run the following commands to set up the database:
```
python manage.py makemigrations
python manage.py migrate
```
To populate the database with sample data run the command:
```
python population_script.py
```
And finally to run the website on your local machine:
```
python manage.py runserver
```
Now open your web browser and visit: https://localhost:8000/
