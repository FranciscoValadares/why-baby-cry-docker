FROM python:3.8-slim-buster


RUN apt update
#RUN apt install -y python3.8 gcc
#RUN pip install fastaudio
#RUN pip install https://github.com/fastaudio/fastaudio.git
RUN pip install https://github.com/FranciscoValadares/fastaudio.git

ADD requirements.txt requirements.txt
ADD export.pkl export.pkl
ADD app.py app.py

# Install required libraries
RUN pip install -r requirements.txt

# Run it once to trigger resnet download
RUN python app.py

EXPOSE 8008

# Start the server
CMD ["python", "app.py", "serve"]
