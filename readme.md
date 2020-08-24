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
DB_NAME=<db_name>
DB_USER=postgres
DB_PASSWORD=
DB_PORT=5432
S3_ACCESS_KEY_ID=<S3_ACCESS_KEY_ID>
S3_SECRET_ACCESS_KEY=<S3_SECRET_ACCESS_KEY>

```

## ERD

## API docs
