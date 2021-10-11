# Shop

## About Project

The website displays products. Users can add and remove products to their basket while also specifying the quantity of each item. They can then enter their address and choose Stripe to handle the payment processing.

[![alt text](https://github.com/Mostafa-N-E/Shop-static/blob/main/static/img/view.jpg?raw=true "Logo")](https://github.com/Mostafa-N-E/Shop-static/blob/main/static/img/view.jpg)

---

## Running this project

Clone or download this repository and open it.

```
# clone the repository
$ git clone https://github.com/Mostafa-N-E/Shop
$ cd Shop
```

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately.

Create a virtualenv and activate it on Mac/Linux:

```
$ python3 -m venv venv
$ . venv/bin/activate
```

Or on Windows cmd:

```
$ py -3 -m venv venv
$ venv\Scripts\activate
```

That will create a new folder `venv` in your project directory. Next, install the project dependencies with:

```
pip install -r requirements.txt
```
### before run project 
Important Note: You must download the static file from this address 
[Shop-static](https://github.com/Mostafa-N-E/Shop-static/)
and put it in the main project file next to the file ‍‍‍`template`

and execute this command
```
python manage.py collectstatic   
```

Now you can run the project with this commands:

```
python manage.py makemigrations
python manage.py migrate  
python manage.py runserver
```