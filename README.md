# HTTParrot

a simple, configurable echo server. Use POST requests to configure certain responses that will
be returned on subsequent GET requests. Can optionally give a status argument to force a certain
status to return and a delay to artificially delay the response

## Example
### build and run the container
```bash
docker build --tag httparrot:latest .
docker run -d -p 8888:8888 httparrot:latest
```

### set up and request an endpoint
```bash
curl -X POST -d "SOME_DATA" localhost:8888/some/endpoint 
curl localhost:8888/some/endpoint 
``` 

Optionally a status and/or delay query parameter can be provided
```bash
curl -X POST -d "UNAUTHORIZED :(" "localhost:8888/slow_unauthorized?status=401&delay=1.5" 
curl -v localhost:8888/slow_unauthorized
``` 