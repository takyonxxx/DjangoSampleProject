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
