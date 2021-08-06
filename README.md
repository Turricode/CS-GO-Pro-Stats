
# HLTV team and player stats

Due to the lack of an official hltv api, I created this very simple unofficial python version.
It uses flask and mongo but feel free to adapt it for another database.

The reason I did not build the api directly "on top" of the hltv scrapper is beacuase
hltv sends a phorbidden response after only a few requests, so ideally you would update the database daily
by simply ruuning the update fucntion in scrapper/hltv.py



## Installation

First thing you do is clone the repository and install all dependencies

```bash
    https://github.com/Turricode/CS-GO-Pro-Stats 
    cd CS-GO-Pro-Stats
    pip install -r requirements.txt
```

You then need to create a .env file containing your mongo access link

```bash
    touch .env
    echo "DB_CONNECT=<your mongo link>" > .env
```

If you would like to set this up for another type of database you obviously
have to modify DB_CONNECT to whatever is suited

To run the server simply

```bash
    python backend/__init__.py
```
## Updating the data base

In scrapper/hltv.py run 

```python
update_to_db() 

```



  
## API Reference

#### Get player stats

```http
  GET /players/${name}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `player` | `string` | Returns stats for a player  |

#### Get team stats

```http
  GET /teams/${name}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `team`      | `string` | Returns stats for a team |

#### 

```http
  GET /all-players
```
####
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `None`      | `None` | Returns all player names |

####

```http
  GET /all-teams
```
####
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `None`      | `None` | Returns all team names |

####

  