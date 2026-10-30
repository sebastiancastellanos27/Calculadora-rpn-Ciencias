
def calcular_npi(expresion):
    pila = []
    operadores = ["+", "-", "*", "/"]

    elementos = expresion.split()

    for elemento in elementos:

        # Si el elemento es un número
        if elemento not in operadores:
            try:
                numero = float(elemento)
                pila.append(numero)
            except ValueError:
                raise ValueError(
                    f"Elemento no válido: {elemento}"
                )

        # Si el elemento es un operador
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

    # Validar que solo quede un resultado
    if len(pila) != 1:
        raise ValueError("La expresión no es válida")

    return pila[0]


def main():
    print("=== CALCULADORA NPI ===")
    print("Operadores: +, -, *, /")
    print("Escribe 'salir' para terminar.")
    print("Separa los números y operadores con espacios.\n")

    while True:
        expresion = input("Expresión postfija: ").strip()

        if expresion.lower() == "salir":
            print("Hasta luego.")
            break

        if not expresion:
            print("Debes ingresar una expresión.\n")
            continue

        try:
            resultado = calcular_npi(expresion)

            # Mostrar enteros sin .0
            if resultado.is_integer():
                resultado = int(resultado)

            print("Resultado:", resultado, "\n")

        except (ValueError, ZeroDivisionError) as error:
            print("Error:", error, "\n")


if __name__ == "__main__":
    main()
