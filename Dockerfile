FROM ubuntu:latest

COPY ./ /generatedocs

ENTRYPOINT ["python", "/generatedocs/src/main.py"]
