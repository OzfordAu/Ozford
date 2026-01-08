Project Requirements Python 3.13.0 PostgreSQL 16 node 22.15.0 npm 10.9.2

How to Run the Project

1\. configure you PostgreSQL database

2\. create .env file in the root directory

.env example
######################################
DJANGO_ENV=development

DEBUG=on

ALLOWED_HOSTS=*

SECRET_KEY='z6wma2u0ojgm7jez3))ug3$9sou8@vsdfg4!#j$@#nv_bs87iue1'

DB_NAME=db_name

DB_USER=db_admin

DB_PASSWORD=db_password

DB_HOST=localhost

DB_PORT=5432
#########################

2\. Run command pip install -r requirements.txt

3\. Run command npm install

4\. Follow standard wagtail/django/tailwinds comand commands
