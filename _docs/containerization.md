# Containerization / docker image

## Build the docker image

docker image is built with the `scripts/docker_image_build.sh` script.

```bash
./scripts/docker_image_build.sh
```

you can change image name and version in the `scripts/docker_image_build.sh` file.

## Run the docker image

```bash
# with nginx server
docker run -d -p 80:80 fastapi-app:1.0.0
# or directly with fastapi server
docker run -d -p 8000:8000 fastapi-app:1.0.0
```

## Stop the docker image

```bash
docker stop <container_id>
```

## Remove the docker image

```bash
docker rmi fastapi-app:1.0.0
```
