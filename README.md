## uwsgi-env
Usually, we use uWSGI to deploy Flask WebAPIs on Linux Ubuntu.

Each API might be deployed with different Python virtual environment.

The uWSGI `Emperor` allows each API to be loaded with its own dedicated Python virtual environment.

## Installation
<pre lang="python">
  pip install uwsgi
  pip install flask
</pre>
<pre lang="bash">
  sudo apt-get update
  sudo apt-get upgrade
  sudo apt-get install nginx
</pre>

## Deployment
1. Create `App1.ini` and `App2.ini` in the `vassals` folder.

App1.ini
<pre lang="bash">
[uwsgi]
socket = /tmp/app1.socket
chdir = /Users/user/uwsgi-env/APP1
module = App1:app
;virtual environment
home = /Users/user/uwsgi-env/APP1/python_env

chmod-socket = 660
vacuum = true
master = true
processes = 2
threads = 2
</pre>

App2.ini
<pre lang="bash">
[uwsgi]
socket = /tmp/app2.socket
chdir = /Users/user/uwsgi-env/APP2
module = App2:app
;virtual environment
home = /Users/user/uwsgi-env/APP2/python_env

chmod-socket = 660
vacuum = true
master = true
processes = 2
threads = 2
</pre>

2. Create `emperor.ini` file, it should load any .ini config file in the `vassals` folder.

emperor.ini
<pre lang="bash">
[uwsgi]
;all app configurations
emperor = /Users/user/uwsgi-env/vassals
die-on-term = true
</pre>

3. Using either `venv` or `virtualenv` to create Python virtual environment in each API folder.

4. Set the app location in each WebAPI.

App1.py
<pre lang="python">
  #import package
  from werkzeug.middleware.dispatcher import DispatcherMiddleware

  #App location
  app = DispatcherMiddleware(None, {
    "/App1": flask_app
  })
</pre>

App2.py
<pre lang="python">
  #import package
  from werkzeug.middleware.dispatcher import DispatcherMiddleware

  #App location
  app = DispatcherMiddleware(None, {
    "/App2": flask_app
  })
</pre>

5. Add WebAPI locations in the NGINX config file, `nginx.conf`.

nginx.conf
<pre lang="bash">
server {
  listen       8080;
  server_name  localhost;

  location / {
      root   html;
      index  index.html index.htm;
  }
  #App1
  location /App1 {
    include uwsgi_params;  #load uWSGI parameters
    uwsgi_pass unix:/tmp/app1.socket;  #pass socket
  }
  #App2
  location /App2 {
    include uwsgi_params;  #load uWSGI parameters
    uwsgi_pass unix:/tmp/app2.socket;  #pass socket
  }
}
</pre>

6. Load all WebAPIs by uWSGI `Emperor` configuration.
<pre lang="bash">
  uwsgi --ini emperor.ini
</pre>

7. Restart NGINX service
<pre lang="bash">
  nginx -s reload
</pre>

8. Try to open WebAPI pages on browser.

App1

<a href="http://127.0.0.1:8080/App1" target="_blank">http://127.0.0.1:8080/App1</a>

App2

<a href="http://127.0.0.1:8080/App2" target="_blank">http://127.0.0.1:8080/App2</a>
