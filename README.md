# rather-labs-coding-challenge
Product inventory system.

## Prerequisites
`docker` and  `docker compose`

## Build and Run
Using  `docker compose` an etl worker will save data on the database, by default  `100000` records will be created.

1. Build
```bash
make docker-build
```

2. Run
```bash
make docker-up
```

## Execute
Go to  `http://localhost:3060/v1/docs` and make a request.