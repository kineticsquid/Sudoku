FROM us.icr.io/redsonja_hyboria/watson-base-common-rhubi7

USER root

# Set the working directory to /app
WORKDIR /app
ADD requirements.txt /app
RUN microdnf update \
    && source scl_source enable rh-python36 \
    && microdnf update; microdnf clean all
ENV PATH="/opt/rh/rh-python36/root/usr/bin:${PATH}"
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy runtime files from the current directory into the container at /app
ADD *.ttf /app/
ADD solvePuzzle.py /app
ADD sudoku.py /app
RUN mkdir /app/static
RUN mkdir /app/static/images
RUN mkdir /app/static/stylesheets
ADD static/images/* /app/static/images/
ADD static/stylesheets/* /app/static/stylesheets/
RUN date > /app/static/build.txt
RUN mkdir /app/templates
ADD templates/* /app/templates/

RUN ls -R
RUN cat /app/static/build.txt


EXPOSE 80

# Run app.py when the container launches
CMD ["python3", "sudoku.py"]
