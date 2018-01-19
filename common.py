

def find_attr_by_name(attrs, name):
    for n, v in attrs:
        if n == name:
            return v
    return None