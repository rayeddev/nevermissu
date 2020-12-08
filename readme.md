# Project NeverMissU
## about: 
aiming to help individuals that want to be notified about  the upcoming important happy events for their loved ones and start reciving emails for gifts offers from all over  our partners network based on preferences attached to each person been added so they can pick offers and buy it


## docker
```bash
    ~$ docker build -t nevermissu .
    ~$ docker run -d --name nevermissu_server -p 80:80 nevermissu
```

## docker project test after docker step
```bash
     $ docker exec -it nevermissu_server sh
     $ cd app
     $ pytest
```
