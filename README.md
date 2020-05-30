In this article we’ll build a simple Django app that displays the current weather for various cities. To get the current weather data, we’ll use the Open Weather Map API.

We’ll work with a database and create a form, so the concepts used here are applicable to more complicated projects.

The code in this article was written with Python 3 and Django 2.0, so to follow this tutorial, you should be somewhat familiar with both.

Here’s what our app is going to look like when we’re done.

Weather App Home Page, with London, Tokyo, Las Vegas, and Miami weather

All the code for this article is on GitHub.

Installation
Installing Django is like installing any other Python library: you can start a virtual environment and run pip to install Django, or you can do what I do and create a project directory, run pipenv, and then activate the pipenv shell. Either method works, but for this article I’ll be using pipenv.

pipenv install django
This will install the latest version of Django for you. At the time of writing this article, Django is on version 2.0.4.

Once you have Django installed, create and navigate to a directory for this project if you haven’t already. Once there, you can run the startproject command that Django gives you to generate the project.

django-admin startproject the_weather
Django should have created a few new files in your directory.

Let’s try starting up our development server. To do that, navigate to the new directory and use manage.py to run the runserver command in your terminal:

cd the_weather
python manage.py runserver
If you look at your terminal, you should see the URL for your app. By default it should be 127.0.0.1:8000.

development server up and running

Open up your browser and go to that URL.

Django development server Congrats page in browser

If you see that, you know you’ve set up Django correctly. You definitely should see it because we haven’t even tried modifying the code yet.

The Admin Dashboard
Next we want to take a look at the admin dashboard Django gives us. To do that, first we have to migrate our database, which means Django will create the pre-defined tables that are needed for the default apps. To do this, run the migrate command. Stop the server by using CTRL+C and then run:

python manage.py migrate
By running that command, Django has created a SQLite database for you, the default database in the settings, and it has added several tables to that database. You’ll know if the database was created if you see a new db.sqlite3 file in your project directory.

One of the tables Django gives us is a user table, which will be used to store any users in our app. The app we’re building doesn’t need any users, but having an admin user will allow us to access the admin dashboard.

To create an admin user, we’ll run the createsuperuser command.

python manage.py createsuperuser
Follow the instructions by giving a username, email address, and a password for your admin user. Once you’ve done that, you’ll need to start the server again and navigate to the admin dashboard.

python manage.py runserver
Then go to 127.0.0.1:8000/admin.

The reason why we can go to this page is because because admin is set up in our urls.py (the reason why we can see the congratulations page is because Django gives you that until you add your own URLs).

If you log in with the username and password you just created, you should see the Django Admin Dashboard.

Admin Dashboard

Groups and users represent two models Django gives us access to. Models are just code representations of tables in a database. Even though Django created more tables, there’s no need to access the rest of them directly, so no models were created.

If you click on 'user' you should see more detail about the user table, and you should see the user you created. It’s a good idea to explore by clicking different links in the dashboard to see what’s there. Just be careful not to delete your user, otherwise you’ll have to run createsuperuser again.

Let’s leave the admin dashboard for now and go to the code. We need to create an app inside of our project for our weather app.

Creating the App
In Django, you can separate functionality in your project by using apps. I think app is a confusing name because we usually refer to an app as being the entire project, but in the case of Django, app refers to a specific piece of functionality in your project. For example, if you look at the settings.py file, you’ll see the INSTALLED_APPS list.

The first of the installed apps, django.contrib.admin is what we just used. It handles all the admin functionality and nothing else. Another app in our project by default are things like auth, which allowed us to log into our admin dashboard.

In our case, we need to create a new app to handle everything related to showing the weather. To create that app, stop the server with CTRL+C and run:

python manage.py startapp weather
By running startapp, Django has added a new directory and more files to our project.

With the latest files generated, let’s create a new file called urls.py in our app directory.

urls.py
from django.urls import path

urlpatterns = [
]
This file is similar to the urls.py in our the_weather directory. The difference is that this urls.py file contains all the URLs that are relevant to the app itself.

