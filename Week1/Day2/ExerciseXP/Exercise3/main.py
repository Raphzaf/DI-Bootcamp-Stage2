snippets = [
    ("5 < 3", False),
    ("3 == 3", True),
    ('3 == "3"', False),
    ('"3" > 3', "TypeError"),
    ('"Hello" == "hello"', False),
]

for expression, guess in snippets:
    print(f"# Guess: {guess}")
    try:
        print(f">>> {expression} -> {eval(expression)}")
    except TypeError as error:
        print(f">>> {expression} -> {error.__class__.__name__}: {error}")