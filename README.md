# numerical-methods
Laboratory works on numerical methods

### Let's see...

You can visit [such-a-huge.space](http://such-a-huge.space) to test the labs. 

### How to run by my own

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
docker run --rm -e DEBUG=TRUE -p 8080:8080 -v "$PWD/src:/app" nummethods/web 
```





