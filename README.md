# placement-portal-application-21f3003074
Hello everyone this is Yasharth Vaibhav, a 2nd year undergrad student at Indian Institute of Technology Madras.<br>
The purpose of this repo is to create a dummy college placement portal as project for MAD-2 which is a part of my course curriculum and is needed for partial fullfillemt of my Bachelor's Degree.<br>
This is a full-stack placement management system built with Flask (backend) and Vue.js (frontend). Supports three user roles, Admin, Company, and Student, each with their own dashboard and set of actions.<br>
In this project I'll be mainly working use Veu, Redis, Celery, Flask, Flask-SQLAlchemy, Bootstrap, SQLite as db, etc.

Setup Instructions

Backend

1. py -m venv .env
2. .\.env\Scripts\Activate.ps1
3. pip install -r requirements.txt
4. python app.py

Frontend

1. npm install
2. npm run dev

Migration

1. flask db init
2. flask db migrate -m "msg"
3. flask db upgrade

For Celery

1. celery -A tasks worker --pool=solo --loglevel=info
2. celery -A tasks beat --loglevel=info

For Memurai

1. Get-Service Memurai
2. Start-Service memurai