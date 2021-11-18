# Django application: "ShortCutURL" 

Service for shortening long URLs. Short version of ***{domain}/AbCdE***

Each short link is *unique*. 

<ins>**The project is designed to familiarize with the basic features of the Django Framework and has no other purpose**

For training purposes, the project was launched in Docker (postgresql + gunicorn + nginx) on the [url-cut.ru](https://url-cut.ru) domain

The project was implemented using Django: 

* Django
* Django-Bootstrap
* Django-rest-framework

|   Directory   | Description                                                                                                                                                                                              |
|:-------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   mainapp/api/  | API for the service, implemented using APIView. GET, POST, PUT, PATCH, DELETE methods for Urls model. Basic and Token Authentication |
|   mainapp/management/  | registering custom actions for manage.py |
|   mainapp/static/  | Application static files |
|   mainapp/templates/  | Application-level templates |
|   mainapp/tests/  | Tests for API, Forms, Model and Views |
|   shortcut/   | Configuration package |
|   docker/   | Docker settings folder for nginx and postgresql |

```
mainapp/             Application directory with modules
shortcut/            Configuration package
docker/              Folder for docker settings
README               this file
Dockerfile           Text document that contains all the commands to assemble an image
docker-compose.yaml  Config files interpreted by the Docker engine
requirements         “Requirements files” are files containing a 
                     list of items to be installed using "pip install -r requirements.txt"
```
###API example:

**With basic auth**

**GET**
```
curl -u mikle:password -X GET https://url-cut.ru/api/v1/urls/ | jq
```
```
[
  {
    "short_url": "R2w32",
    "clicks": 1,
    "time_create": "2021-11-16T20:20:21.275095Z",
    "time_last_click": "2021-11-16T20:20:38.136884Z",
    "owner": "mikle",
    "long_url": "http://example.com/testapi"
  }
]
```
**POST**
```
curl -u mikle:password -X POST -H "Content-Type: application/json" -d '{"long_url": "http://example.com/testpost"}' https://url-cut.ru/api/v1/urls/ | jq
```
```
{
  "long_url": "http://example.com/testpost",
  "short_url": "e2jJ2",
  "clicks": 0,
  "time_create": "2021-11-18T18:07:49.994896+03:00",
  "time_last_click": null,
  "owner": "mikle"
}
```
**djoser token auth**
```
curl -X POST https://url-cut.ru/api-auth/users/ --data 'username=djosername&password=strongpass'
```
>{"email":"","username":"djosername","id":8}
```
curl -X POST https://url-cut.ru/api-auth/token/login/ --data 'username=djosername&password=strongpass'
```
>{"auth_token":"8c01c6e2763244a2ca50361b217b37b0b766fc42"}
```
curl -X POST https://url-cut.ru/api/v1/urls/ -H 'Authorization: Token 8c01c6e2763244a2ca50361b217b37b0b766fc42' -H "Content-Type: application/json" -d '{"long_url": "http://example.com/testtoken"}' | jq
```
```
{
  "long_url": "http://example.com/testtoken",
  "short_url": "XYK5q",
  "clicks": 0,
  "time_create": "2021-11-18T19:36:22.387466+03:00",
  "time_last_click": null,
  "owner": "djosername"
}
```

The project has implemented a custom action for test generation of users and urls:

**python manage.py gen_users_and_url [key]** ,

where the key is:
* **-t [count]** to generate a given number of random users (default 1 test url per user)
* **-u [count]** to generate a given number of urls (anonymous user *[default_user]*)
* **-s** to display the user and the number of shortened links. Optional: total number of users and shortened links
* **-a** to generate a user with an administrator role
* **-t [count] -u [count]** to generate a given number of users with a specific number of urls

##### Home page

![home page](https://i.ibb.co/12V1ctq/shortcut-home.png)

##### Short url

![short url](https://i.ibb.co/Kq1Mh5k/shortcut-short.png)

##### Check clicks for shortl url

![check clicks](https://i.ibb.co/xjLSfQD/shortcut-clicks.png)

##### User`s Dashboard

![dashboard](https://i.ibb.co/QrnJmg8/shortcut-dashboard.png)

##### Example API (GET all urls)

![api](https://i.ibb.co/McqqSKS/shortcut-api.png)

### Contacts for communication

* 8-916-191-51-85
* malykuanov@mail.ru
* @white_bunny_hop (TG)