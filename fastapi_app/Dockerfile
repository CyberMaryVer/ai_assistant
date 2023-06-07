FROM python:3.11.3-slim-bullseye
WORKDIR /app

# For installing deps
COPY ./requirements.txt .

# Update and install deps
RUN apt-get update && \
    pip install --upgrade pip  && \
    pip install -r requirements.txt

# Copy relevant source code
COPY . ./fastapi_app

# Add group AND user 'fastapi', change fastapi_app workdir ownership
RUN groupadd -r fastapi && \
    useradd -r -g fastapi fastapi --home-dir /app && \
    chown -R fastapi:fastapi /app/

# Change to least privilege user (for security reasons)
USER fastapi

CMD ["uvicorn", "fastapi_app.fastapp:app", "--port", "8000", "--host", "0.0.0.0", "--reload"]