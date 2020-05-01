# SimpleMQ: Lightweight Message Queue

Simple message queue written in Python, using Flask

## Instructions

### Environments

- Python 3.8.1
- Flask 1.1.2

### Make python venv and activate

```bash
# Windows - Git Bash
python -m venv venv
source ./venv/Scripts/activate

# Mac
python3 -m venv venv
source ./venv/bin/activate
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Run Development Server
```
export FLASK_APP=message.py
flask run
```

## API

GET `/{prefix}/status`

```
200 'good'
```

POST `/{prefix}`

```
200 'Done'
```

DELETE `/{prefix}`

```
200 [number of lines]
```


## Etc

### `.env` file example
```
FILE_PATH=data/queue
ROUTES=message/
```

---

written by github.com/ghleokim
