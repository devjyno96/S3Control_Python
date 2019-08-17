import boto3
from pprint import pprint

'''
aws는 boto3 라이브러리를 통해 연결 할 수 있다.
'''

filename = 'test.jpg'

bucketName = 'awc20190723'  # 내 버킷 이름

downloadfilename = 'testrandomname'

s3 = boto3.resource('s3')
'''
boto3.resorce는 각  resource service를 위한 상위개체이다 - 버킷 내부의 데이터 관리
boto3.Client를 통해 low - level 에 접근할 수 있다 - 버킷 그 자체를 관리

'''

for bucket in s3.buckets.all():
    print(bucket.name)

case = 5

'''
case 1 upload
case 2 download
case 3 delete
case 4 get metadata
case 5 get file list
'''
# upload
if case == 1:

    s3 = boto3.resource('s3')
    s3.Bucket(bucketName).upload_file('test.jpg', 'testing')
    '''
    s3.Bucket(MyBucketName).upload_file(uploadFileInMyComputer, uploadFileNameInS3)
    '''

# download
elif case == 2:
    bucket = s3.Bucket(bucketName)
    s3.Bucket(bucketName).download_file(downloadfilename, 'test.jpg')
    '''
    s3.Bucket(MyBucketName).download_file(downloadFileNameInS3, downloadFileInMyComputer)
    '''

# delete
elif case == 3:
    client = boto3.client('s3')
    obj = s3.Object(bucketName, 'testing2')
    response = client.delete_object(
        Bucket=obj.bucket_name,
        Key=obj.key
    )

# get metadata
elif case == 4:
    client = boto3.client('s3')
    response = client.get_object(
        Bucket=bucketName,
        Key='testing'
    )
    pprint(response)
    '''

    '''

# list_objects
elif case == 5:
    keys = []
    client = boto3.client('s3')
    response = client.list_objects(
        Bucket=bucketName
    )
    for obj in response['Contents']:
        keys.append(obj['Key'])
    print(keys)


