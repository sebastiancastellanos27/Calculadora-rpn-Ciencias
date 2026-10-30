
import re


class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho


def construir_arbol(expresion):
    tokens = re.findall(
        r"\d+(?:\.\d+)?|[()+\-*/]",
        expresion.replace(" ", "")
    )

    # Verificar que todos los caracteres sean válidos
    if "".join(tokens) != expresion.replace(" ", ""):
        raise ValueError("Hay caracteres no válidos")

    if not tokens:
        raise ValueError("La expresión está vacía")

    posicion = 0

    def expresion_arbol():
        nonlocal posicion

        nodo = termino()

        while posicion < len(tokens) and tokens[posicion] in ("+", "-"):
            operador = tokens[posicion]
            posicion += 1
            derecho = termino()
            nodo = Nodo(operador, nodo, derecho)

        return nodo

    def termino():
        nonlocal posicion

        nodo = factor()

        while posicion < len(tokens) and tokens[posicion] in ("*", "/"):
            operador = tokens[posicion]
            posicion += 1
            derecho = factor()
            nodo = Nodo(operador, nodo, derecho)

        return nodo

    def factor():
        nonlocal posicion

        if posicion >= len(tokens):
            raise ValueError("Falta un número u operando")

        token = tokens[posicion]
        posicion += 1

        if token == "(":
            nodo = expresion_arbol()

            if posicion >= len(tokens) or tokens[posicion] != ")":
                raise ValueError("Faltan paréntesis de cierre")

            posicion += 1
            return nodo

        if token in ("+", "-", "*", "/", ")"):
            raise ValueError(f"Elemento inesperado: {token}")

        return Nodo(float(token))

    arbol = expresion_arbol()

    if posicion != len(tokens):
        raise ValueError("La expresión no es válida")

    return arbol


def recorrido_postorden(nodo):
    if nodo is None:
        return []

    return (
        recorrido_postorden(nodo.izquierdo)
        + recorrido_postorden(nodo.derecho)
        + [nodo.valor]
    )


def calcular_con_arbol(expresion):
    arbol = construir_arbol(expresion)

    elementos = recorrido_postorden(arbol)
    npi = " ".join(
        str(int(x)) if isinstance(x, float) and x.is_integer()
        else str(x)
        for x in elementos
    )

    resultado = calcular_npi(npi)

    return npi, resultado



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
        print("3. Expresión algebraica con árbol")
        print("4. Salir")

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
            expresion = input(
                "\nExpresión algebraica: "
            ).strip()

            try:
                npi, resultado = calcular_con_arbol(expresion)

                print("Expresión en NPI:", npi)

                if resultado.is_integer():
                    resultado = int(resultado)

                print("Resultado:", resultado, "\n")

            except (ValueError, ZeroDivisionError) as error:
                print("Error:", error, "\n")

        elif opcion == "4":
            print("Hasta luego.")
            break

        else:
            print("Opción no válida.\n")


if __name__ == "__main__":
    main()
