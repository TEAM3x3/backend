# fastcampus python school & ios school collaborate
## [market kulry](https://www.kurly.com/shop/main/index.php) clone project - backend repo

## Tech
- Django 3.1
- Python 3.8.2

## Setup

```https://github.com/TEAM3x3/backend``` Fork

```shell
# git clone git@github.com:<user id>/backend.git
# cd <폴더 이름>
pyenv virtualenv 3.8.2 <가상환경 이름>
pyenv local <가상환경 이름>

pip install -r requiremens.text
cd app
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
```

```python
# root/.env
DB_HOST=localhost
DB_NAME=fc-13final
DB_USER=postgres
DB_PASSWORD=
DB_PORT=5432
DB_DEPLOY_HOST=<RDS EndPoint>
DB_DEPLOY_NAME=postgres
DB_DEPLOY_USER=postgres
DB_DEPLOY_PASSWORD=postgres
DB_DEPLOY_PORT=5432
S3_ACCESS_KEY_ID=<s3 key>
S3_SECRET_ACCESS_KEY=<s3 secret key>
```

## ERD

## API docs
[link](https://cloudy-comet-1571.postman.co/collections/5847490-3c3e8773-4e53-4ae8-a7f7-8ef4573e218d?version=latest&workspace=3b9e6b96-acb3-4058-a8b6-4d974402650f#introduction)
