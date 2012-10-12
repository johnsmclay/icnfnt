##Ubuntu (this was done on 12.04)
###Setting up the dependancies
```bash
# Package manager for Python. You can use easy_install, but I am assumimg it's pip.
sudo apt-get install python-pip
# Fontforge is what does the heavy lifting and they have a python interface to issue commands.
sudo apt-get install python-fontforge
# flask is the framework we are using
sudo pip install Flask
# For zipping up the font packages
sudo apt-get install zip
```
###Setting up the code
```bash
# We need a directory for the code.  I'm going to put it in /srv/icnfnt.
APP_DIR='/srv/icnfont'
# We also need a user that will be running the application and updating the code, for now I'll use my current user
APP_USER=$(whoami)
# Let's create the directory and set the permissions
sudo mkdir $APP_DIR
sudo chown -R $APP_USER:$APP_USER $APP_DIR
sudo chmod -R 750 $APP_DIR
# Install git if you don't already have if (If you don't....feel my judgement)
sudo apt-get install git
# clone the repository
git clone git://github.com/johnsmclay/icnfnt.git $APP_DIR

```

###Running the code (Basic)
```bash
cd $APP_DIR
cp icnfnt.cfg.basic_example icnfnt.cfg
export ICNFNT_CONFIG=$APP_DIR/icnfnt.cfg
python icnfnt.py
```
you should see the following:
```bash
 * Running on http://0.0.0.0:5000/
 * Restarting with reloader
```
This means the code is running in debug mode.
In debug mode you can go to http://ip_or_name_of_your_box:5000/index.html and everything should work.

###Running the code (Production)
```bash
# A better python web server than the built-in one (threading, etc.)
sudo pip install tornado
# Used to Daemonize the process
sudo pip install python-daemon
# Create a place for Tornado to log to
sudo mkdir /var/log/tornado/
# Allow Tornado to log to it
sudo chown root:$APP_USER /var/log/tornado
sudo chmod 770 /var/log/tornado
# Copy the init.d script out of the management dir
sudo cp management/icnfnt-tornado /etc/init.d/
# Allow it to execute
sudo chmod +x /etc/init.d/icnfnt-tornado
# NOTE: be sure and change the APP_DIR in the init.d script to match yours
# Swap the config file to the production one
mv icnfnt.cfg icnfnt.cfg.basic_example
cp icnfnt.cfg.production_example icnfnt.cfg
sudo /etc/init.d/icnfnt-tornado start
```

###Using with a web server (Production)
You usually don't want your static files served by python so I set up Nginx to serve up the static files and pass the rest back to python.
```bash
sudo apt-get install nginx
sudo rm /etc/nginx/sites-enabled/default
sudo vim /etc/nginx/sites-available/icnfnt

# Paste in the following and edit to match your settings:
###########################
server {
        client_max_body_size 20M;
        listen 80;
        # A list of DNS entries this will respond to, you can omit it to accept any DNS entry or IP
        server_name icnfnt.com www.icnfnt.com;

        root    /srv/icnfnt/static/;

        # Everything in this directory will be passed back to python
        location /api {
                proxy_set_header X-Real-IP  $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                # change localhost:5000 to the ip/name and port your python is listening on
                proxy_pass http://localhost:5000;
                allow all;
        }

        # A status page for management
        location /nginx_status {
                stub_status on;
                access_log   off;
                # Allow addresses or subnets to access the status page
                allow 10.0.0.0/8;
                allow 172.16.0.0/12;
                allow 192.168.0.0/16;
                deny all;
        }
}
###########################

# Enable the site we just created
sudo ln -s /etc/nginx/sites-available/icnfnt /etc/nginx/sites-enabled/icnfnt
# Allow Nginx to read the files (it runs as www-data)
sudo chown -R $APP_USER:www-data $APP_DIR
# To apply the changes
sudo service nginx reload
```

Go to http://ip_or_name_of_your_box  
Do a little dance...make a little love...get down tonight.

