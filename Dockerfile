FROM python:3

RUN pip install -Iv pyyaml==5.3.1
RUN pip install -Iv jinja2==3.1.2
COPY ./ /generatedocs

ENTRYPOINT ["python", "/generatedocs/src/main.py"]
