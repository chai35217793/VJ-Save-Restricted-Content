FROM python:3.9
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Run the application using Gunicorn (or Flask, if not using Gunicorn)
CMD ["python3", "main.py"]
