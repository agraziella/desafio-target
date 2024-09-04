def fibonacci(n):
    a, b = 0, 1
    while a < n:
        a, b = b, a + b
    return a == n

# Número a ser verificado
num = 21

if fibonacci(num):
    print(f"{num} pertence à sequência de Fibonacci.")
else:
    print(f"{num} não pertence à sequência de Fibonacci.")
