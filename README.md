# Musala Soft Practical Test

## Drones API

### Tech stack used

- [FastAPI](https://fastapi.tiangolo.com/)

- [PostgreSQL](https://www.postgresql.org/)

- [Docker](https://www.docker.com/)

### Build and run

1.  Clone the repo to bootstrap your environment:
    ```bash
    git clone https://github.com/codeshard/drones-api
    cd drones-api
    ```
2.  Create `.env` file (or rename and modify `.env.template`) in project root and set environment variables for application:
    ```bash
    touch .env
    echo DEBUG=False >> .env
    echo PROJECT_NAME=Musala Drones API >> .env
    echo DATABASE_DSN=postgresql://postgres:postgres@postgres:5432/drones >> .env
    echo POSTGRES_DB=drones >> .env
    echo POSTGRES_USER=postgres >> .env
    echo POSTGRES_PASSWORD=postgres >> .env
    ```
3.  Build the app docker container:
    ```bash
    docker-compose build app
    ```
4.  Run the app:

    ```bash
    docker-compose up -d
    ```

5.  Check the running app

    Open your browser at [http://localhost:8000/docs](http://localhost:8000/docs) to check the [Swagger](https://swagger.io/) API Docs

### Available Endpoints

1. Drones:

![Drones Endpoints](drones/docs/drones.png "Drones Endpoints")

2. Medications:

![Medications Endpoints](drones/docs/medications.png "Medications Endpoints")

3. Deliveries:

![Deliveries Endpoints](drones/docs/deliveries.png "Deliveries Endpoints")

### Functionality Check

- Register a drone: make a **post** request to [http://localhost:8000/drones](http://localhost:8000/drones) with the following params:

```json
{
    "serial_number": string(required),
    "weight_limit": float, max:500(required),
    "battery_capacity": float, max: 100(required),
    "model": int value (1: lightweight, 2: middleweght, 3: cruiserweight, 4: heavyweight),
    "state": int value (1: idle, 2: loading, 3: loaded, 4: delivering, 5: delivered, 6: returning),
}
```

- Update a drone: make a **patch** request to [http://localhost:8000/drones/{drone-id}](http://localhost:8000/drones/{drone-id}) with one of the following params:

```json
{
    "serial_number": string,
    "weight_limit": float, max:500,
    "battery_capacity": float, max: 100,
    "model": int value (1: lightweight, 2: middleweght, 3: cruiserweight, 4: heavyweight),
    "state": int value (1: idle, 2: loading, 3: loaded, 4: delivering, 5: delivered, 6: returning),
}
```

- Drone details: make a **get** request to [http://localhost:8000/drones/{drone-id}](http://localhost:8000/drones/{drone-id})

- Delete a drone: make a **post** request to [http://localhost:8000/drones/{drone-id}](http://localhost:8000/drones/{drone-id})

- Register a medication: make a **post** request to [http://localhost:8000/medications](http://localhost:8000/medications) with the following params:

```json
{
  "name": string(required),
  "weight": float, min:0(required),
  "code": string(required),
  "image": string(required)
}
```

- Update a medication: make a **patch** request to [http://localhost:8000/medications/{medication-id}](http://localhost:8000/medications/{medications-id}) with one of the following params:

```json
{
  "name": string,
  "weight": float, min:0,
  "code": string,
  "image": string
}
```

- Medications details: make a **get** request to [http://localhost:8000/medications/{medications-id}](http://localhost:8000/medications/{medications-id})

- Delete a medication: make a **post** request to [http://localhost:8000/medications/{medications-id}](http://localhost:8000/medications/{medications-id})

- Loading a drone with medication items: make a **post** request to [http://localhost:8000/deliveries](http://localhost:8000/deliveries) with the following data:

```json
{
  "drone_id": UUID of a drone,
  "medications": [UUIDs of medications, comma separated]
}
```

- Check loaded medication items for a given drone: make a **get** request to [http://localhost:8000/deliveries/medications/{drone-id}](http://localhost:8000/deliveries/medications/{drone-id)

- Check available drones for loading: make a **get** request to [http://localhost:8000/deliveries/drones-avaliables](http://localhost:8000/deliveries/drones-availables)

- Check drone battery level for a given drone: Plz refer to _Drone details_ endpoint.

- Every 30 mins run a periodic tasks that check every drone available, and stores the drone ID and the battery level in a table called _auditory_, [here is the task](https://github.com/codeshard/drones-api/blob/d52ebc81d29daafb7fbbee11c9cb3c556f6972ab/drones/app/routers/drones.py#L13)

### Run tests

In order to be able to run the tests, you should do:

```bash
docker-compose up -d
docker-compose exec app pytest -vvv
```
