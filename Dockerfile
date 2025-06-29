FROM python:3

COPY ./ /generatedocs
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/generatedocs/src/main.py"]
