# Django application: "ShortCutURL"

Service for shortening long URLs. Short version of ***{domain}/AbCdE***

Each short link is *unique*. Counting of redirects for each short link has been implemented.

The project was implemented using Django:

* Django
* Django-Bootstrap
* Django-rest-framework

|   Directory   | Description                                                                                                                                                                                              |
|:-------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   mainapp/api/  | API for the service, implemented using APIView. GET, POST, PUT, PATCH, DELETE methods for Urls model. Basic and Token Authentication                                                                                                                               |
|   mainapp/tests/  | Tests for API, Forms, Model and Views                                                                                                               |
|   shortcut/   | Configuration package                                                                                                                 |

```
mainapp/             Application directory with modules
shortcut/            Configuration package
README               this file
Dockerfile           Text document that contains all the commands to assemble an image
docker-compose.yaml  Config files interpreted by the Docker engine
requirements         “Requirements files” are files containing a 
                     list of items to be installed using "pip install -r requirements.txt"
```

##### Home page

![home page](https://i.ibb.co/v4HbQLP/home-shortutl.png)

##### Short url

![short url](https://i.ibb.co/fxNBzRX/short-shorturl.png)

##### Check clicks for shortl url

![check clicks](https://i.ibb.co/QkJL1Dt/clicks-shorturl.png)

##### Example API (GET all urls)

![api](https://i.ibb.co/t3LFXVX/api-shorturl.png)

### Contacts for communication

* 8-916-191-51-85
* malykuanov@mail.ru
* @white_bunny_hop (TG)