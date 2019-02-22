# numerical-methods
Laboratory works on numerical methods

### How to start

Well, I hope you like docker. In this case, all you need is to run the following:

```
docker build -t nummethods/web ./ 
```
and then...
```
docker run -p 8080:8080 nummethods/web  
```
In case of development you should extend the command:

```
docker run --rm -e DEBUG=TRUE -p 8080:8080 -v app:/app nummethods/web  
```



