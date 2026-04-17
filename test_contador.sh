#!/bin/bash
# test_contador.sh - Script para git bisect run
# Retorna 0 (good) si python contador.py 5 imprime 6
# Retorna 1 (bad)  si imprime cualquier otro valor

python contador.py 5 | grep -qx "6"
