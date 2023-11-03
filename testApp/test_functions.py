import asyncio
import multiprocessing
import time
from functools import wraps
from math import pi

import numpy as np
import pandas as pd
import requests
from django.http import HttpResponseNotAllowed
from sklearn.linear_model import LinearRegression
from multiprocessing import Pool

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


"""Python Global Interpreter Lock (GIL), Python dilinin referans uygulaması olan CPython'da bulunan bir kilittir. 
GIL, aynı anda birden fazla yerel iş parçacığının Python bytecod'larını çalıştırmasını önleyen bir kilittir. Bu 
kilitleme, CPython'un bellek yönetimi konusunda iş parçacıkları arasında güvenli olmadığı için gereklidir. CPython, 
Python programlama dilinin referans uygulamasıdır. Python dilinin tasarımını ve standart kütüphanesini belirleyen ve 
geliştiren uygulamadır. "C" harfi, CPython'ın Python yorumlayıcısının büyük ölçüde C programlama diliyle yazıldığı 
anlamına gelir."""

"""CPython'ın Garbage Collector'ı, bellekte kullanılmayan nesneleri otomatik olarak tanımlayıp temizleyen bir 
mekanizmadır. Döngüsel referanslar bazen temizlenmez ve bellekte kalabilir. 3.7 den sonra iyileştirme yapıldı."""


def custom_http_methods(request_method_list):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method not in request_method_list:
                response = HttpResponseNotAllowed(request_method_list)
                # You can customize the logging or any other behavior here
                print(f"Method Not Allowed ({request.method}): {request.path}")
                return response
            return func(request, *args, **kwargs)

        return inner

    return decorator


def my_decorator(prefix):
    def wrapper(func):
        def inner_wrapper():
            print(f"{prefix}: Something is happening before the function is called.")
            func()
            print(f"{prefix}: Something is happening after the function is called.")

        return inner_wrapper

    return wrapper


def test_multiprocessing():
    count = 50000000

    def countdown(n):
        while n > 0:
            n -= 1

    pool = Pool(processes=2)
    start = time.time()
    r1 = pool.apply_async(countdown, [count // 2])
    r2 = pool.apply_async(countdown, [count // 2])
    pool.close()
    pool.join()
    end = time.time()
    print('Time taken for test_multiprocessing, in seconds - {:.2f}'.format(end - start))


def test_garbage_collector():
    import gc
    import resource
    import time

    class Person:
        def __init__(self, name):
            self.name = name
            self.friend = None

    # Create instances of Person with circular references
    # Döngüsel referans oluştur
    person1 = Person("Alice")
    person2 = Person("Bob")
    person1.friend = person2
    person2.friend = person1

    # Get the current memory usage
    before_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Run the Garbage Collector
    gc.collect()
    # Give the Garbage Collector some time to work
    time.sleep(1)
    # Get the memory usage after garbage collection
    after_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # Check if there is any change in memory usage
    if before_memory == after_memory:
        print("No memory freed by the Garbage Collector.")
    else:
        print("Memory freed by the Garbage Collector.")


def test_numpy():
    # numpy allow vector and matrix operations
    a = np.arange(15).reshape(3, 5)
    b = np.array([[1, 2], [3, 4]], dtype=complex)
    # load data into a DataFrame object:
    data = {
        "calories": [420, 380, 390],
        "duration": [50, 40, 45]
    }
    data_frame1 = pd.DataFrame(data)
    data = {
        "calories": [None, None, 39430],
        "duration": [530, None, 32]
    }
    data_frame2 = pd.DataFrame(data)
    merged_dataframe = pd.concat([data_frame1, data_frame2], ignore_index=True)
    # print(merged_dataframe.loc[1])  # second line information
    missing_count = merged_dataframe.isnull().sum()
    merged_dataframe['calories'] = merged_dataframe['calories'].fillna(0)
    merged_dataframe['duration'] = merged_dataframe['duration'].fillna(0)


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
    #
    # # Create sample data LinearRegression
    # X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)  # Independent variable
    # y = np.array([2, 4, 5, 4, 5])  # Dependent variable
    #
    # # Create a LinearRegression model
    # model = LinearRegression()
    # model.fit(X, y)
    #
    # # Make predictions using the model
    # new_data_point = np.array([6]).reshape(-1, 1)
    # predicted_value = model.predict(new_data_point)
    #
    # # Print the predicted value, tahmin edilen
    # print("Predicted value:", predicted_value)
    #
    # # Create sample data Logistic Regression
    # X = np.array([50, 55, 60, 65, 70, 75, 80, 85, 90, 95]).reshape(-1, 1)  # Exam scores
    # y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])  # Pass status (0: Fail, 1: Pass)
    #
    # # Create a Logistic Regression model
    # model = LogisticRegression()
    # model.fit(X, y)
    #
    # # Make predictions using the model
    # new_data_point = np.array([72]).reshape(-1, 1)
    # predicted_prob = model.predict_proba(new_data_point)
    #
    # # Print the predicted probability of passing
    # print("Predicted probability of passing:", predicted_prob[0][1])
    #
    # # Create a NumPy array returns the indices that would sort the array
    # arr = np.array([10, 5, 8, 20, 3, 15, 7])
    # # Specify the number of maximum values you want (N)
    # N = 3
    # # Get indices of N maximum values
    # indices_of_max_values = np.argsort(arr)[-N:]
    # indices_of_min_values = np.argsort(arr)[:N]
    # # Print the result
    # print(
    #     "Indices of the {} maximum/minimum values: {} / {}".format(N, indices_of_max_values, indices_of_min_values))
    # a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # p = np.percentile(a, 25)  # Returns the 50th percentile which is also the median
    # print(p)


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


def star_triangle(n):
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


class Process(multiprocessing.Process):
    def __init__(self, id):
        super(Process, self).__init__()
        self.id = id

    def run(self):
        time.sleep(1)
        print("I'm the process with id: {}".format(self.id))


# x = threading.Thread(target=thread_function, args=(1,))
# x.start()
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


# s = time.perf_counter()
# asyncio.run(test_async())
# elapsed = time.perf_counter() - s
# print(f"Async executed in {elapsed:0.2f} seconds.")
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


def test_args(*args):
    print(args[0] * args[1])
    for name in args:
        print(f"Hello, {name}")


def test_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
