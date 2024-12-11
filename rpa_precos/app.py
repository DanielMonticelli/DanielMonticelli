from classes import RPA # Podemos importar desta forma devido ao __init__.py em app


if __name__ == "__main__": # Assim o código só pode ser executado por este arquivo diretamente
    rpa = RPA()
    prices = rpa.run()

    print(prices) # Imprimindo valores no terminal, podes fazer o que quiser a partir daqui
