FROM python:3.10-slim

# Install mime-support
RUN apt-get update &&\
    apt-get install --no-install-recommends -y mime-support &&\
    rm -rf /var/lib/apt/lists/*

# Make a new group and user so we don't run as root.
ARG UID=2008
ARG GID=2008

RUN addgroup --gid $GID appuser && adduser -u $UID --system --home /app --shell /bin/bash --ingroup appuser appuser
WORKDIR /app

# Let the appuser own the files so he can rwx during runtime.
COPY . .
RUN chown -R appuser:appuser /app

# We install all our Python dependencies. Add the extra index url because some
# packages are in the meemoo repo.
RUN pip3 install -r requirements.txt \
    --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple \
    --trusted-host do-prd-mvn-01.do.viaa.be

USER appuser

# This command will be run when starting the container. It is the same one that can be used to run the application locally.
CMD [ "python", "main.py"]
