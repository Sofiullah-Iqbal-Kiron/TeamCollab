# TeamCollab

A project management tool to use by developer teams in TeamCollab

## About

API implementation only. No frontend included yet. <br>
Contains <br>
`project`: main project and it's related settings file <br>
`rootapp`: actual app implementing required apis <br>
Database migrations are already done. If you want to change the database then after doing that, make migrations: `py manage.py makemigrations` then migrate them to the database: `py manage.py migrate`.

## Features

1. Handy RESTful API's.
2. Documentation for apis included with OpenAPI 2.0 schema.
3. Token based authentication using [Django REST Knox](https://github.com/jazzband/django-rest-knox).
4. Browsable API redesigned with [material-design](https://github.com/youzarsiph/drf-material).

## Setup locally

##### 1. Clone the repository

`git clone https://github.com/Sofiullah-Iqbal-Kiron/TeamCollab.git`

##### 2. Change working directory

`cd TeamCollab`

##### 3. Create virtual environment

Windows: `py -m venv env` _or_ Mac/Linux: `python -m venv env`. <br>
For further information, look at the documentation for **_how to work with python virtual environment_**.

##### 4. Activate virtual environment

Windows(activate permission for virtual env first if using powershell): `env/Scripts/activate` or Mac/Linux: `source env/bin/activate`

##### 5. Install all necessary packages mentioned in `requirements.txt`

`pip install -r requirements.txt`

##### 6. Go to the actual django project directory

`cd project`

##### 7. Run development server

Windows: `py manage.py runserver` <br>
Mac/Linux: `python/python3 manage.py runserver`

## API documentation

After starting development server, both swagger-style and redoc-style documentation will be found at: <br>

- $Swagger$ `api/docs/swagger/`
- $Redoc$ `api/docs/redoc/`

## Todo

- [ ] Use JWT authentication instead of Knox-Token authentication
- [ ] Develop CI/CD pipelines
- [ ] Optimize view processing
- [x] Redesign Browsable API

## Conclusion

Nothing to conclude. Django never dies, Problem Solving never ends.
