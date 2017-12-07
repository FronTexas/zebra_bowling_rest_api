# zebra_bowling_rest_api

# Setup

First, you need to create the database by running this command:

```
python manage.py migrate 
```


Then you can start the server by running this command:
 
 ```
 python manage.py startserver
 ```

# REST HTTP Request

After the server started you can do `GET`on `/bowling_game/` to either start a game or get the most updated  `frames` 

`frames` is an array of `Frame` which is a JSON object that contains four fields:  `first_throw_score`, `second_throw_score`, `third_throw_score`, and `total_score`

Do a `POST` on `/bowling_game/` to throw a bowling ball which will update the game's `frames`




