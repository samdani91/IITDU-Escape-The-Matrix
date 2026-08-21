FROM python:3.12-slim
RUN useradd --create-home --shell /bin/bash ctfuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh && chown -R ctfuser:ctfuser /app
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
CMD ["su","-","ctfuser","-c","python /app/app.py"]
