# Parking spot application
### About the project
Full-stack challenge with a time limit of maximum 2 working days.    
Back-end in Python Flask and front-end in Vue.js.  

### Run in Docker
``` bash
docker-compose build
docker-compose up --force-recreate
```
Now visit the application at URL http://localhost:8080

### Run the back-end tests from inside the container
``` bash
docker exec -it backend /bin/bash
python src/Tests.py
```

## Diagram
\
![data_model](diagram.png)