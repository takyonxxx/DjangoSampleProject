import asyncio
import multiprocessing
import time
from math import pi

import pandas as pd
import requests
from sklearn.linear_model import LinearRegression


# MVC Tasarım Deseni (Model-View-Controller)
# ORM (Object-Relational Mapping)
# Admin Paneli:
# Form ve Validasyon
# Templating Engine
# URL Yönlendirme ve Gelişmiş Routing
# Güvenlik
# Çoklu Dil ve Zaman Dilimi Desteği
# RESTful API Desteği
# Modüler ve Genişletilebilir
# SEO Search Engine Optimization
# CRUD Create, Read, Update, and Delete
# Django ORM is a database abstraction API

def calculate_weather_data():
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = 'YOUR_API_KEY'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'

    # Function to get weather data for a specific date
    def get_weather_data(date):
        params = {
            'q': 'YOUR_CITY',  # Replace with your city name
            'appid': api_key,
            'dt': date.timestamp(),
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        return data['main']['temp']  # Extract temperature from the response

    # Create historical temperature data
    historical_data = pd.DataFrame({
        'Date': pd.date_range(start='2022-01-01', end='2022-12-31', freq='D'),
        'Temperature': [get_weather_data(date) for date in
                        pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')],
    })

    # Convert dates to ordinal numbers
    historical_data['Date_Ordinal'] = historical_data['Date'].apply(lambda x: x.toordinal())

    # Dates for the days you want to predict in the future
    future_dates = pd.date_range(start='2023-06-01', end='2023-06-10', freq='D')

    # Convert future dates to ordinal numbers
    future_dates_ordinal = future_dates.to_series().apply(lambda x: x.toordinal())

    # Create a Linear Regression model
    X_train = historical_data[['Date_Ordinal']]
    y_train = historical_data['Temperature']
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions for the upcoming year
    X_future = pd.DataFrame({'Date_Ordinal': future_dates_ordinal})
    future_predictions = model.predict(X_future)

    # Add predictions to a DataFrame
    future_data = pd.DataFrame({'Date': future_dates, 'Temperature Prediction': future_predictions})

    # Print the results
    print(future_data)


# tersten okunması aynı
def is_palindrome(s):
    # Base case: If the string is empty or has only one character, it's a palindrome
    if len(s) <= 1:
        return True
    s1 = s
    s2 = s[::-1]
    if s1 == s2:
        return True
    else:
        return False


def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        # Her geçitte en büyük elemanı sona getir
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def Star_triangle(n):
    for x in range(n):
        print(' ' * (n - x - 1) + '*' * (2 * x + 1))


def fibonacci(n):
    fib_series = [0, 1]

    while len(fib_series) < n:
        fib_series.append(fib_series[-1] + fib_series[-2])

    return fib_series


# asal mı
def is_prime(number):
    if number <= 1:
        return False
    elif number == 2:
        return True
    elif number % 2 == 0:
        return False
    else:
        # Kontrol edilecek olan sayıya kadar olan tüm tek sayıları kontrol et
        for i in range(3, int(number ** 0.5) + 1, 2):
            if number % i == 0:
                return False
        return True


# Self is an object or an instance of a class.
class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        pass

    def fact(self):
        return "I am a two-dimensional shape."

    def __str__(self):
        return self.name


class Square(Shape):
    def __init__(self, length):
        super().__init__("Square")
        self.length = length

    def area(self):
        return self.length ** 2

    def fact(self):
        return "Squares have each angle equal to 90 degrees."


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2


class Process(multiprocessing.Process):
    def __init__(self, id):
        super(Process, self).__init__()
        self.id = id

    def run(self):
        time.sleep(1)
        print("I'm the process with id: {}".format(self.id))


def thread_function(name):
    print(f"Thread {name}: starting")
    time.sleep(2)
    print(f"Thread {name}: finishing")


async def async_test1():
    print("Async async_test1 working...")
    await asyncio.sleep(1)


async def async_test2():
    print("Async async_test2 working...")
    await asyncio.sleep(1)


async def test_async():
    await asyncio.gather(async_test1(), async_test2())


def test_generator(n):
    # initialize counter
    val = 0
    # loop until counter is less than n
    while val < n:
        # produce the current value of the counter
        yield val
        # increment the counter
        val += 1


def mul(*args):
    print(args[0] * args[1])
    for name in args:
        print(f"Hello, {name}")


def pretty_print(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
