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