We’re not specifying a URL yet, but we can set up the project to recognize our app and route any URLs specific to our app to the app urls.py file.

First, go to the INSTALLED_APPS list and add this app to the list.

the_weather/the_weather/settings.py
...

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'weather',
]

...
This lets Django know we want to use the weather app in our project. By doing this, Django will know where to look for migrations and the URLs.

Next, we need to modify the original urls.py to point to our app urls.py file. To do that, we add a line under the existing path for the admin dashboard. We also need to import include so we can point to our app urls.py file.

the_weather/the_weather/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
path('admin/', admin.site.urls),
path('', include('weather.urls')),
]
The empty string means that we won’t use an endpoint for the entry point to our app. Instead we’ll let the app handle any specific endpoints. We could have put something like path (‘weather/’, …), which would have meant we would have to type 127.0.0.1:8000/weather/ to get anything associated with our weather app. But since our project is simple, we won’t be doing that here.

Adding the Template and View
Now for the first interesting thing we’re going to do. We need to add the template to our project.

A template in Django is just an HTML file that allows for extra syntax that makes the template dynamic. We’ll be able to do things like add variables, if statements, and loops, among other things.

We have an HTML file, but this will be enough for us to start.

We’re going to create a template directory to put this file in.

cd weather
mkdir templates && cd templates
mkdir weather
We also created another directory with the same name as our app. We did this because Django combines all the template directories from the various apps we have. To prevent filenames being duplicated, we can use the name of our app to prevent the duplicates.

Inside of the weather directory, create a new file called index.html. This will be our main template. Here’s the HTML we’ll use for the template:

the_weather/weather/templates/weather/index.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>What's the weather like?</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.6.2/css/bulma.css" />
</head>
<body>
    <section class="hero is-primary">
        <div class="hero-body">
            <div class="container">
                <h1 class="title">
                    What's the weather like?
                </h1>
            </div>
        </div>
    </section>
    <section class="section">
        <div class="container">
            <div class="columns">
                <div class="column is-offset-4 is-4">
                    <form method="POST">
                        <div class="field has-addons">
                            <div class="control is-expanded">
                                <input class="input" type="text" placeholder="City Name">
                            </div>
                            <div class="control">
                                <button class="button is-info">
                                    Add City
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
    <section class="section">
        <div class="container">
            <div class="columns">
                <div class="column is-offset-4 is-4">
                    <div class="box">
                        <article class="media">
                            <div class="media-left">
                                <figure class="image is-50x50">
                                    <img src="http://openweathermap.org/img/w/10d.png" alt="Image">
                                </figure>
                            </div>
                            <div class="media-content">
                                <div class="content">
                                    <p>
                                        <span class="title">Las Vegas</span>
                                        <br>
                                        <span class="subtitle">29° F</span>
                                        <br> thunderstorm with heavy rain
                                    </p>
                                </div>
                            </div>
                        </article>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <footer class="footer">
    </footer>
</body>
</html>
Now that we have our template created, let’s create a view and URL combination so we can actually see this in our app.

Views in Django are either functions or classes. In our case since we’re creating a simple view, we’ll create a function. Add this function to your views.py:

the_weather/weather/views.py
from django.shortcuts import render

def index(request):
return render(request, 'weather/index.html') #returns the index.html template
We’re naming our view index because it will be at the index of our app, which is the root URL. To have the template render, we return request, which is necessary for the render function, and the name of the template file we want to render, in this case weather/index.html.

Let’s add the URL that will send the request to this view. In the urls.py for the app, update the urlpatterns list.

the_weather/weather/urls.py
from django.urls import path
from . import views

urlpatterns = [
path('', views.index), #the path for our index view
]
This allows us to reference the view we just created.

Django is going to match any URL without an endpoint and route it to the view function we created.

Go back to your project root, start the server, and go to 127.0.0.1:8000 again.

python manage.py runserver
Template returned

