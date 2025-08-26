import os
import boto3
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION_NAME = 'ru-central1'
ENDPOINT_URL = 'https://storage.yandexcloud.net'

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise RuntimeError("Не заданы переменные окружения AWS_ACCESS_KEY_ID и/или AWS_SECRET_ACCESS_KEY")

with open('buckets.txt', 'r') as f:
    bucket_names = [line.strip() for line in f if line.strip()]

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
    endpoint_url=ENDPOINT_URL,
)

successful_buckets = []

with open('requests.txt', 'w', encoding='utf-8') as log:
    for bucket in bucket_names:
        list_success = False
        put_success = False

        # Попытка получить список объектов
        try:
            log.write(f'REQUEST: list_objects_v2 Bucket={bucket}\n')
            response = s3.list_objects_v2(Bucket=bucket)
            log.write(f'RESPONSE: {response}\n')
            list_success = True
        except ClientError as e:
            log.write(f'ERROR (list_objects_v2): {e}\n')

        # Попытка загрузить пустой ��айл
        try:
            key = 'wellenc_lex.test'
            log.write(f'REQUEST: put_object Bucket={bucket}, Key={key}\n')
            put_response = s3.put_object(Bucket=bucket, Key=key, Body=b'')
            log.write(f'RESPONSE: {put_response}\n')
            put_success = True
        except ClientError as e:
            log.write(f'ERROR (put_object): {e}\n')

        # Если хотя бы одна операция успешна, добавляем бакет
        if list_success or put_success:
            successful_buckets.append(bucket)

print('Бакеты, для которых хотя бы одна операция была успешна:')
for bucket in successful_buckets:
    print(bucket)