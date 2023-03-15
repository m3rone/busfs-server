FROM python:3.10.9

COPY . .

RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

RUN apt update && apt install nano

EXPOSE 6798

CMD ["venv/bin/uwsgi", "--http-socket", "0.0.0.0:6798", "--wsgi-file", "start.py"]

# docker run -d -p 6798:6798 -v busfs-data:/app busfs-server:latest
