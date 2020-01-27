FROM 192.168.11.3:10000/home/python:3.7
WORKDIR /usr/src/app
ADD ./source/ /usr/src/app
RUN pip3 install -r requirements.txt
CMD ["python3","mainSpider.py"]