# CatalogApp

It is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Instructions to run this app:

1. Install Vagrant and VirtualBox (Follow instructions from https://www.udacity.com/wiki/ud197/install-vagrant to install and configure)
2. Run vagrant up command followed by vagrant ssh to login
3. Add the CatalogApp folder you downloaded inside the vagrant folder.
4. Change directory in bash using cd /vagrant/CatalogApp
5. Run the following commands to set up database:
    python database_setup.py
6. Run the following command to run this web app on localhost port 5000
    python project.py
Run the application @ http://localhost:5000/categories
