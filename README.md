# GBFS export engine
New GBFS export service, work with EN data. We can accept files for scooters and bikes

## Local requirements
- docker & docker-compose 
- poetry

## Use docker

```sh
cd [GBFS_EXPORT]
docker-compose build && docker-compose up
```

## GBFS export service commands

You can execute GBFS export service with :

Make POST request on http://0.0.0.0:5000/api/v1/send_gbfs

You have examples of request in gbfs/request_example

## Some elements to read

- `Docker`: https://www.docker.com/<br/>
- `Poetry`: https://www.python-poetry.org/docs/<br/>