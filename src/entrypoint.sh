if [ $DEBUG == "TRUE" ]
then
    gunicorn --reload -b 0.0.0.0:8080 -w 3 app:app
else
    gunicorn -b 0.0.0.0:8080 -w 3 app:app
fi
