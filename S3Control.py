import boto3
from pprint import pprint
import hashlib
import time
import os
'''
aws는 boto3 라이브러리를 통해 연결 할 수 있다.
'''
fileKey = ''
# 파일 키값 저장

fileName = 'test.jpg'
# 파일이름 파일의 위치까지 지정해도 상관업다. 스플릿 해서 잘라 사용할꺼니깐

bucketName = 'awc20190723'
# 내 버킷 이름


s3 = boto3.resource('s3')
# 전체 함수에서 사용할 객체

statinfo = os.stat(fileName)


#진행도를 나타내기 위한 함수
progressBytes = 0

def progressPercent(chunk): # 업로드한 byte 입력됨 누적시켜야함
    global progressBytes
    if progressBytes >= statinfo.st_size :
        progressBytes = 0
    progressBytes += chunk
    print(progressBytes / statinfo.st_size * 100)


def getHash(string): # 파일명 + 현재시간 을 sha1코드로 변환

    # 입력받은 문자열 + 현재 시간(형식 :  1510647686.5457149 ) 을 해쉬매핑
    changeString = string.encode('utf-8') + str(time.time()).encode('utf-8')
    sha = hashlib.sha1(changeString)

    # hexdigent 방법을 이용하여 객체로 부터 해시값을 16진법으로 구함
    hexSha1 = sha.hexdigest()
    return hexSha1


def getMetadate(fileKeyGet) :
    client = boto3.client('s3')
    response = client.get_object(
        Bucket = bucketName,
        Key = fileKeyGet
    )
    #response['Metadata']['filename'] responce에서(dict타입) 파일 이름 뜯어내는 방법
    return response


def upload(filePathUp) :
    fileNameUp = filePathUp.split('/').pop()#파일 이름을 / 로 나눈 배열의 맨 끝
    fileKeyUp = getHash((fileNameUp))
    s3.Bucket(bucketName).upload_file(filePathUp, fileKeyUp, Callback = progressPercent)

    '''
    s3.Bucket(MyBucketName).upload_file(uploadFileInMyComputer, uploadFileNameInS3)
    '''
    # 메타데이터 넣기
    s3_object = s3.Object(bucketName, fileKeyUp)
    s3_object.metadata.update({'fileName': fileNameUp})
    s3_object.metadata.update({'test2': 'testes2'})
    s3_object.copy_from(CopySource={'Bucket': bucketName, 'Key': fileKeyUp}, Metadata=s3_object.metadata,
                        MetadataDirective='REPLACE')
    # 완료
    return fileKeyUp


def download(fileKeyDown) :
    metadata = getMetadate(fileKeyDown)
    fileNameDown = metadata['Metadata']['filename']
    s3.Bucket(bucketName).download_file(fileKeyDown, fileNameDown, Callback = progressPercent)
    #다운 받고싶은 바일 이름을 바꾸고 싶아면 fileNameDown 변경
    '''
    s3.Bucket(MyBucketName).download_file(target_Key_Name_In_S3, file_name_As_MyComputer)
    '''


def deleteObject(fileKeyDelete) :
    client = boto3.client('s3')
    obj = s3.Object(bucketName, fileKeyDelete)
    response = client.delete_object(
        Bucket=obj.bucket_name,
        Key=obj.key
    )


def getList() :
    keys = []
    client = boto3.client('s3')
    response = client.list_objects(
        Bucket=bucketName
    )
    for obj in response['Contents']:
        keys.append(obj['Key'])
    print(keys)
    #일단 key값만 가져오게 만들었다 다음에 쓸모에 따라 수정하자


fileKey = upload(fileName)
download(fileKey)