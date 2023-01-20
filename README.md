# URL Counter
API to count the number of hits in given URLs.

## Installation
Just run docker compose to start the application. The endpoint should be available at `http://localhost:5000`.
```bash
$ docker-compose up -d
```

## Testing
To run the tests (unit and integration), just run the following command:
```bash
$ make test
```

## Checking and Fixing Python Code Style
Mypy:
```bash
$ make check-mypy
```

Flake8:
```bash
$ make check-flake8
```

ISort:
```bash
$ make check-isort
$ make fix-isort
```

Black:
```bash
$ make check-black
$ make fix-black
```

The coverage will also run. This project has around 98% coverage.

## Design and Architecture Decisions

- The application is organized following the Clean Architecture. The main idea is to separate the business logic from the framework and infrastructure;
- The Docker is organized in a way that the build is multi-stage. This way is easier to rerun builds from succeeded checkpoints;
- I'm separating the unit tests from the integration tests. Basically, the difference is that the integration tests connect to the database;
- To increment the values, I chose to use the Redis `Sorted Set` data structure. According to the [documentation](https://redis.io/docs/data-types/sorted-sets/), it has more fit to solve the problem of counting strings. Also, most of the operations has time complexity of O(log(N)), which is good for this kind of problem;
- The application is using the `uwsgi` as WSGI server. It can handle multiple requests from more than one source at the same time;
- If I had more time, I'd like to add a pagination feature, so the user can get the top 10, 20, 30, etc. URLs;

## More Information
I took around 3h30 to 4h to complete this test.