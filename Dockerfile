FROM python:3.7
LABEL maintainer="Mokit Hossain"

WORKDIR /app
ADD . .

RUN pip install -r requirements.txt
RUN python db_create.py

EXPOSE 50000

CMD ["python", "app.py"]