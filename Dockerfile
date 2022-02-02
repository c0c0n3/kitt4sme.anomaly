# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 8000

RUN pip install pipenv
RUN mkdir /src
COPY Pipfile /src/Pipfile
COPY Pipfile.lock /src/Pipfile.lock
RUN cd /src && { pipenv lock -r > /requirements.txt; }
RUN pip install -r /requirements.txt

COPY anomaly_detection /src/anomaly_detection
COPY data /src/data
WORKDIR /src
ENV PYTHONPATH=$PWD:$PYTHONPATH

EXPOSE 8000
ENTRYPOINT ["uvicorn", "anomaly_detection.main:app", "--host", "0.0.0.0", "--port", "8000"]
