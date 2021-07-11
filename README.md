# File uploading app

This is an application for uploading files to the server.
Uploading progress you can see in CLI.

## build and run containers

```bash
mkdir files
docker-compose up -d --build
```

This will expose fastapi application on 8000 and celery flower on 5555

swagger docs - `http://localhost:8000/docs`

redoc - `http://localhost:5000/redoc`

celery flower - `http://localhost:5555`