What we see now is just the result of the HTML you have in index.html file. You’ll see an input to add a city and the weather for Las Vegas. However, the form doesn’t work and the weather is just a placeholder, but don’t worry, because we’ll be creating those for this app.

Using the Weather API
What we want to do now is sign up for the Open Weather Map API. This will allow us to get real-time weather for any cities that we add in our app.

Go to the site, create an account and then go to the API keys on their dashboard. Enter a name and generate a new API key. This key will allow us to use the API to get the weather.

Open Weather Map Dashboard

The one endpoint we’ll use is below, so you can see the data that gets returned by modifying the following URL with your API key and navigating to the URL in your browser. It may take a few minutes for your API key to become active, so if it doesn’t work at first, try again in after a few minutes.

http://api.openweathermap.org/data/2.5/weather?q=las%20vegas&units=imperial&appid=YOUR_APP_KEY
With that, let’s add in a request to get the data into our app.

First, we’ll need to install requests so we can call the API from inside our app.

pipenv install requests
Let’s update our index view to send a request to the URL we have.

the_weather/weather/views.py
from django.shortcuts import render
import requests

def index(request):
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_APP_KEY'
city = 'Las Vegas'
city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    return render(request, 'weather/index.html') #returns the index.html template

With those three lines, we’re adding the URL that we will send a request to. We’ll make the part for the city a placeholder for when we allow users to add their own cities.

For now we’ll set the city to be Las Vegas, but later this will be set to the cities from the database.

Finally, we’ll send the request to the URL using the city and get the JSON representation of that city. If we print that to the console we can see the same data we saw when we put the URL in our address bar.

If you start your server again and reload the page, you’ll see the data get printed to your console.

API Data

Displaying the Data in the Template
Next, we need to pass the data to the template so it can be displayed to the user.

Let’s create a dictionary to hold all of the data we need. Of the data returned to us, we need temp, description, and icon.

the_weather/weather/views.py
def index(request):
...
weather = {
'city' : city,
'temperature' : city_weather['main']['temp'],
'description' : city_weather['weather'][0]['description'],
'icon' : city_weather['weather'][0]['icon']
}

    return render(request, 'weather/index.html') #returns the index.html template

Now that we have all the information we want, we can pass that to the template. To pass it to the template, we’ll create a variable called context. This will be a dictionary that allows us to use its values inside of the template.

the_weather/weather/views.py
def index(request):
...
context = {'weather' : weather}
return render(request, 'weather/index.html', context) #returns the index.html template
And then in render, we’ll add the context as the third argument.

With the weather data added inside of context, let’s go to the template to add the data.

Inside of the template, all we need to do is modify the HTML to use variables instead of the values I typed in. Variables will use {{ }} tags, and they will reference anything inside of your context dictionary.

Note that Django converts dictionary keys so you can only access them using dot notation. For example, weather.city will give us the city name. We don’t use weather['city'] like we would in Python.

Find the box div, and update it to this:

the_weather/weather/templates/weather/index.html

<div class="box">
    <article class="media">
        <div class="media-left">
            <figure class="image is-50x50">
                <img src="http://openweathermap.org/img/w/{{ weather.icon }}.png" alt="Image">
            </figure>
        </div>
        <div class="media-content">
            <div class="content">
                <p>
                    <span class="title">{{ weather.city }}</span>
                    <br>
                    <span class="subtitle">{{ weather.temperature }}° F</span>
                    <br> {{ weather.description }}
                </p>
            </div>
        </div>
    </article>
</div>
With all the variables replaced, we should now see the current weather for our city.

Weather for Las Vegas

Now we can see the weather for one city, but we had to hard code the city. What we want to do now is pull from the database and show the cities that are in our database.

To do that, we’ll create a table in our database to hold the cities that we want to know the weather for. We’ll create a model for this.

Go to the models.py file in your weather app, and add the following:

the_weather/weather/models.py
from django.db import models

class City(models.Model):
name = models.CharField(max_length=25)

    def _str_(self): #show the actual city name on the dashboard
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'

This will create a table in our database that will have a column called name, which is the name of the city. This city will be a charfield, which is just a string.

