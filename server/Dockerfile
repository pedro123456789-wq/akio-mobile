FROM python:3.10 as python

# This stops terminal buffering. Basically resolves some weird issues with python in docker containers
ENV PYTHONUNBUFFERED 1

# Install dependencies separately from adding source code
# This means that image builds will be super fast if the only difference is the source code
# If dependencies have changed then it'll be slow though :(
FROM python as dependencies

RUN pip install poetry
COPY poetry.lock pyproject.toml ./

RUN poetry export --format requirements.txt --output requirements.txt --without-hashes


FROM python as app

WORKDIR /akio

# Label helps with some scripts, but not 100% necessary
LABEL application=akio
EXPOSE 8080
COPY --from=dependencies /requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python", "run_server.py"]
