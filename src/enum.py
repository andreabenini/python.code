# Simplest method ever: one function, one var
def enum(**enums):
    return type('Enum', (), enums)

DEBUG = enum(OFF=0, ON=1, VERBOSE=2)
print(DEBUG.OFF, DEBUG.ON, DEBUG.VERBOSE)

# With a class, overhead and heavy but classy:
from enum import Enum
class Animal(Enum):
    ant = 1
    bee = 2
    cat = 3
    dog = 4

print(Animal.bee.name, Animal['bee'].value, Animal.bee.value)

