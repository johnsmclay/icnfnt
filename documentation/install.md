This is still beign written. Don't judge me. It'll be done before I release it.

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

# other stuffs we may need for daemonizing and other stuffs. No worries yet.
#sudo apt-get install python-virtualenv
#pip install wsgi
#pip install wsgicontainer
#pip install tornado
#pip install python-daemon

```
###Setting up the code
```bash
# We need a directory for the code.  I'm going to put it in /srv/icnfnt.
APP_DIR='/srv/icnfnt'
# We also need a user that will be running the application and updating the code, for now I'll use my current user
APP_USER=$(whoami)
# Let's create the directory and set the permissions
sudo mkdir $APP_DIR
sudo chown -R $APP_USER:$APP_USER $APP_DIR
sudo chmod -R 764 $APP_DIR
# Install git if you don't already have if (If you don't....feel my judgement)
sudo apt-get install git
# clone the repository
sudo git clone git://github.com/johnsmclay/icnfnt.git $APP_DIR

```