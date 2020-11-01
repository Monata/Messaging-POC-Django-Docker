**Raiment Django Server**

The project is structured like this:
```
ribbon
├── raiment
|   ├── models.py (to define our database models)
|   ├── serializers.py (to convert our models to JSON format)
|   ├── urls.py (to define URLs for our API)
|   ├── views.py (to add a api logic to our API)
|   └── tests.py (to write tests for our API)
├── ribbon
|   └── Django setting files (urls.py, settings.py)
├── script.sh (you only have to run this script to deploy the server)
└── requirements.txt
```

*Api definition:*
    
    URL: hello/ 
    TYPE: GET
    PARAMETERS: NONE
    RETURNS: JSON OBJECT
    {
    "message": 39
    }
    DESCRIPTION:must be called with a JWT, returns the user id
.    

    URL: signup/ 
    TYPE: POST
    PARAMETERS: JSON OBJECT 
    e.g.
    {
    "user": {
        "username": "Admin",
        "password": "rootpass"
        }
    }
    RETURNS: 
        ON SUCCESS:
            {"user": {
                "user": {
                    "id": USERID,
                    "username": USERNAME,
                    "email": ""
                }
                }
            }
         ON FAIL:
            "user": {
                "username": [
                    "A user with that username already exists." e.g.
                ]
            }
    DESCRIPTION:returns the serialized user object
.

    URL: login/ 
    TYPE: POST
    PARAMETERS: username,password
    RETURNS: JWT
    DESCRIPTION: JWT is needed for accessing messsaging system
.

    URL: message/ 
    TYPE: GET
    PARAMETERS: receiver
    RETURNS: JSON object
    {
    "users": [
        USER1,
        USER2
    ],
    "messages": [
        {
            "author": "Victoria Legrand", 
            "message": "A strange pair of dice", e.g.
            "date": "2020-10-29 23:25:13.545748+00:00"
        }, 
        {
            "author": AUTHOR,
            "message": CONTENT,
            "date": DATETIME
        },
        OTHER MESSAGES
    ]
    }
    DESCRIPTION:must be called with a JWT, returns the messaging history
.

    URL: message/ 
    TYPE: POST
    PARAMETERS: receiver,txt
    ON SUCCESS:
        JSON OBJECT
        {
        "from": AUTHOR,
        "to": RECEIVER,
        "txt": CONTENT
        }
    ON FAILURE:
        JSON OBJECT
        {
            "error_message": ERROR MESSAGE
        }
    DESCRIPTION: Sends a message, returns info about the message sent
. 
    
    URL: block/ 
    TYPE: GET
    PARAMETERS: NONE
    RETURNS:
        {
    "blocker": USERNAME,
    "blocked_users": [
        "Victoria Legrand", e.g.
        USERNAME,
        USERNAME
    ]
    }    
    DESCRIPTION: Returns the list of users blocked by the user logged in,JWT is needed for accessing blocking system
.
    
    URL: block/ 
    TYPE: POST
    PARAMETERS: receiver
    RETURNS:
        ON SUCCESS:
            JSON OBJECT
            {
                "blocker": USERNAME,
                "blocked": USERNAME
            }
        ON FAILURE:
            JSON OBJECT
            {
                "error_message": ERROR MESSAGE
            }
    DESCRIPTION: Blocks a user from sending a message to the logged in user, JWT is needed for accessing blocking system

warning.log records a human readable log, debug.log records system information