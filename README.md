## Setup

Install deps:

```
virtualenv -p python3 env
. ./env/bin/activate
pip install -r requirements.txt
```

Start Tika (you can download it from https://cdn.atomshare.net/1dde887fde2644b2f0e0e37ed5ca9c5774144abf/tika-server-1.18.jar):

```
/usr/lib/jvm/java-8-openjdk-amd64/bin/java -jar tika-server-1.18.jar
```

Run migrations:

```
./manage.py migrate
```

Re-index the files:

```
python -m fmapp.update
```

Run the web server:

```
./manage.py runserver
```
