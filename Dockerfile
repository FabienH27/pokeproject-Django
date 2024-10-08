FROM python:3

# Prevent Python from writing .pyc files and enable output buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt;

# Copy the entire project to the working directory
COPY . /code/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

# Set the entrypoint to the script
RUN /entrypoint.sh

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]