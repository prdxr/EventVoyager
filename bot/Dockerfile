FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]