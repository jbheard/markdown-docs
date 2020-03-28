FROM python:3

COPY ./ /generatedocs

ENTRYPOINT ["python", "/generatedocs/src/main.py"]
