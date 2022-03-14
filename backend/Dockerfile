FROM python:3.8.9-buster
# make the 'backend' folder the current working directory
WORKDIR /backend
COPY . .
# install project dependencies
RUN pip install -r requirements.txt

CMD ["python", "src/API.py"]