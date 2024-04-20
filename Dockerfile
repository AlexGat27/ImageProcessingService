FROM python

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6

COPY . /app/

EXPOSE 5000

CMD [ "python", "AdminFlask.py" ]