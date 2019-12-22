def arrayFlattener(Array):
    return __arrayWalker(Array, [])

def __arrayWalker(Array, Accumulator):
    if len(Array)==0:
        return Accumulator
    for i in range(len(Array)):
        if isinstance(Array[i], list):
            __arrayWalker(Array[i], Accumulator)
        else:
            Accumulator.append(Array[i])
    return Accumulator

print(arrayFlattener(['a','b','c']))
print(arrayFlattener([[1,2,[3]],4]))
print(arrayFlattener([['a',2,'d'],4]))
print(arrayFlattener([[1,2,[3]],4, ['a', 'b', 'c']]))
print(arrayFlattener([-1, 0, [1,2,[3]],4]))
