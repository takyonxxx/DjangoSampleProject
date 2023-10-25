import asyncio
import operator
import os
import random
import threading
import time

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
import json
from testApp.models import TestModel
from testApp.serializers import TestModelSerializer, TestSubModelSerializer
import array
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from functools import reduce

from testApp.test_functions import Square, Circle, thread_function, test_async, mul, pretty_print
from testApp.test_inheritance import test_inheritance, test_abstract_class


@require_http_methods(['POST', 'OPTIONS'])
@csrf_exempt
def test_api(request):
    if request.method == 'POST':
        demo_list = [5, 4, 4, 6, 8, 12, 12, 1, 5]

        # filename = "test_file.txt"
        # lines = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
        # s = "Hello\n"
        # with open(filename, "w") as file:
        #     file.write(s)
        #     file.writelines(lines)
        # with open(filename, "r") as file:
        #     count = 0
        #     text = file.read()
        #     for character in text:
        #         if character.isupper():
        #             count += 1
        #     for i, _ in enumerate(file):
        #         pass
        # os.remove(filename)

        # that prints out keyword arguments in a nice format
        # pretty_print(title="The Matrix", director="Wachowski", year=1999)

        # iterate over the generator object produced by my_generator
        # for value in test_generator(3):
        #     # print each value produced by generator

        # a = Square(4)
        # b = Circle(7)
        # print(a, a.area(), b, b.area())

        # x = threading.Thread(target=thread_function, args=(1,))
        # x.start()
        #
        # s = time.perf_counter()
        # asyncio.run(test_async())
        # elapsed = time.perf_counter() - s
        # print(f"Async executed in {elapsed:0.2f} seconds.")

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

        # Create sample data LinearRegression
        X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)  # Independent variable
        y = np.array([2, 4, 5, 4, 5])  # Dependent variable

        # Create a LinearRegression model
        model = LinearRegression()
        model.fit(X, y)

        # Make predictions using the model
        new_data_point = np.array([6]).reshape(-1, 1)
        predicted_value = model.predict(new_data_point)

        # Print the predicted value, tahmin edilen
        print("Predicted value:", predicted_value)

        # Create sample data Logistic Regression
        X = np.array([50, 55, 60, 65, 70, 75, 80, 85, 90, 95]).reshape(-1, 1)  # Exam scores
        y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])  # Pass status (0: Fail, 1: Pass)

        # Create a Logistic Regression model
        model = LogisticRegression()
        model.fit(X, y)

        # Make predictions using the model
        new_data_point = np.array([72]).reshape(-1, 1)
        predicted_prob = model.predict_proba(new_data_point)

        # Print the predicted probability of passing
        print("Predicted probability of passing:", predicted_prob[0][1])

        # Create a NumPy array returns the indices that would sort the array
        arr = np.array([10, 5, 8, 20, 3, 15, 7])
        # Specify the number of maximum values you want (N)
        N = 3
        # Get indices of N maximum values
        indices_of_max_values = np.argsort(arr)[-N:]
        indices_of_min_values = np.argsort(arr)[:N]
        # Print the result
        print(
            "Indices of the {} maximum/minimum values: {} / {}".format(N, indices_of_max_values, indices_of_min_values))
        a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        p = np.percentile(a, 25)  # Returns the 50th percentile which is also the median
        print(p)

        # ternary operator, conditional statements
        x, y = 10, 20
        count = x if x < y else y
        res = ("Both x and y are equal" if x == y else "x is greater than y" if x > y else "y is greater than x")

        # pick a random element from a list.
        rnd_value = random.choice(demo_list)

        # return the value of quotient before the decimal point.
        # print(13 // 3)

        output_list = list(map(lambda x: x ** 2, demo_list))
        output_list = list(filter(lambda x: (x > 0 and x % 2 == 0), demo_list))
        output_list = list(filter(lambda x: x > 6, range(9)))

        squared_list = [x ** 2 for x in demo_list]  # list comprehension
        squared_dict = {x: x ** 2 for x in demo_list}  # dict comprehension
        reduce_list = reduce(lambda x, y: x - y, [1, 2, 3, 4, 5]) - 13
        # 1-2 = -1, -1-3 = -4, -4-4 = -8, -8-5 = -13 -> -13 - 13 = -26

        print("The sum of the list elements is : ", end="")
        print(reduce(lambda a, b: a + b, demo_list))
        # print(demo_list[0] + sum(demo_list[1:]))
        print("The sum of the list elements is : ", end="")
        print(reduce(operator.add, demo_list))
        print("The maximum element of the list is : ", end="")
        print(reduce(lambda a, b: a if a > b else b, demo_list))
        print("The concatenated product is : ", end="")
        print(reduce(operator.add, ["geeks", "for", "geeks"]))

        unique_list = list(set(demo_list))
        reversed_list = demo_list[::-1]
        sliced_list = unique_list[1: -1]

        x = array.array('d', [11.1, 2.1, 3.1])
        x.append(10.1)
        x.extend([8.3, 1.3, 5.3])
        x.insert(2, 6.2)
        x.pop()
        x.pop(3)
        x.remove(8.3)
        # [11.1, 2.1, 6.2, 10.1, 1.3]

        numbers = ["2", "5", "7", "8", "1"]
        numbers = [int(i) for i in numbers]
        numbers.sort()

        x = 'a'
        print("ASCII value of '" + x + "' is", ord(x))
        test_inheritance()
        test_abstract_class()

        # Return the serialized data as JsonResponse
        return JsonResponse({'result': numbers}, safe=False)
    else:
        raise ValueError('Method not allowed.')


