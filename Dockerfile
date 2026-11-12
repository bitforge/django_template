FROM alpine:3.24

# Install runtime requirements
# System python is used on purpose to get prebuilt pillow & psycopg2 packages
COPY requirements.txt /app/
RUN apk update &&\
    apk add --no-cache py3-pip py3-pillow py3-psycopg2 py3-cffi libmagic tzdata &&\
    apk add --no-cache --virtual build-deps gcc libffi-dev python3-dev musl-dev &&\
    pip3 install --no-cache-dir --break-system-packages google-crc32c google-cloud-storage uvicorn &&\
    pip3 install --no-cache-dir --break-system-packages -r /app/requirements.txt &&\
    # Cleanup
    find /usr/lib/python* | grep '__pycache__' | xargs -n1 rm -rf &&\
    apk del build-deps gcc libffi-dev python3-dev musl-dev

# Disable python output stream buffering
ENV PYTHONUNBUFFERED=1

# Copy required files
COPY src/ /app/src/
COPY manage.py /app/
COPY startup.py /app/
WORKDIR /app/

# Static files are served from container directly via whitenoise
RUN ./manage.py collectstatic --link

# Start HTTP server
CMD ["python3", "startup.py"]
