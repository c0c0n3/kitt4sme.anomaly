# kitt4sme.anomaly
Detects anomalies in amount of energy produced in battery packs when they are welded.

## Usage

1. Install python(```>=3.8```), pipenv and Docker

## Get the repository
``` 
git clone https://github.com/c0c0n3/kitt4sme.anomaly.git
cd kitt4sme.anomaly
pipenv install
```
## Activate virtual environment
``` 
pipenv shell
```
## Testing before building
Open your favorite python ide in this virtual enviromnment and run the tests
```
python -m pytest tests
```
or just run unit tests
```
python -m pytest tests/unit
```
## Buid and Run Docker image
```
docker build -t kitt4sme/anomaly .
docker run -p 8000:8000 kitt4sme/anomaly
```
