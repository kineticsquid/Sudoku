FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app
RUN pip3 install --upgrade pip

ADD requirements.txt /app
RUN pip3 install -r requirements.txt

# Copy runtime files from the current directory into the container at /app
ADD solvePuzzle.py /app
ADD sudoku.py /app
ADD generateImage.py /app
RUN mkdir /app/static
RUN mkdir /app/static/images
RUN mkdir /app/static/images/solutions
RUN mkdir /app/static/stylesheets
ADD static/images/* /app/static/images/
ADD static/stylesheets/* /app/static/stylesheets/
RUN mkdir /app/templates
ADD templates/* /app/templates/

#EXPOSE 5010

# Run app.py when the container launches
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 sudoku:app
