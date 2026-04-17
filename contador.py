# contador.py

# Versión inicial correcta

def siguiente(n):
    return n + 2  # BUG intencionado: debería ser +1

if __name__ == "__main__":
    import sys
    valor = int(sys.argv[1])
    print(siguiente(valor))
# Log: añadido comentario 1
# Log: añadido comentario 2
# Log: añadido comentario 3
