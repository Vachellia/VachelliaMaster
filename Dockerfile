FROM python:3

# Create app directory
WORKDIR /app

# Bundle app source
COPY ./ /app

RUN pip install -r requirements.txt

CMD [ "python", "server.py" ]