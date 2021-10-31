# Challenge for ClicOh

## Running with docker

### Pre-requisites:
- docker
- docker-compose

### Steps
1. Create a file called `.env` with environment variables
2. Build with `docker-compose build`
2. Run with `docker-compose up`

### How to use
1. In terminal run: 
   - `docker-compose exec web python manage.py migrate` 
   - `docker-compose exec web python manage.py createsuperuser`
   - `Go to http://localhost:8000/`
