# Musala Soft Practical Test


## Drones API
 

### Tech stack used


- [FastAPI](https://fastapi.tiangolo.com/)

- [PostgreSQL](https://www.postgresql.org/)

- [Docker](https://www.docker.com/)

### Build and run

 1. Create an *.env* file in the root folder of the project, plz, check [.env.template](https://github.com/codeshard/drones-api/blob/1324b20dc1c8fd097c49ce5da68c2b8c51968854/.env.template) file

### Tests
In order to be able to run the tests, you should do:
```bash
docker-compose up -d
docker-compose exec app pytest
```