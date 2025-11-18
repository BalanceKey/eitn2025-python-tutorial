
def print_hello():
    print("Hello world!")

def add_numbers(a, b):
    return a + b

def youngest(name_age_dict):
    min_age = min(name_age_dict.values())
    names = [name for name, age in name_age_dict.items() if age == min_age]
    return names


def oldest(name_age_dict):
    max_age = max(name_age_dict.values())
    names = [name for name, age in name_age_dict.items() if age == max_age]
    return names
