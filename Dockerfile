FROM python:3.12.1 as requirements-stage
# This is for install dependecies with poetry 
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.12.1
# requirment files and all the installations and run command
WORKDIR /app 
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
