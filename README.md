# airbus-inventory
Airbus Inventory code challenge

The application is deployed on Heroku and `gunicorn` is used as WSGI server.

Heroku app URL : https://airbus-inventory.herokuapp.com/

The user needs to login first to use the application. If needed, user can register new account.

Please use the below dummy Email account for logging in for the first time 
Email : admin@example.com
Password: admin

The application screenshots are available in the screenshots folder .

Most of the REST API ( `/api/v1/login` for example) are secured with JWT Bearer Token. The APIs can be tested with PostMan. The JWT tokens can be obtained by calling the `/api/v1/login` REST API. For subsequent REST API calls, this JWT Token has to be pased.

## Screenshots

Please see `screenshots` folder for more.

![Product Listing Page](https://github.com/gauravssnl/airbus-inventory/blob/main/screenshots/Screenshot%20from%202021-12-13%2023-36-02.png)
## Steps
To run the application , follow the below steps as needed:
1. Set the Flask application name environment variable first, by running the below command:

```bash
export FLASK_APP=flask_app
```
2. Pick desired environemnt configuartion (defualt value is set to  `DevelopmentConfig` ) by setting the below environment variable :
```bash
FLASK_CONFIG=production #for production
```
Change the value accordingly. Use `testing` for `TestingConfig ` and `development`' for `DevelopmentConfig` .

3. Create Migration repository. If `migrations` folder for DB tables  is not present, we need to initailize flask-migrate scripts which uses Alembic. We can do by running the below command:
```bash
flask db init
``` 
4. Creating Migration scripts. To create an automatic migration script(s), run the blow command and pass your  commit message similar to git commit:
```bash
flask db migrate -m "initial migration"
```

5. To run the application in PROD mode, please run the below commands:

```bash
export FLASK_APP=flask_app 
export FLASK_CONFIG=production
export FLASK_DEBUG=0
flask run
```

6. To run the application in DEBUG + DEV mode, please run the below commands:

```bash
export FLASK_APP=flask_app 
export FLASK_CONFIG=development
export FLASK_DEBUG=1   
flask run
```
7. Once the application server is running (on port 5000 for example), we need to call the `/api/v1/login` first to get JWT Bearer Access Token. The JWT token has to be passed for all the protected API calls.

8. APIs realted to Users are avialble at `/api/v1/users`, APIs related to Product Categories are available at `/api/v1/categories` and APIs related to Products are available at `/api/v1/products` .

9. `GET` method is used for fetching the data and id can be passed in the URL path to fetch data with particular Id ( Example : `/api/v1/products/1` ) . If no ID is passed the URL, all records are fetched ( we can also add pagination based on requirements). `POST` is used for new resource creation , `PUT` is used for updating an existing resource and `DELETE`  is used for deletion of any resource. For more API details, please see `app.api` package code.
