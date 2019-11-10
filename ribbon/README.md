**Raiment Django Server**

To run the server you need to write

npm install
pip install -r requirements.txt

then after setting up dependencies start the react by writing

npm run dev

then populate the database with the following command

python manage.py migrate && python manage.py loaddata raiment

then run the django server by

python manage.py runserver


