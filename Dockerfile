FROM 192.168.11.3:10000/home/python:3.7
WORKDIR /usr/src/app
ADD ./source/mainSpider.py /usr/src/app
CMD ["python3","mainSpider.py"]