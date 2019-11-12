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

The project is structured like this:
```
ribbon
├── raiment
|   ├── models.py (to define our models)
|   ├── serializers.py (to convert our models to JSON format)
|   ├── urls.py (to define URLs for our API)
|   ├── views.py (to add a viewable part to our API)
|   └── tests.py (to write tests for our API, currently empty)
├── frontend
|   ├── templates/frontend
|   |   └── (Django template files)
|   ├── static/frontend
|   |   └── where main.js is stored, in a nonreadable format created by babel
|   ├── src (babel uses these files to create main.js)
|   |   ├── component
|   |   |    └── (where the react js files are stored)
|   |   └── index.js (the part where react enters)
|   └── (Django setting files, urls.py, views.py to map URLs to the views)
├── ribbon
|   └── Django setting files (urls.py, settings.py)
├── package.json 
├── (babel js configuration files)
└── requirements.txt
```