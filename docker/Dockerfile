FROM python:3.6
COPY ./geocoder-ie/requirements.txt /opt/code/requirements.txt
COPY ./geocoder-ie/setup.py /opt/code/setup.py
WORKDIR /opt/code
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 setup.py
EXPOSE 5000