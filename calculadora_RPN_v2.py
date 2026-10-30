
def calcular_npi(expresion):
    pila = []
    operadores = ["+", "-", "*", "/"]

    elementos = expresion.split()

    for elemento in elementos:
        if elemento not in operadores:
            try:
                numero = float(elemento)
                pila.append(numero)
            except ValueError:
                raise ValueError(f"Elemento no válido: {elemento}")

        else:
            if len(pila) < 2:
                raise ValueError("Faltan operandos")

            b = pila.pop()
            a = pila.pop()

            if elemento == "+":
                resultado = a + b
            elif elemento == "-":
                resultado = a - b
            elif elemento == "*":
                resultado = a * b
            elif elemento == "/":
                if b == 0:
                    raise ZeroDivisionError(
                        "No se puede dividir entre cero"
                    )
                resultado = a / b

            pila.append(resultado)

    if len(pila) != 1:
        raise ValueError("La expresión no es válida")

    return pila[0]


def calcular_paso_a_paso():
    pila = []
    operadores = ["+", "-", "*", "/"]

    print("\n=== MODO PASO A PASO ===")
    print("Introduce un número o un operador.")
    print("Escribe 'fin' para terminar o 'cancelar' para salir.\n")

    while True:
        elemento = input("Número u operador: ").strip()

        if elemento.lower() == "cancelar":
            print("Operación cancelada.\n")
            return

        if elemento.lower() == "fin":
            break

        if not elemento:
            print("Introduce un valor.\n")
            continue

        if elemento in operadores:
            if len(pila) < 2:
                print("Error: faltan operandos.\n")
                print("Pila actual:", pila)
                continue

            b = pila.pop()
            a = pila.pop()

            try:
                if elemento == "+":
                    resultado = a + b
                elif elemento == "-":
                    resultado = a - b
                elif elemento == "*":
                    resultado = a * b
                elif elemento == "/":
                    if b == 0:
                        raise ZeroDivisionError(
                            "No se puede dividir entre cero"
                        )
                    resultado = a / b

                pila.append(resultado)

            except ZeroDivisionError as error:
                # Restaurar los operandos si falla la división
                pila.append(a)
                pila.append(b)
                print("Error:", error, "\n")
                print("Pila actual:", pila)
                continue

        else:
            try:
                numero = float(elemento)
                pila.append(numero)
            except ValueError:
                print(f"Elemento no válido: {elemento}\n")
                print("Pila actual:", pila)
                continue

        print("Pila:", pila, "\n")

    if len(pila) == 1:
        resultado = pila[0]

        if resultado.is_integer():
            resultado = int(resultado)

        print("Resultado final:", resultado, "\n")
    elif len(pila) == 0:
        print("La pila está vacía.\n")
    else:
        print("Error: la expresión está incompleta.")
        print("Pila final:", pila, "\n")


def main():
    while True:
        print("=== CALCULADORA NPI ===")
        print("1. Introducir expresión completa")
        print("2. Calcular paso a paso")
        print("3. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            expresion = input(
                "\nExpresión postfija: "
            ).strip()

            if not expresion:
                print("Debes ingresar una expresión.\n")
                continue

            try:
                resultado = calcular_npi(expresion)

                if resultado.is_integer():
                    resultado = int(resultado)

                print("Resultado:", resultado, "\n")

            except (ValueError, ZeroDivisionError) as error:
                print("Error:", error, "\n")

        elif opcion == "2":
            calcular_paso_a_paso()

        elif opcion == "3":
            print("Hasta luego.")
            break

        else:
            print("Opción no válida.\n")


if __name__ == "__main__":
    main()
