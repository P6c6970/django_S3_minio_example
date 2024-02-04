# django-S3-minio example django project

This is an example Django project with s3 Minio storage connected

## Quick start

1. Install using pip (python-dotenv is used for env)

    ``` bash
    pip install python-dotenv
    pip install pillow
    pip install django-storages
    pip install boto3
    ```
   
2. Add "storages" to your INSTALLED_APPS:

    ``` python
    INSTALLED_APPS = [
        ...
        'storages',
    ]
    ```
   
3. Set the params in settings.py. 

    ``` python
    # django-storages settings
    # S3 configuration
    AWS_ACCESS_KEY_ID = os.getenv("MINIO_ROOT_USER")
    AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_ROOT_PASSWORD")
    AWS_STORAGE_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT")
    AWS_S3_SECURE_URLS = False  # !
    AWS_S3_URL_PROTOCOL = 'http:'  # !
    AWS_S3_CUSTOM_DOMAIN = '%s/%s' % (os.getenv("MINIO_CUSTOM_DOMAIN"), AWS_STORAGE_BUCKET_NAME)
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = True
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }   
    
    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = '{folder containing storage_backends.py}.storage_backends.StaticStorage'
    
    # s3 media settings
    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = '{folder containing storage_backends.py}.storage_backends.PublicMediaStorage'
    ```
   
4. Create a file storage_backends.py next to the settings file:

    ``` python
    from storages.backends.s3boto3 import S3Boto3Storage


    class StaticStorage(S3Boto3Storage):
        location = 'static'
        default_acl = 'public-read'
    
    
    class PublicMediaStorage(S3Boto3Storage):
        location = 'media'
        default_acl = 'public-read'
        file_overwrite = False
    ```
   
5. Don't forget to add parameters to your ENV, such as:

    ``` env
    SECRET_KEY =

    # MINIO
    MINIO_ENDPOINT=http://127.0.0.1:9000 # http://minio:9000
    MINIO_CUSTOM_DOMAIN = 127.0.0.1:9000
    MINIO_ROOT_USER=minioadmin
    MINIO_ROOT_PASSWORD=minioadmin
    MINIO_BUCKET_NAME=bucket
    ```
   
6. IMPORTANT: don't forget about collectstatic

## An example of running Minio in docker-compose.yml:

``` yml
version: '3.9'
services:
  minio:
    container_name: Minio_test
    image: minio/minio:latest
    hostname: "minio"
    volumes:
      - ./minio:/minio_files
    env_file:
      - .env
    command: 'minio server /minio_files --console-address ":9001"'
    ports:
      - "9000:9000"
      - "9001:9001"

  createbuckets:
    container_name: Minio_bucket_test
    image: minio/mc:latest
    depends_on:
      - minio
    env_file:
      - .env
    entrypoint: >
      /bin/sh -c "
      /usr/bin/mc config host add myminio http://minio:9000 minioadmin minioadmin;
      /usr/bin/mc mb --quiet myminio/bucket;
      /usr/bin/mc anonymous set download myminio/bucket;
      "
```