To get these changes in the database, we have to run makemigrations to generate the code to update the database and migrate to apply those changes. Let’s do that now:

python manage.py makemigrations
python manage.py migrate
We need to make it to where we can see this model on our admin dashboard. To do that, we need to register it in our admin.py file.

the_weather/weather/admin.py
from django.contrib import admin
from .models import City

admin.site.register(City)
You’ll see the city as an option on the admin dashboard.

Cities on Admin Dashboard

We can then go into the admin dashboard and add some cities. I’ll start with three: London, Tokyo, and Las Vegas.

Three cities weather

With the entries in the database, we need to query these entries in our view. Start by importing the City model and then querying that model for all objects.

the_weather/weather/views.py
from django.shortcuts import render
import requests
from .models import City
the_weather/weather/views.py
...
def index(request):
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_APP_KEY'
cities = City.objects.all() #return all the cities in the database
...
Since we have the list of cities, we want to loop over them and get the weather for each one and add it to a list that will eventually be passed to the template.

This will just be a variation of what we did in the first case. The other difference is we are looping and appending each dictionary to a list. We’ll remove the original city variable in favor of a city variable in the loop:

the_weather/weather/views.py
def index(request):
...
weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data}
    ...

Now let’s update the context to pass this list instead of a single dictionary.

the_weather/weather/views.py
...
context = {'weather_data' : weather_data}
...
Next, inside of the template, we need to loop over this list and generate the HTML for each city in the list. To do this, we can put a for loop around the HTML that generates a single box for the city.

the_weather/weather/index.html

<div class="column is-offset-4 is-4">
    {% for weather in weather_data %}
    <div class="box">
        <article class="media">
            <div class="media-left">
                <figure class="image is-50x50">
                    <img src="http://openweathermap.org/img/w/{{ weather.icon }}.png" alt="Image">
                </figure>
            </div>
            <div class="media-content">
                <div class="content">
                    <p>
                        <span class="title">{{ weather.city }}</span>
                        <br>
                        <span class="subtitle">{{ weather.temperature }}° F</span>
                        <br> {{ weather.description }}
                    </p>
                </div>
            </div>
        </article>
    </div>
    {% endfor %}
</div>
Now we can see the data for all the cities we have in the database.

Creating the Form
The last thing we want to do is allow the user to add a city directly in the form.

To do that, we need to create a form. We could create the form directly, but since our form will have exactly the same field as our model, we can use a ModelForm.

Create a new file called forms.py.

the_weather/weather/forms.py
from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
class Meta:
model = City
fields = ['name']
widgets = {
'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
} #updates the input class to have the correct Bulma class and placeholder
To view the form, we need to create it in our view and pass it to the template.

To do that, let’s update the index video to create the form. We’ll replace the old city variable at the same time since we no longer need it. We also need to update the context so the form gets passed to the template.

the_weather/weather/views.py
def index(request):
...
form = CityForm()

    weather_data = []
    ...
    context = {'weather_data' : weather_data, 'form' : form}

Now in the template, let’s update the form section to use the form from our view and a csrf_token, which is necessary for POST requests in Django.

<form method="POST">
    {% csrf_token %}
    <div class="field has-addons">
        <div class="control is-expanded">
            {{ form.name }}
        </div>
        <div class="control">
            <button class="button is-info">
                Add City
            </button>
        </div>
    </div>
</form>
With the form in our HTML working, we now need to handle the form data as it comes in. For that, we’ll create an if block checking for a POST request. We need to add the check for the type of request before we start grabbing the weather data so we immediately get the data for the city we add.

the_weather/weather/views.py
def index(request):
cities = City.objects.all() #return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_APP_KEY'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()
    ...

By passing request.POST, we’ll be able to validate the form data.

Now you should be able to type in the name of a city, click add, and see it show up. I’ll add Miami as the next city.

Form submitted with new city

When we drop out of the if block, the form will be recreated so we can add another city if we choose. The rest of the code will behave in the same way.
