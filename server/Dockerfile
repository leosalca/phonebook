FROM python:3.9-alpine
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
# EXPOSE 5000

# Binding gunicon to python app, and serving it on port 5000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]