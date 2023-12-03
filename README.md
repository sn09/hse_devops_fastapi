# hse_devops_fastapi

Run FastAPI service:  

```
uvicorn main:app
```  

Run docker container
```
docker run -d -p 5555:5555 --name fastapi_service saraevn/hse_devops_fastapi_service
```

Interactive documentation is available at `/docs` endpoint.  

Authors:
* Saraev Nikita