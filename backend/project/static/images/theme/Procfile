uwsgi : nohup uwsgi --socket 127.0.0.1:8000 -w runserver:app &
flask_sockets local : gunicorn -w 4 -b 127.0.0.1:8000 -k flask_sockets.worker --reload runserver:app
socketio local :gunicorn --worker-class eventlet -w 1 runserver:app --reload
nohup gunicorn --worker-class eventlet -w 1 runserver:app --reload -u root -g apache &

flask_sockets remote :nohup gunicorn -w 4 -b 0.0.0.0:8000 -k flask_sockets.worker --reload runserver:app -u root -g apache &
