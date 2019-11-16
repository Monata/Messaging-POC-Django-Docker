#!/bin/bash
echo Hello, World!
npm install
pip install -r requirements.txt
python manage.py migrate && python manage.py loaddata raiment
npm run dev
python manage.py runserver
