# start by pulling the python image
FROM python:3.12-slim


# timezone env and linking it to debian's OS config
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# tzdata for timzone
RUN apt-get update -y
RUN apt-get install -y tzdata

# copy the requirements file into the image
COPY requirements.txt /purchasing-manager/requirements.txt

# switch working directory
WORKDIR /purchasing-manager

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /purchasing-manager/

# configure the container to run in an executed manner
ENTRYPOINT [ "flask", "--app", "purchasing_manager", "run", "-h", "0.0.0.0", "-p", "5000" ]