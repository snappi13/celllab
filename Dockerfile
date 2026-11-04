FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cellab ./cellab
COPY automata ./automata
COPY web ./web

EXPOSE 8000
CMD ["uvicorn", "cellab.api:app", "--host", "0.0.0.0", "--port", "8000"]
