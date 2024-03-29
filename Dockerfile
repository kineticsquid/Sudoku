# Python image to use.
FROM python:3.11-alpine

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

RUN date > /app/static/build.txt

# Run app.py when the container launches
# ENTRYPOINT ["python", "sudoku.py"]
EXPOSE 8080
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "wsgi_server:app"]
