# Flavor sync

The Flavor synchronization tool provides a backend system for a marketplace
of OpenStack flavors. This project is part of [FIWARE](http://www.fiware.org/).

## Table of contents

* [Overall description](#overall-description)
* [Features implemented](#features-implemented)
* [Installation](#installation)
	* [Software Requirements](#software-requirements)
	* [Installation steps](#installation-steps)
	* [Configuration](#configuration)
	* [Installation verification](#installation-verification)
* [Running](#running)
	* [Running in development mode](#running-in-development-mode)
	* [Deploying in production mode](#deploying-in-production-mode)
* [API specification](#api-specification)
* [License](#license)

## Overall description

In a OpenStack multi cloud environment the use of several types of flavors can
be hard to manage. Flavors with different names can offer similar
configurations. From a user perspective, the use of the same flavors in the 
different infrastructures could ease the operations.

In order to solve this problem, the Flavor synchronization tool has been
developed. In conjunction with the Fi-Dash component, it will allow the
infrastructure managers to publish the information of their private flavors, as
well as to install in the own infrastructure other published flavors. Moreover,
they will be able to perform the regular OpenStack flavor management operations,
such as create, modify and delete.

In addition, the capability of having "promoted" flavors is also supported. They
are recommended flavors, flavors that should exist in every node. The idea
behind the promoted flavors is to homogenize the user experience. Although all
infrastructures have a similar set of flavors, the existence of a large number
of them can lead to a situation of confusion on which to use. By offering a
small range of promoted flavors, the user and services using the platform can
better choose the one that fits the best to their needs.

This is accomplished exposing a REST API that provides a very similar set of
operations and data structures that the OpenStack one, so it can be easily 
integrated with existing applications that use the
[OpenStack REST API](http://developer.openstack.org/api-ref-compute-v2.1.html#os-flavors).

This is a work in progress. At the moment, the remaining issues include the
implementation of the authentication system, the integration of with the FiWare
infrastructure and proper testing.

## Features implemented

The complete requirement list of this version (v0.8 beta, at the moment) is the
following one:

* An infrastructure operator registers his infrastructure in the Flavor
synchronization tool.
* An infrastructure operator lists all the available flavors in his
infrastructures.
* An infrastructure operator gets the details of one of the flavors in his
infrastructure.
* An infrastructure operator creates a new flavor in his infrastructure.
* An infrastructure operator updates a in his infrastructure.
* An infrastructure operator deletes a in his infrastructure.
* An infrastructure operator gets a list of the “promoted” flavors.
* An infrastructure operator gets a list of the public flavors.
* An infrastructure operator “installs” one of the public flavors into his
infrastructure.
* An infrastructure operator publishes one of his private flavors.
* A Fiware operator makes promotes one of the public.

## Installation

### Software requirements

The requirements to install a working copy of the Flavor synchronization tool are:

* Python 3
* Python 3 Virtualenv
* Python 3 Pip

### Installation steps

The Flavor synchronization tool is a Python web application that uses the
[Flask microframework](http://flask.pocoo.org/). The general recommendations
when running Python applications is to use Virtualenv.

The Python virtual environments is a way to run isolated Python environments
with different default Python version and libraries. This, for example, allows
two run two different Python applications that rely on some common library but
use different versions of it.

Pip is the package installer of Python. It allows to easily search, install and,
in general, manage Python libraries. It also provides automatic dependency
resolution and is able to generate and read requirements files. This file 
lists the libraries needed to be installed in order to execute the app.

The list of steps to get the Flavor synchronization tool installed is the
following:

1. Install virtualenv

		$ pip3 install virtualenv

2. Create virtualenv

		$ virtualenv-3.x $VIRTUALENV_NAME (where 3.x is the version of Python 3 installed)

3. Activate virtualenv

		$ . $VIRTUALENV_NAME/bin/activate

4. Change to application directories and install requirements

		($VIRTUALENV_NAME)$ cd $FLAVOR_SYNC_DIR
		($VIRTUALENV_NAME)$ pip install -r requirements.txt


#### Download the project

Clone the project using git from the
[Flavor sync repository](https://github.com/Atos-FiwareOps/flavor-sync.git)

	$ git clone https://github.com/Atos-FiwareOps/flavor-sync.git

#### Creating the MySQL database

This project is database engine agnostic. [SQLAlchemy](http://www.sqlalchemy.org/)
is used as ORM system, so any database engine system supported could be used.
Anyway, we tested it with MySQL, so the following instructions explains how to
set up the project with this engine.

From mysql command tool, create a database (with a user with sufficient 
privileges, as root):

	$ mysql -p -u root 
	
	mysql> CREATE DATABASE fiwareflavorsync;

Create a user:

	mysql> CREATE USER flavorsync@localhost IDENTIFIED BY 'yourpassword';
	mysql> GRANT ALL PRIVILEGES ON fiwareflavorsync.* TO flavorsync@localhost; -- * optional WITH GRANT OPTION;

The Flavor synchronization tool webapp will create all the needed tables when
loaded by first time.

The names used here are the default values. See [configuration](#configuration) 
to know how to change the values.

### Configuration

The Flavor synchronization tool needs minimal configuration, basically the
parameters to connect to the database. The first step after cloning the code is
to copy the config.py.sample file to config.py.sample (you can find this file
in the $PROJECT_DIR/flavorsync/ directory). The parameter that can be adjusted
are:

* dbhost: the hostname, URI or IP to connect to the database.
* dbuser: the username that will have permissions to use the Flavor synchronization tool database.
* dbpass: the password for that user.
* dbname: the name of the database for the Flavor synchronization tool.

## Running

Flask offers a lightweight embedded server for development purposes. It allows
to run quickly the application without having to worry about production server
configurations. It also allows, in combination with other Python tools, to debug
the running app, as well as automatic reloading when the code changes (so stop
and start it is not needed when a change is performed in the code). Anyway,
this is not recommended for production environments.

In that case, several web server projects allow the deployment and run of Python
code. For example, when using other application servers, Apache and Nginx can
be used. Since the combination possibilities are large, we will explain here one
we have tested. It is based on Nginx, Gunicorn and Supervisor, running on a
Debian stable Linux distribution. Please, feel free to send us feedback about
other possible configurations.

### Running in development mode

Runnin the Flavor synchronization tool using Flask development server is easy.
Please, take into account that to run it, the database system must be running
and properly configured as stated before. If this have been done, follow the
following steps:

1. Activate virtualenv

		$ . $VIRTUALENVS_NAME/bin/activate

2. Change to the application directory

		($VIRTUALENV_NAME)$ cd $PROJECT_DIR

3. Start server

		($VIRTUALENV_NAME)$ python runserver.py

	The default URL served by the server is http://127.0.0.1:5000/. You can find
	more information about the development server in the [Flask documentation webpage](http://flask.pocoo.org/docs/0.10/).

4. Test

		$ curl http://localhost:5000/v1/flavors

### Deploying in production mode

As mentioned before, several deployment configurations are possible. In this
section we described how we deployed this in a production environment using
Debian 8, Nginx, Gunicorn, Supervisor and Virtualenv.

We suppose that you have performed the installation steps and you have set up a
virtual environment for the project.

We also suppose those global variables:

* $PROJECT_DIR: the directory the Flavor synchronization tool code has been placed.
* $VIRTUALENV_DIR: the directory where the dedicated virtual 
environment for the Flavor synchronization tool resides.

Most of the scripts have are based on [Michał Karzyński](https://gist.github.com/postrational)
Gist examples on [how to set up Django on Nginx with Gunicorn and supervisor](https://gist.github.com/postrational/5747293#file-gunicorn_start-bash) and on the
[Flask documentation](http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/#gunicorn)

The steps are the following:

1. Install the dependences

		$ sudo pip3 install virtualenv
		$ sudo aptitude install nginx gunicorn supervisor

2. Create a Gunicorn start script

	This script can be placed wherever you want. In our case, we placed it in
	$PROJECT_DIR/bin/gunicorn_start.

		#!/bin/bash

		NAME="flavorsync"                    # Name of the application
		PROJECTDIR=$PROJECT_DIR              # Project directory
		SOCKFILE=$PROJECT_DIR/gunicorn.sock  # we will communicate using this unix socket
		USER=root                            # the user to run as
		GROUP=root                           # the group to run as
		NUM_WORKERS=3                        # how many worker processes should Gunicorn spawn
		
		# Activate the virtual environment
		cd $PROJECT_DIR
		source $VIRTUALENV_DIR/bin/activate
		export PYTHONPATH=$PROJECT_DIR:$PYTHONPATH
		
		# Create the run directory if it doesn't exist
		RUNDIR=$(dirname $SOCKFILE)
		test -d $RUNDIR || mkdir -p $RUNDIR
		
		# Start your Flask Unicorn
		# Programs meant to be run under supervisor should
		#   not daemonize themselves (do not use --daemon)
		exec $VIRTUALENV_DIR/bin/gunicorn ${NAME}:app \

		  --name $NAME \
		  --workers $NUM_WORKERS \
		  --user=$USER --group=$GROUP \
		  --bind=unix:$SOCKFILE \
		  --log-level=debug \
		  --log-file=-

3. Create the Supervisor script to start/stop the application:

	It should be placed in /etc/supervisor/conf.d/flavorsync.conf and should
	contain the following parameters:

		[program:flavorsync]
		command = $PROJECT_DIR/bin/gunicorn_start                   ; Command to start app
		user = root                                                 ; User to run as
		stdout_logfile = $PROJECT_DIR/logs/gunicorn_supervisor.log  ; Where to write log messages
		redirect_stderr = true                                      ; Save stderr in the same log
		environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8 

4. Create Nginx virtual servers

	This script should be placed in /etc/nginx/sites-available/flavorsync

		upstream flavorsync_app_server {
		  # fail_timeout=0 means we always retry an upstream even if it failed
		  # to return a good HTTP response (in case the Unicorn master nukes a
		  # single worker for timing out).

		  server unix:$PROJECT_DIR/gunicorn.sock fail_timeout=0;
		}

		server {
			listen   0.0.0.0:80;
			server_name localhost {public_ip};

			client_max_body_size 4G;

			access_log $PROJECT_DIR/logs/nginx-access.log;
			error_log $PROJECT_DIR/logs/nginx-error.log;

			location / {
				# an HTTP header important enough to have its own Wikipedia entry:
				#   http://en.wikipedia.org/wiki/X-Forwarded-For
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

				# enable this if and only if you use HTTPS, this helps Rack
				# set the proper protocol for doing redirects:
				# proxy_set_header X-Forwarded-Proto https;

				# pass the Host: header from the client right along so redirects
				# can be set properly within the Rack application
				proxy_set_header Host $http_host;

				# we don't want nginx trying to do something clever with
				# redirects, we set the Host: header above already.
				proxy_redirect off;

				# set "proxy_buffering off" *only* for Rainbows! when doing
				# Comet/long-poll stuff.  It's also safe to set if you're
				# using only serving fast clients with Unicorn + nginx.
				# Otherwise you _want_ nginx to buffer responses to slow
				# clients, really.
				# proxy_buffering off;

				# Try to serve static files from nginx, no point in making an
				# *application* server like Unicorn/Rainbows! serve static files.
				if (!-f $request_filename) {
					proxy_pass http://flavorsync_app_server;
					break;
				}
			}
		}

5. Start/restart the application using supervisor:

		$ sudo supervisorctl restart flavorsync

6. Add the virtual server for the Flavor synchronization tool to the directory of
enabled sites and restart Nginx:

		$ sudo ln -s /etc/nginx/sites-available/slagui /etc/nginx/sites-enabled
		$ sudo systemctl restart nginx.service 

## Installation verification

To check that everything was correctly installed, run the project in development
mode and perform the following HTTP call:

		$ curl http://localhost:5000/v1/flavors

It should return an empty JSON list.

## Configure the users and roles

The file initial_data.json has created automatically the groups CONSUMER AND
PROVIDER when you have executed "python manage.py syncdb".

You only need to create the users and the providers associated to the agreements
and to assign the correct role (CONSUME and PROVIDER).

In order to introduce them you have to connect to http://localhost:8000/admin
and add the new users (with CONSUME or PROVIDER groups).

## API specification

Note: there is an [Apiary version](http://docs.fiwareflavorsync.apiary.io/)
of this page with a more readable and structured format, as well as a
mock server to perform some tests at.

### Group Infrastructures

#### Infrastructure Collection [/v1/infrastructures]

##### Register a new infrastucture [POST]

Allows to create a new infrastructure. It takes a XML or JSON body containing
the name, endpoint url of nova.

+ name (string) - The name of the of the infrastructure
+ nova_url (string) - URL where the Nova API can be reached
+ keystone_url (string) - URL where the Keystone API can be reached
+ username (string) - Username for authenticating in Keystone
+ password (string) - Password for authenticating in Keystone
+ tenant (string) - Tenant name to be managed

+ Request (application/xml)

    + headers
    
            user: basic authentication user
            password: basic authentication password

    + body
            
            <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <infrastructure>
                <name>Mordor</name>
                <nova_url>http://11.22.33.44:8776/</nova_url>
                <keystone_url>http://55.66.77.88:35357/</keystone_url>
                <username>myUsername</username>
                <password>myPassword</password>
                <tenant>myTenant</tenant>
            </infrastructure>

+ Response 201 (application/xml)

    + Body

            <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <infrastructure>
                <name>Mordor</name>
            </infrastructure>

+ Request (application/json)

    + headers
    
            user: basic authentication user
            password: basic authentication password

    + body
            
            {
                "infrastructure": {
                    "name": "Mordor",
                    "nova_url": "http://11.22.33.44:8776/",
                    "keystone_url": "http://55.66.77.88:35357/",
                    "username": "myUsername",
                    "password": "myPassword",
                    "tenant": "myTenant"
                }
            }

+ Response 201 (application/json)

    + Body

            {
                "infrastructure": {
                    "name":"Mordor"
                }
            }

+ Response 400

        Returned when incorrect data has been suplied.

+ Response 409

        Returned when the uuid or name already exists in the database.

#### Infrastructure [/v1/infrastructures/{id}]

##### Unregister infrastructure [DELETE]

+ Parameters

    + id (string) - Id of the infrastructure

+ Request

    + Headers
    
            user: basic authentication user
            password: basic authentication password

+ Response 204
+ Response 404

        Returned when the given uuid doesn't exist in the database.

+ Response 409

        Returned when the infrastructure is still being used.

### Group Flavors

#### Flavors Collection [/v1/flavors{?promoted}{?public}]

##### List all flavors [GET]

This operations allows to get all the registered flavors.


+ Parameters

    + promoted (optional, boolean) - If true retrieves only the promoted flavors.
    + public (optional, boolean) - Retrieve only the public or private flavors.

+ Request

    + Headers
    
            user: basic authentication user
            password: basic authentication password

+ Response 200 (application/xml)

    + Body
            
            <?xml version="1.0" encoding="UTF-8"?>
            <flavors>
                <flavor id="82375e8c-9b4c-4e7c-9495-c0205c8622d2">
                    <name>tiny</name>
                    <vcpus>1</vcpus>
                    <ram>512</ram>
                    <disk>1</disk>
                    <swap>0</swap>
                    <promoted>true</promoted>
                    <public>true</public>
                    <node>SaoPaulo</node>
                    <node>Karlskrona2</node>
                    <node>Lannion</node>
                    <node>SophiaAntipolis</node>
                    <node>Mexico</node>
                    <node>Waterford</node>
                    <node>Poznan</node>
                    <node>PiraeusU</node>
                    <node>Crete</node>
                    <node>PiraeusN</node>
                    <node>Stockholm2</node>
                    <node>Zurich</node>
                    <node>Budapest2</node>
                    <node>Berlin2</node>
                    <node>Prague</node>
                    <node>Volos</node>
                    <node>Gent</node>
                    <node>Trento</node>
                    <node>Spain2</node>
                </flavor>
                <flavor id="e3b0f0a4-ea03-428b-97c6-8a06fd62b014">
                    <name>medium</name>
                    <vcpus>2</vcpus>
                    <ram>1024</ram>
                    <disk>1</disk>
                    <swap>0</swap>
                    <promoted>false</promoted>
                    <public>true</public>
                    <node>Waterford</node>
                    <node>Poznan</node>
                    <node>Crete</node>
                    <node>Stockholm2</node>
                    <node>Budapest2</node>
                    <node>Berlin2</node>
                    <node>Volos</node>
                </flavor>
                <flavor id="d1fb4620-f711-4393-b9f3-f2d476464daf">
                    <name>hpc</name>
                    <vcpus>16</vcpus>
                    <ram>16384</ram>
                    <disk>100</disk>
                    <swap>0</swap>
                    <promoted>false</promoted>
                    <public>true</public>
                    <node>SaoPaulo</node>
                    <node>Spain2</node>
                </flavor>
                <flavor id="857dc211-e1f4-4cbe-b498-6847c14acb26">
                    <name>my_flavor</name>
                    <vcpus>2</vcpus>
                    <ram>512</ram>
                    <disk>3</disk>
                    <swap>0</swap>
                    <promoted>false</promoted>
                    <public>false</public>
                    <node>Mordor</node>
                </flavor>
            </flavors>
        
        
+ Response 200 (application/json)

    + Body
            
            {
                "flavors":[
                    {
                        "id":"82375e8c-9b4c-4e7c-9495-c0205c8622d2",
                        "name":"tiny",
                        "vcpus":1,
                        "ram":512,
                        "disk":1,
                        "swap":0,
                        "promoted":true,
                        "public":true,
                        "nodes":[
                            "SaoPaulo",
                            "Karlskrona2",
                            "Lannion",
                            "SophiaAntipolis",
                            "Mexico",
                            "Waterford",
                            "Poznan",
                            "PiraeusU",
                            "Crete",
                            "PiraeusN",
                            "Stockholm2",
                            "Zurich",
                            "Budapest2",
                            "Berlin2",
                            "Prague",
                            "Volos",
                            "Gent",
                            "Trento",
                            "Spain2"
                        ]
                    },
                    {
                        "id":"e3b0f0a4-ea03-428b-97c6-8a06fd62b014",
                        "name":"medium",
                        "vcpus":2,
                        "ram":1024,
                        "disk":1,
                        "swap":0,
                        "promoted":false,
                        "public":true,
                        "nodes":[
                            "Waterford",
                            "Poznan",
                            "Crete",
                            "Stockholm2",
                            "Budapest2",
                            "Berlin2",
                            "Volos"
                        ]
                    },
                    {
                        "id":"d1fb4620-f711-4393-b9f3-f2d476464daf",
                        "name":"hpc",
                        "vcpus":16,
                        "ram":16384,
                        "disk":100,
                        "swap":0,
                        "promoted":false,
                        "public":true,
                        "nodes":[
                            "SaoPaulo",
                            "Spain2"
                        ]
                    },
                    {
                        "id":"857dc211-e1f4-4cbe-b498-6847c14acb26",
                        "name":"my_flavor",
                        "vcpus":2,
                        "ram":512,
                        "disk":3,
                        "swap":0,
                        "promoted":false,
                        "public":false,
                        "nodes":[
                            "Mordor"
                        ]
                    }
                ]
            }

+ Response 502

        Returned when the OpenStack infrastructure is not reachable.

##### Create a new flavor [POST]

Allows to create a new flavor. It takes an XML or JSON body the description
of the flavor characteristics:

+ name (string) - The name of the new flavor
+ vcpus (int) - The number of CPUs for the VMs based on this flavor
+ ram (int) - The amount of RAM in megabytes for the VMs based on this flavor
+ disk (int) - The amount of disk space in gigabytes for the VMs based on this flavor
+ swap (int) - The amount of swap space in megabytes for the VMs based on this flavor
+ public (boolean, optional) - Make the flavor public in the flavor sync tool.

+ Request (application/xml)

    + headers
    
            user: basic authentication user
            password: basic authentication password

    + body
    
            <?xml version="1.0" encoding="UTF-8"?>
            <flavor>
                <name>insane</name>
                <vcpus>640</vcpus>
                <ram>1232896</ram>
                <disk>1262485504</disk>
                <swap>0</swap>
            </flavor>


+ Response 201 (application/xml)

    + Body

            <?xml version="1.0" encoding="UTF-8"?>
            <flavor id="567b200e-0aca-49e0-8e9a-8c1f6ad3abe2">
                <name>insane</name>
                <vcpus>640</vcpus>
                <ram>1232896</ram>
                <disk>1262485504</disk>
                <swap>0</swap>
                <promoted>false</promoted>
                <public>false</public>
                <node>Mordor</node>
            </flavor>

+ Request (application/json)

    + headers
    
            user: basic authentication user
            password: basic authentication password

    + body
            
            {
                "flavor": {
                    "name":"insane",
                    "vcpus":640,
                    "ram":1232896,
                    "disk":1262485504,
                    "swap":0
                }
            }

+ Response 201 (application/json)

    + Body

            {
                "flavor": {
                    "id":"567b200e-0aca-49e0-8e9a-8c1f6ad3abe2",
                    "name":"insane",
                    "vcpus":640,
                    "ram":1232896,
                    "disk":1262485504,
                    "swap":0,
                    "promoted":false,
                    "public":false,
                    "nodes":[
                        "Mordor"
                    ]
                }
            }

+ Response 400

        Returned when incorrect data has been suplied.

+ Response 409

        Returned when the name already exists in the database.
        
+ Response 502

        Returned when the OpenStack infrastructure is not reachable.

#### Flavor [/v1/flavors/{id}]

##### Get flavor info [GET]

+ Parameters

    + id (string) - Id of the flavor

+ Request

    + Headers
    
            user: basic authentication user
            password: basic authentication password

+ Response 200 (application/xml)

    + Body

            <?xml version="1.0" encoding="UTF-8"?>
            <flavor id="567b200e-0aca-49e0-8e9a-8c1f6ad3abe2">
                <name>insane</name>
                <vcpus>640</vcpus>
                <ram>1232896</ram>
                <disk>1262485504</disk>
                <swap>0</swap>
                <promoted>false</promoted>
                <public>false</public>
                <node>Mordor</node>
            </flavor>

+ Response 200 (application/json)

    + Body

            {
                "flavor": {
                    "id":"567b200e-0aca-49e0-8e9a-8c1f6ad3abe2",
                    "name":"insane",
                    "vcpus":640,
                    "ram":1232896,
                    "disk":1262485504,
                    "swap":0,
                    "promoted":false,
                    "public":false,
                    "nodes":[
                        "Mordor"
                    ]
                }
            }

+ Response 404

        Returned when the object is not in the database.

+ Response 502

        Returned when the OpenStack infrastructure is not reachable.

##### Modify an existing flavor [PUT]

Updates the flavor identified by the id. The allowed changes refers to its 
public and promoted parameters. Any infrastructure owner will be able to publish
his images, but superadmin privileges will be needed for promoting them. Once
the flavor has been published, it cannot be unpublished.

It also allows to install a public flavor in a new infrastructure.

+ promoted (optional boolean) - Promote the flavor in the flavor sync tool.
+ public (optional, boolean) - Make the flavor public in the flavor sync tool.
+ nodes (optional, array[string]) - Single list with the nodes to install the flavor in

+ Parameters

    + id (string) - Id of the flavor

+ Request (application/xml)

    + headers
    
            user: basic authentication user
            password: basic authentication password

    + body
            
            <?xml version="1.0" encoding="UTF-8"?>
            <flavor>
                <node>Mordor</node>
            </flavor>

+ Response 200 (application/xml)

    + Body

            <?xml version="1.0" encoding="UTF-8"?>
            <flavor id="d1fb4620-f711-4393-b9f3-f2d476464daf">
                <name>hpc</name>
                <vcpus>16</vcpus>
                <ram>16384</ram>
                <disk>100</disk>
                <swap>0</swap>
                <promoted>false</promoted>
                <public>true</public>
                <node>SaoPaulo</node>
                <node>Spain2</node>
                <node>Mordor</node>
            </flavor>

+ Request (application/json)

    + headers
    
            user: basic authentication user
            password: basic authentication password

    + body
            
            {
                "flavor": {
                    "nodes":["Mordor"]
                }
            }

+ Response 200 (application/json)

    + Body

            {
                "flavor": {
                    "id":"d1fb4620-f711-4393-b9f3-f2d476464daf",
                    "name":"hpc",
                    "vcpus":16,
                    "ram":16384,
                    "disk":100,
                    "swap":0,
                    "promoted":false,
                    "public":true,
                    "nodes":[
                        "SaoPaulo",
                        "Spain2",
                        "Mordor"
                    ]
                }
            }

+ Response 400

        Returned when incorrect data has been suplied.

+ Response 401

        Returned when a user has not privileges to promote a flavor.

+ Response 404

        Returned when the object with the id is not in the database.

+ Response 409

        Returned when the node to publish on is not found in the database.
        Returned when trying to unpublish a flavor.
        
+ Response 502

        Returned when the OpenStack infrastructure is not reachable.

##### Delete flavor [DELETE]

+ Parameters

    + id (string) - Id of the flavor.

+ Response 204
+ Response 404

        Returned when the given id doesn't exist in the database.

+ Response 502

        Returned when the OpenStack infrastructure is not reachable.

##License##

Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)
