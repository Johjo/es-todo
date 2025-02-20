FROM python:3.13.1-bookworm

ENV LANG=fr_FR.ISO-8859-1
ENV LC_ALL=fr_FR.ISO-8859-1

COPY requirements.txt ./
COPY .env.docker ./.env
COPY Makefile ./

RUN pip install -r requirements.txt
COPY start_demo.py ./
COPY src/ ./src

EXPOSE 80

CMD ["fastapi", "run", "start_demo.py", "--port", "80"]

