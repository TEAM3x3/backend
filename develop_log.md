# load data guide line

```python
# 세일품목
Goods.random_discount_rate()
# 카트 보관 상태 
Goods.set_goods_packing_status()
```

# [REST API](https://meetup.toast.com/posts/92)

# 마켓컬리를 구현하면서 작성하는 일지
## 0819
- [변수 시작이 숫자가 되지 못하는 이유](https://epicdevsold.tistory.com/20)
- **크롤링 참고**
	- [지연 시간](https://codechacha.com/ko/selenium-explicit-implicit-wait/)
	- [단축키](https://tariat.tistory.com/656)
	- [셀레니움 참고 링크](https://seyul.tistory.com/45)
	- find_element_by_id 요소의 속성 id로 찾는 오브젝트를 찾습니다. 
	- find_element_by_class_name 요소의 속성 class가 포함된 오브젝트를 찾습니다. 
	- find_element_by_name 요소의 속성 name로 찾는 오브젝트를 찾습니다. 
	- find_element_by_xpath xpath를 이용해서 오브젝트를 찾습니다. 
	- find_element_by_link_text 하이퍼 링크의 텍스트로 오브젝트를 찾습니다.(완전 일치) - 탐색이 잘 안됩니다. 
	- find_element_by_partial_link_text 하이퍼 링크의 텍스트로 오브젝트를 찾습니다.(포함) - 탐색이 잘 안됩니다. 
	- find_element_by_tag_name 요소의 태그 이름으로 찾습니다. 
	- find_element_by_css_selector css selector(sizzle)로 오브젝트를 찾습니다.


#### s3 연동
- [media files 설정](https://wayhome25.github.io/django/2017/05/10/media-file/)
- [Amazon s3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)

1. boto3 [quick start docs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) : python 개발자가 S3 및 ec2서비스를 작성할 수 있도록 도와주는 소프트웨어 ```pip install boto3```
2. boto3를 사용하기 위해서 [IAM console](https://console.aws.amazon.com/iam/home?region=ap-northeast-2#/home)에 가서 키를 생성해야 한다.
3. 사용자 생성, 이름은 아무렇게나 (명시적으로 S3User 추천), 엑세스 유형은 프로그래밍 방식 으로 하며, 권한은 기존 정책 직접 연결에서 - AmazonS3FullAccess을 설정한다. 나머지는 다 건너 뛰고 생성을 누르면 엑세스 키를 준다. 해당하는 값들을 다른곳에 저장을 해 두어야 한다. 
4. ```pip install django-storages boto3```
	-	 shell 에서 작성을 원한다면  

```python
import boto3
client = boto3.client('s3')

client.create_bucket(
Bucket='<버켓 명>',
CreateBucketConfiguration={
'LocationConstraint':'ap-northeast-2'}
)
```



- AWS S3 GUI에서 작성을 원한다면 [해당링크](https://siner308.github.io/2019/07/17/django-aws-s3/)를 참고 



##### s3 에러 발생 
```
<Code>SignatureDoesNotMatch</Code>
<Message>The request signature we calculated does not match the signature you provided. Check your key and signing method.</Message>
```
라는 에러가 발생하는 경우 [참고 링크](https://lynlab.co.kr/blog/52)
또는
일정 시간이 지나고 난 뒤에는 정상 작동 한다.

##### sqlite3를 사용하지 않는 이유
- [참고 링크](http://egloos.zum.com/sweeper/v/3052951)
- [sqlite vs mysql vs postgresql](https://ko.bccrwp.org/compare/sqlite-vs-mysql-vs-postgresql-a-comparison-of-relational-database-management-systems-8f2704/)


##### [포스트맨 문서](https://velog.io/@jinee/TIL-Postman%EC%9C%BC%EB%A1%9C-API%EB%AC%B8%EC%84%9C-%EB%A7%8C%EB%93%A4%EA%B8%B0-l4k5mj31rl)

## 0820 
##### [sqlite -> postgresql](https://gustjd887.tistory.com/26)


## 0824
##### [readme 작성 ](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)
	
### 배포
1. EC2 생성
2. Elastic IP 생성
3. RDS 생성  - 로컬 개발환경이랑, RDS 랑 연동

### [postman 예제 저장하기](https://velog.io/@jinee/TIL-Postman%EC%9C%BC%EB%A1%9C-API%EB%AC%B8%EC%84%9C-%EB%A7%8C%EB%93%A4%EA%B8%B0-l4k5mj31rl)

## 0826
### develop
extreme progmming , scrum

## 0827
**시리얼라이저의 중복을 최소화 할 수 있을까?**


파일 병합 시 migrations 파일 충돌을 해결하는 방법

[django haystack](https://django-haystack.readthedocs.io/en/master/)

[django filter- goods](https://brownbears.tistory.com/96)


## 0831 wsgi app server

### 개념정리
[블로그 글 1](https://brownbears.tistory.com/350)
- 웹 서버 : 클라이언트가 HTTP request를 통해 리소스를 요청하면 그 리소스를 그대로 보여주는 것이 웹 서버의 역할이다. (html, css, image등../static)
- CGI(Common Gateway Interface) : 웹 서버에서 앱을 작동시키기 위한 인터페이스)

### two scoop django

늘 장고는 wsgi와 함께 배포한다. 

이 파일은 장고 프로젝트를 wsgi 서버에 배포할 때 필요한 기본 설정 사항을 담고 있다. 

uWSGI와 구니콘은 장고 개발자들이 웹 서버에서 최대한 성능을 뽑아 내는데 자주 사용한다.

현재 uWSGI가 좀 더 많은 설정을 제공하지만, 구니콘 또만 매우 많은 설정을 제공하며, 설정이 좀 더 쉽다. 

#### wsgi 가 필요한 이유
[https://ossian.tistory.com/110의 글](https://ossian.tistory.com/110)
- Django의 runserver는 단일 쓰레드로 작동하여 테스트 용도에서는 적당하나,Request 요청이 많아지는 경우, 현저히 능력이 떨어지므로, product환경에서는 적당하지 않다. 
#### wsgi 에서 사용하는 server의 종류
[블로그 정리 글 1](https://paphopu.tistory.com/entry/WSGI%EC%97%90-%EB%8C%80%ED%95%9C-%EC%84%A4%EB%AA%85-WSGI%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80)

- wsgi server는 많은 Request를 다룰 수 있도록 설계가 되었다. 
framework들은 스스로 수천개의 request들을 실행하고 최고의 방법으로 처리할 수 있도록 설계가 되어있지 않다. -> Django는 manage.py runserver로 배포를 하면 안된다는 소리이다. 

- wsgi는 python web 개발 속도를 올려준다. 이유는 wsgi 의 기초적인 것들만 알아도, 사용하는데 아무런 문제가 없다는 뜻 이다. 너가 TurboGears, Django, cherryPy를 사용한다면, 너의 framework가 wsgi 표준을 어떻게 사용하는지 굳이 알 필요는 없다. 하지만 확실히 wsgi에 대해 안다면 도움이 된다.




## shell에서 환경설정 쉽게 하기
export -> shell 변수들은 export 명령어와 사용이 된다면 환경 변수를 쉽게 정의할 수 있다.




## Order 뒤로 가기 시 카트가 None이 되는 상황은?
주문서 생성 시 cart 는 None이 된다. 이후에 뒤로가기가 요청이 될 경우 cart에 담긴 item들은 None이 되어 데이터가 소실된다. 

이에 대한 방법은 order에 status field - 결제 완료, 진행 중 등 값을 넣고 완료 시 cart 의 값을 None으로 변경한다.

-> signal로 결제 완료 후 status value >>> update 호출.  업데이트 

## django admin page custom
[링크](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#overriding-admin-templates)

## django transaction
#### django에서 트랜잭션을 구현하는 3가지 방법
1. 데코레이터를 이용한 Transaction : 하나의 함수에 적용
2. with 명령어를 이용한 트랜잭션 : 중간 부분에 적용 
3. savepoint를 직접 지정 


기본적으로 django는 transaction을 지원하지만, ATOMIC_REQUESTS가 False 이므로, ORM 쿼리 단위로 transaction이 관리된다. (create, delete, update, get_or_create …)

그래서 어떤 특정 코드 뭉치에 DB transaction을 지원하려면, transaction.atomic과 같은 구문이 필요하다.

이 때 주의할 점은 with transaction.atomic 블록 안에서 try-except를 하지말라는 것이다. (django 문서에도 언급되어 있다.)

transaction.atomic() 내부에서는 try-except 를 사용하지말자. 써야만 한다면 try 블록이 transaction.atomic() 블록을 감싸도록 사용하자.

# [django sercrets](https://docs.python.org/3/library/secrets.html) - 비밀관리를 위한 난수 생성 
- 암호, 계정 인증, 보안 토큰, 관련 비밀 등 데이터 관리에 적합한 암호화된 강력한 무작위 번호를 생성하는 데 사용된다.
- 보안이나 암호화가 아닌 모델링과 시뮬레이션을 위해 설계된 무작위 모듈의 기본 의사 난수 생성기에 우선하여 사용해야 한다.
- 랜덤함수는 매번 같은 난수를 생성한다. secrets는 다른 난수를 생성한다. 

# [Django ORM](https://medium.com/@chrisjune_13837/django-%EB%8B%B9%EC%8B%A0%EC%9D%B4-%EB%AA%B0%EB%9E%90%EB%8D%98-orm-%EA%B8%B0%EC%B4%88%EC%99%80-%EC%8B%AC%ED%99%94-592a6017b5f5)

### [kakao pay blog](https://in0-pro.tistory.com/16)

### [django session](https://valuefactory.tistory.com/708)


### [쿠키, 세션, 캐시 장단점](https://homzzang.com/b/css)

#### [세션문서](http://rmaru.com/open/django_%EC%84%B8%EC%85%98_%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)

#### [django filters](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html)


### [datetime calculate](https://stackoverflow.com/questions/31432397/calculate-datefield-until-days-in-django)


### [Session: HTTP & RESTful HTTP API](https://velog.io/@magnoliarfsit/Session-HTTP-RESTful-HTTP-API-1)

### [인증 방법, header, session&cookie, JWT](https://tansfil.tistory.com/58)

### [django 검색엔진 - django full text]

### [db indexing](https://medium.com/@dlarkqrl4966/how-to-create-an-index-in-django-without-downtime-c9a5a194877a)

### [drf yasg](https://velog.io/@rubycho/%EB%AC%B8%EC%84%9C%ED%99%94%EB%A5%BC-%EC%9C%84%ED%95%9C-drf-yasg-%EC%A0%81%EC%9A%A9%ED%95%98%EA%B8%B0)

### [drf yasg 문서 자동화](https://medium.com/towncompany-engineering/%EC%B9%9C%EC%A0%88%ED%95%98%EA%B2%8C-django-rest-framework-api-%EB%AC%B8%EC%84%9C-%EC%9E%90%EB%8F%99%ED%99%94%ED%95%98%EA%B8%B0-drf-yasg-c835269714fc)

### [drf yasg example value](https://item4.blog/2020-03-04/Add-Example-on-drf-yasg/)

# 10.1 
ModelActionSerializers는 drf-yasg를 사용할 때 serializers field 표현이 각 액션마다 적용이 안되어 어려우므로 api docs 를 yasg를 사용하게 되었으므로 modelserialziers를 사용하여 대체한다.
