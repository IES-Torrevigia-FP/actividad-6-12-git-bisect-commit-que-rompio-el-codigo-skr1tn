# contador.py

# Versión inicial correcta

def siguiente(n):
    return n + 1

if __name__ == "__main__":
    import sys
    valor = int(sys.argv[1])
    print(siguiente(valor))
