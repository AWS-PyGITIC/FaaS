FROM python:alpine3.15 AS build-stage


COPY requirements.txt requirements.txt 

run pip install -r requirements.txt 

RUN apk --no-cache add graphviz font-noto

COPY diagram.py diagram.py


RUN python3 diagram.py

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

FROM scratch AS export-stage
COPY --from=build-stage /*.png /
