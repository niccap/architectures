# Use the lightweight alpine image
FROM python:3.8-alpine

# Installing needed packages
RUN pip install flask waitress

# Defining the working directory
WORKDIR /usr/src/app

# Adding needed files
COPY vin_decoder.py ./

# Exposing the port used to communicate
EXPOSE 8081

# Command to run when executed
CMD ["python","vin_decoder.py"]

