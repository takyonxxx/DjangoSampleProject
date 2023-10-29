from .models import Employee, ManagerProxy, Person, Article, Comment


def test_inheritance():
    # Abstract Base Class
    person = Person(name='John Doe', age=30)
    person.save()

    # Multi-table Inheritance
    employee = Employee(name='Jane Doe', age=25, position='Developer')
    employee.save()

    # Proxy Model
    manager_proxy = ManagerProxy(name='Alice', age=35)
    manager_proxy.save()

    # Querying
    people = Person.objects.all()
    employees = Employee.objects.all()
    managers = ManagerProxy.objects.all()

    return {'people': people, 'employees': employees, 'managers': managers}


# Usage example in views.py or elsewhere
def test_abstract_class():
    # Creating an article
    article = Article.objects.create(title='Sample Article', content='This is the content of the article')
    # Creating a comment
    comment = Comment.objects.create(author='John Doe', text='Great article!')

    # Accessing common fields
    print(article.created_at)  # Accessing 'created_at' from CommonFields
    print(comment.updated_at)  # Accessing 'updated_at' from CommonFields


class Animal:
    def __init__(self, species):
        self.species = species

    def speak(self):
        print(f"Animal of species {self.species} speaks")


class Mammal:
    def __init__(self, mammal_type):
        self.mammal_type = mammal_type

    def give_birth(self):
        print(f"{self.mammal_type} gives birth")


class Dog(Animal, Mammal):
    def __init__(self, species, mammal_type, breed):
        # Call the __init__ methods of both parent classes using super()
        super().__init__(species)
        super(Mammal, self).__init__(mammal_type)
        self.breed = breed

    def bark(self):
        print(f"{self.breed} dog barks")


def test_multi_inheritance():
    # Create an instance of Dog
    my_dog = Dog(species="Canine", mammal_type="Mammal", breed="Golden Retriever")

    # Access methods and attributes from all parent classes and the current class
    my_dog.speak()  # Inherited from Animal
    my_dog.give_birth()  # Inherited from Mammal
    my_dog.bark()  # Defined in Dog class

    # Access attributes specific to Dog class
    print(f"Breed: {my_dog.breed}")
