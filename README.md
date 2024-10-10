# Mafia Game
This project is a simple web app to facilitate a game of Mafia. It handles role assignment and aids the facilitator to keep track of everyone's roles.

Eventually, it will have features to help Mafia members keep track of their accomplices, help the facilitator keep track of which players have been eliminated and much more to come.

## Getting the project running
You need Python installed, along with Django.

After cloning the project, navigate to the directory with the `manage.py` file, open a command prompt and run `python manage.py makemigrations` and then `python manage.py migrate`
This will create the database with the necessary tables. NOTE: no roles are inserted into the database by default, but the game needs roles to exist before it can work. There is exception handling code to populate the roles if none are found

To run the project, simply run the following command, but replace <localip> with your computer's IP address on the local network `python manage.py runserver localip:8000`.
When the server is up and running, you can enter it's IP address and the specified port number (:8000 in this case) in the browser of any device that is connected to the same network.

## Contributing to the game
Any suggestions for improvements are welcome. Most of the game logic sits in the web_ui/views.py file. 

For changes to the UI, navigate to the web_ui/templates/web_ui directory (This is Django's convention for folder structure). The pages in here are what gets displayed to the user. These are Jinja2 template syntax. 

To add new endpoints (URLS), you need to create a function in web_ui/views.py that accepts a request object as a parameter, then navigate to web_ui/urls.py and add an additional path that points to your new function.
