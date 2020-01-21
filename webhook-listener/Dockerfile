FROM python:2.7-alpine

RUN pip install Flask flask_restplus

COPY webhook-listener.py /src/webhook-listener.py
EXPOSE 5000
CMD ["python", "/src/webhook-listener.py"]