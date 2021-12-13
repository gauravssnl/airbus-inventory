# airbus-inventory
Airbus Inventory code challenge

The application is deployed on Heroku and `gunicorn` is used as WSGI server.

Heroku app URL : https://airbus-inventory.herokuapp.com/
## Steps
To run the application , follow the below steps as needed:
1. Set the Flask application nave environment variable first, by running the below command:

```bash
export FLASK_APP=flask_app
```

2. Create Migration repository. If `migrations` folder for DB tables  is not present, we need to initailize flask-migrate scripts which uses Alembic. We can do by running the below command:
```bash
flask db init
``` 
3. Creating Migration scripts. To create an automatic migration script(s), run the blow command and pass your  commit message similar to git commit:
```bash
flask db migrate -m "initial migration"
```

4. To run the application in PROD mode, please run the below commands:

```bash
export FLASK_APP=flask_app 
export FLASK_DEBUG=0
flask run
```

5. To run the application in DEBUG/DEV mode, please run the below commands:

```bash
export FLASK_APP=flask_app 
export FLASK_DEBUG=1   
flask run
```
6. Once the application server is running (on port 5000 for example), we need to call the `/api/v1/login` first to get JWT Bearer Access Token. The JWT token has to be passed for all the protected API calls.

7. APIs realted to Users are avialble at `/api/v1/users`, APIs related to Product Categories are available at `/api/v1/categories` and APIs related to Products are available at `/api/v1/products` .

8. `GET` method is used for fetching the data and id can be passed in the URL path to fetch data with particular Id ( Example : `/api/v1/products/1` ) . If no ID is passed the URL, all records are fetched ( we can also add pagination based on requirements). `POST` is used for new resource creation , `PUT` is used for updating an existing resource and `DELETE`  is used for deletion of any resource. For more API details, please see `app.api` package code.