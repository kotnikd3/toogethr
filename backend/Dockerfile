FROM python:3.8
# make the 'backend' folder the current working directory
WORKDIR /backend
COPY . .
# install project dependencies
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["src/API.py"]