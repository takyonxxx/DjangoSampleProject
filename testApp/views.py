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

        # iterate over the generator object produced by my_generator
        # for value in test_generator(3):
        #     # print each value produced by generator

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

        # ternary operator, conditional statements
        x, y = 10, 20
        count = x if x < y else y
        res = ("Both x and y are equal" if x == y else "x is greater than y" if x > y else "y is greater than x")

        x = 'a'
        print("ASCII value of '" + x + "' is", ord(x))

        form_data = request.POST.get('form_data')
        print(form_data)

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
        reduce_list = reduce(lambda x, y: x + y, demo_list)

        #  bir diziyi birikimli olarak işlemek için öğeler üzerine bir ikili işlemi ardışık olarak uygular
        # ilk iki elemandan çıkan sonuç sıradaki elemana uygulanır.
        print("The sum of the list elements is : ", end="")
        print(reduce(lambda a, b: a + b, demo_list))
        # print(reduce(operator.add, demo_list))
        print("The maximum element of the list is : ", end="")
        print(reduce(lambda a, b: a if a > b else b, demo_list))
        print("The concatenated product is : ", end="")
        print(reduce(operator.add, ["geeks", "for", "geeks"]))

        unique_list = list(set(demo_list))
        reversed_list = demo_list[::-1]
        # ilk index dahil (inclusive), son index hariç (exclusive)
        sliced_list = unique_list[1:-1]
        print(unique_list, sliced_list)

        x = array.array('d', [11.1, 2.1, 3.1])
        x.append(10.1)
        x.extend([8.3, 1.3, 5.3])
        x.insert(2, 6.2)
        x.pop()
        x.pop(3)
        x.remove(8.3)
        # [11.1, 2.1, 6.2, 10.1, 1.3]
        print(x)

        numbers = ["2", "5", "7", "8", "1"]
        numbers = [int(i) for i in numbers]
        numbers.sort()
        # Let's print the sorted list
        print("Sorted Numbers:", numbers)
        # Now, let's find the sum of the numbers
        sum_of_numbers = sum(numbers)
        print("Sum of Numbers:", sum_of_numbers)
        # Find the maximum and minimum values in the list
        max_value = max(numbers)
        min_value = min(numbers)
        print("Maximum Value:", max_value)
        print("Minimum Value:", min_value)
        # Let's calculate the average of the numbers
        average_value = sum_of_numbers / len(numbers)
        print("Average Value:", average_value)
        # Finally, let's square each number in the list comprehension
        squared_numbers = [num ** 2 for num in numbers]
        print("Squared Numbers:", squared_numbers)

        my_list = [1, 2, 3]
        print(my_list[0], my_list.index(2))
        repeated_list = my_list * 3
        print("Repeated list:", repeated_list)  # Output: (4, 5, 6, 4, 5, 6, 4, 5, 6)

        my_tuple = (4, 5, 6)
        print(my_tuple[1], my_tuple.index(6))
        repeated_tuple = my_tuple * 3
        print("Repeated tuple:", repeated_tuple)  # Output: (4, 5, 6, 4, 5, 6, 4, 5, 6)

        my_set = {7, 8, 9}
        # No direct indexing in sets
        # You would typically check for membership
        # print(8 in my_set)  # Output: True
        my_set.add(10)
        my_set.remove(8)
        other_set = {9, 10, 11}
        print("My set:", my_set, "Other set:", other_set)
        union_set = my_set.union(other_set)
        print("Union of the two sets:", union_set)  # Output: {7, 9, 10, 11}
        intersection_set = my_set.intersection(other_set)
        print("Intersection of the two sets:", intersection_set)  # Output: {9, 10}
        difference_set = my_set.difference(other_set)
        print("Difference between the two sets:", difference_set)  # Output: {7}
        # Checking if one set is a subset of another
        is_subset = my_set.issubset({7, 9, 10, 11, 12})
        print("Is my_set a subset of {7, 9, 10, 11, 12}?", is_subset)  # Output: True
        # Checking if two sets have no elements in common
        are_disjoint = my_set.isdisjoint({11, 12, 13})
        print("Are my_set and {11, 12, 13} disjoint?", are_disjoint)

        import heapq
        my_heap = [3, 1, 4, 1, 5, 9, 2]
        heapq.heapify(my_heap)
        print("my_heap", my_heap)

        filename = "test_file.txt"
        lines = ["This is Delhi\n", "This is Paris\n", "This is London\n"]
        s = "Hello\n"
        with open(filename, "w") as file:
            file.write(s)
            file.writelines(lines)
        with open(filename, "r") as file:
            # Move the file cursor back to the beginning
            file.seek(0)
            for i, line in enumerate(file):
                pass
        os.remove(filename)

        char = 'HELLO'
        lower_string = char.lower()
        string = 'hello'
        upper_string = string.upper()
        print(lower_string, upper_string)

        # Return the serialized data as JsonResponse
        return JsonResponse({'result': form_data}, safe=False)
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
            # Check if test_model with the given name already exists
            test_model_name = request.data.get('test_model')['name']
            existing_test_model = TestModel.objects.filter(name=test_model_name).first()

            if existing_test_model:
                # If it exists, return a response indicating it already exists
                return Response({
                    'message': f'Test model with name "{test_model_name}" already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)

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