# Palautekooderit
Shadow wizard money gang, we love casting spells.

Developement is primarily to be done locally, some testing and production on the server.

## Local Developement

To setup local developement environment
1. Install django and django-extensions
windows:
> pip install django django-extensions
windows, with multiple pythons installed
> python -m pip install django django-extensions
debian
> sudo apt install python3-django python3-django-extensions
2. Clone the repo
3. change palautekooderit/palautekooderit/secretKey_template.py to palautekooderit/palautekooderit/secretKey.py and fill it.
    - If you are one of us, you can grab the key, or the entire file, from the server.
4. Profit???

to run the local server use
> python manage.py runserver 0:80
in palautekooderit folder

## Navigating the server

The server is running two instances of the app.
Production and Dev are separated, and you can ofcourse also run local instanses to test things.
Both instances are git repos, and can pull updates from github. There is no push configured, as that would need credentials. I don't know about you but I don't want my git keys on a quick-school project server with insecure dev environment running most of the time. 

**You can make quick modification on the dev server if you want to. To commit them you then need to copy the changes over to your local machine.**

### Production
Production in /var/www/palautekooderit
This one is running trough apache, on ports 80 and 443.
80 is automatically redirected to 443, because we are secure ☃
Since this is intended for production, it is meant to only hold production code. Ideally testing is done with the dev instance.
When we update code here we need to refresh apache sometimes. To do that you can use:
> sudo systemctl restart apache2.service
To use the production environment navigate to [ankkapeli.fi](https://ankkapeli.fi)

To load the newest main branch from git use:
> cd /var/www/palautekooderit; sudo git checkout main; sudo git pull; cd
- sudo is needed because this folder technically belongs to root.

### Dev
Dev is in /home/azureuser/palautekooderit.
Dev is running with `manage.py runserver` on port 8080.
Remeber that there is no real security here. So do not use passwords you would use anywhere else ever here.
This is mean to hold testing code. Ideally we would develope locally and then only test here, since we only have one server to split between us. We could if we really wanted to spin up more dev instanses but the server is slow as is 😅
There shouldn't be a need to restart the server, but because computers are computers there surely will be. To do that you can use:
> sudo systemctl restart django.service
To use the dev environment navigate to [ankkapeli.fi:8080](http://ankkapeli.fi:8080) WITH HTTP, no https here.

To load the newest main branch from git use:
> cd ~/palautekooderit; git checkout main; git pull; cd
- you can change the branch to something else than main too.

## Repo notes
We have some special files in the repo.  
`django.service` -> service file used to run the dev server.
`wsgi.conf`-> configures wsgi for apache.
These two files need to be, and are, in their respective configuration folders on the server. There is also a virtual host config for the apache server which is not included in the repo, as it is just stock + certbot modifications.
