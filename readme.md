# Project NeverMissU
## about: 
aiming to help individuals that want to be notified about  the upcoming important happy events for their loved ones and sending them gifts offers from all over the our partners network based on preferences attached to each person he adds


## docker
```bash
    ~$ docker build -t nevermissu .
    ~$ docker run -d --name nevermissu_server -p 80:80 nevermissu
```

## docker project test after docker step
```bash
    ~$ docker build -t nevermissu .
    ~$ docker exec -it nevermissu_server sh
     $ cd app
     $ pytest
```