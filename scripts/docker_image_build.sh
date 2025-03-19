if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

repository_name="fastapi-app-graphql"
image_version="1.0.0"

docker build \
 --platform="linux/amd64" \
 --build-arg PYTHON_VERSION=3.12-slim \
 --file=docker/dockerfiles/app.Dockerfile \
 --tag="${repository_name}:${image_version}" .