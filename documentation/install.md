This is still beign written. Don't judge me. It'll be done before I release it.

##Ubuntu (this was done on 12.04)
###Setting up the dependancies
```bash
# Package manager for Python. You can use easy_install, but I am assumimg it's pip.
sudo apt-get install python-pip
# Fontforge is what does the heavy lifting and they have a python interface to issue commands.
sudo apt-get install python-fontforge
# flask is the framework we are using
pip install Flask
sudo apt-get install python-virtualenv
pip install wsgi
pip install wsgicontainer
pip install tornado
pip install python-daemon
# For zipping up the font packages
apt-get install zip
```
###Setting up the code
```bash
# We need a directory for the code.  I'm going to put it in /srv/icnfnt.
APP_DIR='/srv/icnfnt'
# Let's create the directory and set the permissions
sudo mkdir $APP_DIR
sudo chmod -R 664 $APP_DIR
# clone the repository
git clone git://github.com/johnsmclay/icnfnt.git $APP_DIR

```