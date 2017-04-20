# Nuevo M&eacute;xico

Nuevo M&eacute;xico is a simple RESTful web application. Use it to learn more about New Mexico.


## Details

Nuevo M&eacute;xico is written in Python and uses the Flask framework. The application employs third-party OAuth authentication (Google+ and Facebook) and uses the object-relational mapping tool SQLAlchemy to interact with a SQLite database. Styling is implemented with the aid of Bootstrap.

The backbone of Nuevo M&eacute;xico is a database with three tables: a `PlaceType` table for storing information about categories of places to visit in New Mexico (e.g. pueblos, restaurants, parks and monuments), a `Place` table for documenting information about specific places to visit in the state (e.g. Acoma Pueblo or Orlando's New Mexican Cafe), and a `User` table for storing a small amount of data related to each user.

When logged in, users can view, create, edit and delete items in the application; users are only able to edit and delete items they created. When not logged in, users are only able to view content.

Nuevo M&eacute;xico provides JSON API endpoints allowing users to access data that is easily serializable. A user has three options: access a list of all the place types in the application, access a list of all the place items within a specific place type and access data for an individual place item.

The application includes a number of files and directories, including application.py, the application itself; database_setup.py, which creates an SQLite database called nuevomexico.db; populator.py, which is used to load the database with data; a directory named templates, which contains 14 html pages; and a directory called static, which holds CSS files as well as a directory for images. The repository also includes a config.json file, which is part of the Bootstrap framework.


## Install instructions

Nuevo M&eacute;xico can be installed by cloning the Nuevo M&eacute;xico repository on GitHub:

`$ git clone https://github.com/bencam/nuevo-mexico.git`


## Usage

Please note that Nuevo M&eacute;xico will not run unless a user has SQLAlchemy and SQLite installed and configured on their machine.

The first step to running Nuevo M&eacute;xico is to set up the database. To do this, change to the local directory containing the Nuevo M&eacute;xico repository and run the database_setup.py file.

`$ python database_setup.py`

This will create an SQLite database in the working directory called nuevomexico.db.

Note: the repository includes a file called database_setup_postgres.py. Use this file for creating a PostgeSQL database. If using PostgreSQL, either (a) the name of the database_setup_postgres.py file will need to be changed to database_setup.py (and therefore the original database_setup.py file will need to be renamed, moved to another directory, or deleted) or (b) the import lines for the database_setup file in application.py and populator.py will need to be changed to database_setup_postgres.

Next, populate the databa    se by running the populator.py file.

`$ python populator.py`

The next step is to implement the Google+ login. Do this by creating a new project on the Google API Console. Create a OAuth Client ID (under the Credentials tab), and make sure to add http://localhost:8000 as an authorized JavaScript origin and http://localhost:8000/login, http://localhost:8000/gconnect and http://localhost:8000/oauth2callback as authorized redirect URIs. Google will provide a client ID and client secret for the project. Download the JSON file, move it to the local Nuevo M&eacute;xico directory and rename the file client_secrets.json. Add the client ID to line 16 of the login.html file in the local directory.

Next, implement the Facebook login by creating a new app at [Facebook for Developers](https://developers.facebook.com/). Make http://localhost:8000/ the site URL. Add the "Facebook Login" project, and put http://localhost:8000/ as the authorized redirect URI. Within the local directory containing the Nuevo M&eacute;xico repository, create a file called fb_client_secrets.json. Insert the following:

`{
	"web": {
		"app_id": "INSERT_APP_ID",
		"app_secret": "INSERT_APP_SECRET"
	}
}`

Finally, add the Facebook App ID to line 61 of the login.html file in the local directory.

With the third-party authentication in place, start up the application.

`$ python application.py`

With application.py running, open a browser and navigate to: http://localhost:8000

A landing page will load, and users will be given the option to enter the main part of the site. Users will then be able to view the content within the database or login and view the content as well as create, edit and delete new items.

Users can access the JSON API endpoints by using the URLs below.

Access a list of all the place types in the application: http://localhost:8000/placetype/JSON/

Access a list of all the place items within a specific place type: http://localhost:8000/placetype/INSERT_PLACE_TYPE_ID/place/JSON/

Access data for an individual place item: http://localhost:8000/placetype/INSERT_PLACE_TYPE_ID/place/INSERT_PLACE_ID/JSON/


## SOURCES

I relied very heavily on a set of Udacity course videos and examples for the code in the application.py, the database_setup.py, and the populator.py files as well as the html files in the templates directory. I also relied on the Udacity forums (see [here](https://discussions.udacity.com/t/conditional-styling-problems/185662) for example).


## License

Nuevo M&eacute;xico is released under the [MIT License](http://opensource.org/licenses/MIT).
