


### 크롤링 참고 
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

### s3 연동
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

- AWS S3 GUI에서 작성을 원한다면 [해당링크](MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')를 참고 



#### s3 에러 발생 
```
<Code>SignatureDoesNotMatch</Code>
<Message>The request signature we calculated does not match the signature you provided. Check your key and signing method.</Message>
```
라는 에러가 발생하는 경우 [참고 링크](https://lynlab.co.kr/blog/52)