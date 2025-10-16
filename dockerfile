FROM  python:3.13
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r packages.txt
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000