import sys

def debug(*args, **kwargs):
    print(*args, **kwargs)  # Igual que print()

def tam_total(obj):
    """Calcula el tamaño en bytes de un objeto y sus elementos recursivamente."""
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(tam_total(k) + tam_total(v) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(tam_total(x) for x in obj)
    return size

# mi_lista = ["hola", 3.14, {"clave": "valor"}, [1, 2, 3]]
# print(f"Tamaño total de la lista: {tam_total(mi_lista)} bytes")
