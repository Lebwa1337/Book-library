# Library DRF Project

This project aims to create a web application using Django REST Framework (DRF) for managing library operations. It provides users with the ability to reserve and pay for books online.

---

## Features

- **User Authentication**: 
  The project includes user authentication via JWT token functionality to allow users to create accounts, log in, and manage their profiles.

- **Book Reservation**: 
  Users can browse the library's collection, select books they wish to borrow, and reserve them for a specific period.

- **Payment Integration**: 
  Integration with payment gateways enables users to pay for reserved books securely online.

- **Book Management**: 
  Librarians or administrators have the ability to add, update, and delete books from the library's collection.

- **User Profiles**: 
  Users can view their borrowing history, manage their reservations, and update their profile information.

- **Telegram message sender**:
  You will receive messages when you borrow a book, return a book, have borrowing overdue

- **Asynchronize schedule tasks**:
  Every day you will receive telegram message of your upcoming books that you should return. <\n>
  If you don't have upcoming books to return you will receive "No borrowings overdue today"

-------------------------------------------------------------------------------------

## Installation using GitHub
 
For beginning you have to install Python3+
 
**In terminal write down following command:**

```shell

git clone https://github.com/Lebwa1337/Book-library
python -m venv venv

* MacOS *
source venv/bin/activate
* Windows *
venv/scripts/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
 
```
## Run with docker
 
Docker should be installed
```shell
docker-compose up --build
```

-------------------------------------------------------------------------------------

## API Reference

#### Before start using this API Project, u should use register(if not yet) or use JWT Token for authentication if u already register.

#### For register:

```http
  POST api/user/
```

| Key | Type     | Description                |
| :-------- | :------- | :------------------------- |
| Email | Email | **Required**. Your Email |
| Password | Password | **Required**. Your Password |

#### For authentication (you should use your credentials for authentication)

```http
  GET api/user/token/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| Email    | Email | **Required**. Your Email |
| Password    | Password | **Required**. Your Password |

### You can see information about your account inc. email, are you staff etc. (update account info as well)


```http
  GET api/user/me/
```

------------------------------------------------------------------------------------

## RESOURCES

Note: You can get further resources if you are authenticated (**ex. Book List page**)
 
#### Get list of Books and create new one (if you have admin permissions)

```http
   GET /api/books/
```

#### Create a new book (You need admin permissions) 

```http
   POST /api/books/ 
```

#### Get detail info about book

```http
   GET, PATCH, PUT, DELETE /api/books/<int:pk>/
```
---------------------------------------------------------------------------------------
#### Get list of your borrowings (You can see all ones if you have admin permissions)

```http
   GET /api/borrowings/
```

#### Create a new borrow (only for authenticated user)

```http
   POST /api/borrowings/
```

#### Get detail info about your borrow (only for authenticated user)

```http
   GET /api/borrowings/<int:pk>/
```

#### Return your borrow 

```http
   POST /api/borrowings-return/
```
| Parameter    | Type     | Description                     |
|:-------------|:---------|:--------------------------------|
| borrowing_id | integer | **Required**. Your borrowing id |
---------------------------------------------------------------------------------------

#### Get list of Payments (You can see all ones if you have admin permissions)

```http
   GET /api/payments/
```

---------------------------------------------------------------------------------------

#### Get SWAGGER schema about this API

```http
   GET /api/doc/swagger/
```

#### Download SWAGGER schema

```http
   GET /api/schema/
```

----------------------------------------------------------------------------------
## Admin Panel

#### You can join admin panel through this endpoint:

```http
GET /admin
```
*Example*: http://127.0.0.1:8000/admin/

#### How to create superuser

If you run project locally you can use this command:
```shell
python manage.py createsuperuser
```
If you run project in docker so to create superuser follow these steps:
- check container app id:
```shell
docker ps
```
- enter container shell:
```shell 
docker exec -it <container_id> sh
```
- Create super user as usual:
```shell
python manage.py createsuperuser
```
----------------------------------------------------------------------------------
## Schedule tasks

#### You can start worker for asynchronize schedule task only if you run project in docker

#### How to run schedule task

After you up your project in docker follow these steps:
- Go to admin panel, choose Periodic tasks and create new periodic task
 where you should specify task and interval when this task will be triggered
- check container app id:
```shell
docker ps
```
- enter container shell:
```shell 
docker exec -it <container_id> sh
```
- Run worker:
```shell
celery -A book_library beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
----------------------------------------------------------------------------------
