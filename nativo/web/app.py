from flask import Flask, render_template, request

app = Flask(__name__)

OPERACIONES = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def calcular(v1, v2, op):
    """Valida los operandos y la operacion; devuelve (resultado, error)."""
    try:
        a = float(v1)
        b = float(v2)
    except (TypeError, ValueError):
        return None, "Introduce dos numeros validos."

    if op not in OPERACIONES:
        return None, "Operacion no valida."
    if op == "/" and b == 0:
        return None, "No se puede dividir entre cero."

    return OPERACIONES[op](a, b), None


def formatear(valor):
    """Muestra 12 en lugar de 12.0 cuando el resultado es entero."""
    if valor.is_integer():
        return int(valor)
    return round(valor, 6)


@app.get("/")
def formulario():
    return render_template("index.html", v1="", v2="", op="+")


@app.post("/")
def calcular_formulario():
    v1 = request.form.get("v1", "")
    v2 = request.form.get("v2", "")
    op = request.form.get("op", "+")
    resultado, error = calcular(v1, v2, op)
    return render_template(
        "index.html",
        v1=v1,
        v2=v2,
        op=op,
        resultado=formatear(resultado) if resultado is not None else None,
        error=error,
    )
