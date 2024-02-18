FROM alpine:3.19

# Install runtime requirements
COPY requirements.txt /app/
RUN apk update &&\
    apk add --no-cache py3-pip py3-pillow py3-psycopg2 py3-cffi tzdata &&\
    apk add --no-cache --virtual build-deps gcc libffi-dev python3-dev musl-dev &&\
    pip3 install --no-cache-dir google-crc32c google-cloud-storage uvicorn &&\
    pip3 install --no-cache-dir -r /app/requirements.txt &&\
    # Cleanup
    find /usr/lib/python* | grep '__pycache__' | xargs -n1 rm -rf &&\
    apk del build-deps gcc libffi-dev python3-dev musl-dev

# Disable python output stream buffering
ENV PYTHONUNBUFFERED 1

# Copy required files
COPY src/ /app/src/
COPY manage.py /app/
COPY startup.py /app/
WORKDIR /app/

# Static files are served from container directly via whitenoise
RUN ./manage.py collectstatic --link

# Start HTTP server
CMD python3 startup.py