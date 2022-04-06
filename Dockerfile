FROM python:alpine3.15


COPY requirements.txt requirements.txt 

run pip install -r requirements.txt 

RUN apk --no-cache add graphviz

COPY diagram.py diagram.py

RUN python3 diagram.py

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
