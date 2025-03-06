FROM python

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=valify_task.settings

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/runserver.sh  # Ensure the script is executable

EXPOSE 8000

ENTRYPOINT ["/app/runserver.sh"]
