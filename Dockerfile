FROM python:2.7-alpine

RUN apk -Uuv add ca-certificates

RUN pip install boto3

ADD ecs-deploy.py /bin/

RUN chmod +x /bin/ecs-deploy.py 

ENTRYPOINT ["python", "/bin/ecs-deploy.py"]
