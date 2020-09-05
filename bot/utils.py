import re

def get_cases(source):
    parts = source.split("-") if len(source.split("-")) > 1 else source.split("_")

    if len(parts) > 1:
        snake_case = "_".join(p.lower() for p in parts)
        camelCase = "".join(p.title() for p in parts)
    else:
        snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', source).lower()
        camelCase = "".join(p.title() for p in snake_case.split("_"))

    return snake_case, camelCase
