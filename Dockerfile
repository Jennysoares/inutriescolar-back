FROM python:3

RUN mkdir code/
COPY . code/
WORKDIR /code/inutriescolar_api
COPY requirements.txt /code/inutriescolar_api

RUN pip3 install -r requirements.txt
    
WORKDIR /code

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]