import array
import json
import operator
import os
import random
import unittest
from functools import reduce, partial

import requests
from django.db import transaction, connection
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.response import Response

from testApp.models import Customer
from testApp.serializers import CustomerSerializer
from .models import Order
from .serializers import OrderSerializer


class TestAPIRequests(unittest.TestCase):
    def make_api_request(self, method='GET'):
        url = 'http://127.0.0.1:8000/docs'
        response = requests.request(method, url)
        return response

    def test_successful_request(self):
        response = self.make_api_request()
        self.assertEqual(response.status_code, 200)

    def test_invalid_method(self):
        response = self.make_api_request(method='POST')
        self.assertEqual(response.status_code, 405)


def run_test_api_requests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPIRequests)
    # Run the entire test suite using TextTestRunner
    unittest.TextTestRunner().run(suite)


def handle_attribute_error(class_or_method):
    if isinstance(class_or_method, type):  # If it's a class
        for name, value in vars(class_or_method).items():
            if callable(value):
                setattr(class_or_method, name, handle_attribute_error(value))
            elif isinstance(value, type):  # If it's a nested class
                setattr(class_or_method, name, handle_attribute_error(value))
        return class_or_method
    else:  # If it's a method
        def decorated_method(*args, **kwargs):
            if 'username' not in kwargs or 'password' not in kwargs:
                raise AttributeError("Both 'username' and 'password' must be provided.")
            try:
                return class_or_method(*args, **kwargs)
            except AttributeError as e:
                raise e  # Re-raise the original AttributeError for other attributes

        return decorated_method


@handle_attribute_error
class MyBaseClass:
    instance = None

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        # self.test = kwargs['test']
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.args = args
        self.kwargs = kwargs


# @custom_exception_decorator
class MyChildClass(MyBaseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@require_http_methods(['POST', 'OPTIONS'])
@csrf_exempt
def test_db(request):
    def email_user(email):
        print(f"Dear {email}, Thank You.")

    if request.method == 'POST':
        with transaction.atomic():
            customers = Customer.objects.select_for_update(). \
                filter(Q(name__startswith='Türk') | Q(name__startswith='Gök'))

            # Serialize all posts at once
            serialized_customers = CustomerSerializer(customers, many=True).data
            _q = customers.query
            _c = connection.queries
        if serialized_customers:
            partial_email_user = partial(email_user, "turkaybiliyor@hotmail.com")
            transaction.on_commit(partial_email_user)
            for item in serialized_customers:
                # Modify the additional_info field for each object
                item['additional_info'] = "Mail has been sent to turkaybiliyor@hotmail.com."
            return JsonResponse(serialized_customers, safe=False)  # non dict object --> safe=False
        else:
            return JsonResponse({'error': 'No data to serialize.'}, status=400)
    else:
        raise ValueError('Method not allowed.')


@require_http_methods(['POST', 'OPTIONS'])
@csrf_exempt
def test_api(request):
    if __name__ == "__main__":
        print("This is the main block of code.")
    else:
        print("This is not the main block of code.")

    if request.method == 'POST':

        import heapq
        my_heap = [3, 1, 4, 1, 5, 9, 2]
        heapq.heapify(my_heap)
        print("my_heap", my_heap)

        import copy
        # Sample list
        original_list = [1, 2, [3, 4]]
        # Shallow copy
        shallow_copied_list = copy.copy(original_list)
        # Deep copy
        deep_copied_list = copy.deepcopy(original_list)
        # Modifying the original list
        original_list[2][0] = 'X'
        # Displaying the results
        print("Original List:", original_list)
        print("Shallow Copy:", shallow_copied_list)
        print("Deep Copy:", deep_copied_list)

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

        demo_list = [5, 4, 4, 6, 8, 12, 12, 1, 5]

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
        output_list_even = list(filter(lambda x: (x > 0 and x % 2 == 0), demo_list))  # even number
        output_list_odd = list(filter(lambda x: (x > 0 and x % 2 != 0), demo_list))  # odd number
        print('even', output_list_even, 'odd', output_list_odd)
        output_list = list(filter(lambda x: x > 6, range(9)))  # [7, 8]

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

        obj = Customer.objects.get(id=1)
        class_name_from_obj = obj.__class__.__name__
        class_name = Customer.__name__
        print(class_name, class_name_from_obj)  # class ismi
        print(__name__)  # modül ismi
        print(obj)  # return __str__ magic function

        # Call run_test_api_requests to execute a specific test method
        # run_test_api_requests()

        base_instance = MyBaseClass(instance='Base_Instance',
                                    username="username", password="password")
        print("Base:", base_instance.username)

        child_instance = MyChildClass(instance='Child_Instance',
                                      username="child_username", password="child_password")
        print("Child:", child_instance.username)

        # Return the serialized data as JsonResponse
        return JsonResponse({'result': form_data}, safe=False)
    else:
        raise ValueError('Method not allowed.')


def docs(request):
    return render(request, 'docs.html')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
