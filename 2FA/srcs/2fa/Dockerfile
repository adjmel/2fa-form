FROM python:3.10.13

RUN apt update -y && apt upgrade -y

COPY ./tools/requirements.txt .
COPY --chmod=777 ./tools/script.sh .

RUN apt install python3 \
    && pip install -r /requirements.txt \
    && pip install Django \
    && pip install -U djangorestframework \
    && pip install djangorestframework_simplejwt \
    && pip install django-otp \
    && pip install django-bootstrap-v5

ENTRYPOINT ["./script.sh"]