def example_view(request):
    username = 'John Doe'
    age = 30
    hobbies = ['Reading', 'Coding', 'Hiking']

    context = {
        'username': username,
        'age': age,
        'hobbies': hobbies,
    }

    return render(request, 'example_template.html', context)


@require_http_methods(['GET', 'OPTIONS'])
@csrf_exempt
def get_test_models(request):
    def test_generator(n):

        # initialize counter
        value = 0

        # loop until counter is less than n
        while value < n:
            # produce the current value of the counter
            yield value

            # increment the counter
            value += 1

    try:
        if request.method == 'GET':
            filtered_test_models = TestModel.objects.using('test_db').all()

            # Serialize the queryset to JSON
            serialized_data = [
                {'id': model.id, 'name': model.name, 'age': model.age, 'sub_model_name': model.sub_model.name}
                for model in filtered_test_models
            ]

            input_list = [1, 2, 3, 4, 5]
            output_list = list(map(lambda x: x ** 2, input_list))
            print(output_list)

            output_list = list(filter(lambda x: (x > 0 and x % 2 == 0), input_list))
            print(output_list)

            # Return the serialized data as JsonResponse
            return JsonResponse({'test_models': serialized_data}, safe=False)
        else:
            raise ValueError('Method not allowed.')

    except json.JSONDecodeError:
        response_data = {
            'success': False,
            'message': 'Invalid JSON format in the request body.',
        }
        return JsonResponse(response_data, status=400)

    except ValueError as e:
        response_data = {
            'success': False,
            'message': str(e),
        }
        return JsonResponse(response_data, status=405)


@require_http_methods(['GET', 'OPTIONS'])
@csrf_exempt
def get_test_model_by_sub_model_name(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        sub_model_name = data.get('sub_model_name', '')

        if request.method == 'GET':
            filtered_test_models = TestModel.objects.using('test_db').filter(sub_model__name=sub_model_name)

            # Serialize the queryset to JSON
            serialized_data = [
                {'id': model.id, 'name': model.name, 'age': model.age,
                 'sub_model_id': model.sub_model.id, 'sub_model_name': model.sub_model.name}
                for model in filtered_test_models
            ]

            # Return the serialized data as JsonResponse
            return JsonResponse({'test_models': serialized_data}, safe=False)
        else:
            raise ValueError('Method not allowed.')

    except json.JSONDecodeError:
        response_data = {
            'success': False,
            'message': 'Invalid JSON format in the request body.',
        }
        return JsonResponse(response_data, status=400)

    except ValueError as e:
        response_data = {
            'success': False,
            'message': str(e),
        }
        return JsonResponse(response_data, status=405)


# @transaction.atomic()
class TestApiViewSet(ModelViewSet):
    queryset = TestModel.objects.using('test_db').all()
    serializer_class = TestModelSerializer

    def create(self, request, *args, **kwargs):
        with transaction.atomic(using='test_db'):
            test_sub_model_serializer = TestSubModelSerializer(data=request.data.get('test_sub_model'))
            test_sub_model_serializer.is_valid(raise_exception=True)
            test_sub_model = test_sub_model_serializer.save()

            test_model_data = {
                'name': request.data.get('test_model')['name'],
                'age': request.data.get('test_model')['age'],
                'sub_model': test_sub_model.id
            }

            test_model_serializer = TestModelSerializer(data=test_model_data)
            test_model_serializer.is_valid(raise_exception=True)
            test_model_serializer.save()

            return Response({
                'test_model': test_model_serializer.data,
                'test_sub_model': test_sub_model_serializer.data
            }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        with transaction.atomic(using='test_db'):
            test_model_serializer = TestModelSerializer(instance, data=request.data.get('test_model'), partial=True)
            test_model_serializer.is_valid(raise_exception=True)
            test_model_serializer.save()

            test_sub_model_data = request.data.get('test_sub_model')
            if test_sub_model_data:
                test_sub_model_instance = instance.sub_model
                test_sub_model_serializer = TestSubModelSerializer(test_sub_model_instance, data=test_sub_model_data,
                                                                   partial=True)
                test_sub_model_serializer.is_valid(raise_exception=True)
                test_sub_model_serializer.save()

        return Response({
            'test_model': test_model_serializer.data,
            'test_sub_model': test_sub_model_serializer.data if test_sub_model_data else None
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        with transaction.atomic(using='test_db'):
            test_sub_model_instance = instance.sub_model
            instance.delete()

            if test_sub_model_instance:
                test_sub_model_instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        test_model_serializer = TestModelSerializer(instance)
        test_sub_model_serializer = TestSubModelSerializer(instance.sub_model)

        return Response({
            'test_model': test_model_serializer.data,
            'test_sub_model': test_sub_model_serializer.data
        })
