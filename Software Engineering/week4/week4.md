compiler: parses and simplifies and generalisations 

method overloading only works if the type of the variable is defined in java and python

# Visitor Pattern

- have different classes for different functionality and have corresponding functions to go along with it
- Use abstract classes that classes in the middle inherit from, use polymophism

**chat gpt example:**
```
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

class Cat(Animal):
    def speak(self):
        print("Cat meows")

# Dynamic dispatch in action
def make_animal_speak(animal):
    animal.speak()

# Creating instances
dog = Dog()
cat = Cat()

# Calling the function with different animal objects
make_animal_speak(dog)  # Output: Dog barks
make_animal_speak(cat)  # Output: Cat meows
```

Python iterators

class Iterator:
    def __next__(self):
    .
    .
    ..
it = next(x)


class Iterable:
    def __iter__(self):
    return Iterator()

x = Iterable()
it = iter(x)

iterators are iterables 