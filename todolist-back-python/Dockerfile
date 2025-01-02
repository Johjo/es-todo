FROM python:3.13.1-bookworm

ENV LANG=fr_FR.ISO-8859-1
ENV LC_ALL=fr_FR.ISO-8859-1

COPY requirements.txt ./
COPY .env.docker ./.env

RUN pip install -r requirements.txt
COPY start_web_for_test.py ./
COPY src/ ./src
COPY views/ ./views
COPY static/ ./static



EXPOSE 8080

CMD ["python", "start_web_for_test.py"]

