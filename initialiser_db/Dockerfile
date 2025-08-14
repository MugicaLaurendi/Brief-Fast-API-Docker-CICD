FROM python:3.12


WORKDIR /initialiser_db


COPY ./requirements.txt /initialiser_db/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /initialiser_db/requirements.txt


COPY . .
#EXPOSE 8000
CMD ["python3", "main.py"]