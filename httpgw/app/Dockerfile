FROM python:3-alpine
RUN mkdir app

COPY app /app

WORKDIR /app
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["httpgw.py"]


