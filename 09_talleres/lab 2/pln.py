# Analizador de Sentimientos Simple - Ejemplo para exposición de PLN

# 1. Diccionarios de palabras (esto simula lo que en la vida real
#    se construye con miles de palabras o se aprende con IA)
palabras_positivas = [
    "feliz", "alegre", "contento", "excelente", "increíble", "genial",
    "encantó", "encanta", "bueno", "buena", "maravilloso", "divertido",
    "divertida", "amo", "amé", "recomiendo", "espectacular", "bien"
]

palabras_negativas = [
    "triste", "mal", "malo", "mala", "pésimo", "horrible", "aburrido",
    "aburrida", "decepcionante", "odio", "odié", "feo", "fea",
    "terrible", "deprimido", "deprimida", "enojado", "enojada"
]

# Conectores que pueden invertir el sentido de la oración
conectores_de_contraste = ["pero", "aunque", "sin embargo"]


def tokenizar(texto):
    """Convierte el texto en una lista de palabras (tokens) en minúsculas."""
    texto = texto.lower()
    # quitamos signos de puntuación básicos
    for signo in [".", ",", "!", "¡", "?", "¿"]:
        texto = texto.replace(signo, "")
    return texto.split()


def analizar_sentimiento(texto):
    tokens = tokenizar(texto)

    puntaje = 0
    encontro_conector = False

    for i, palabra in enumerate(tokens):
        if palabra in conectores_de_contraste:
            encontro_conector = True
            continue

        if palabra in palabras_positivas:
            # si ya pasó un conector de contraste, le damos más peso
            # a lo que viene después (ej: "bueno, PERO aburrido")
            puntaje += 2 if encontro_conector else 1

        elif palabra in palabras_negativas:
            puntaje -= 2 if encontro_conector else 1

    # 2. Clasificación final según el puntaje total
    if puntaje > 0:
        return "😄 Sentimiento POSITIVO (texto feliz)", puntaje
    elif puntaje < 0:
        return "😢 Sentimiento NEGATIVO (texto triste)", puntaje
    else:
        return "😐 Sentimiento NEUTRAL", puntaje


# 3. Programa principal
if __name__ == "__main__":
    print("=== Analizador de Sentimientos ===")
    print("Escribe una frase y te diré si es feliz, triste o neutral.")
    print("(Escribe 'salir' para terminar)\n")

    while True:
        texto_usuario = input("Escribe tu texto: ")

        if texto_usuario.lower() == "salir":
            print("¡Gracias por probar el analizador!")
            break

        resultado, puntaje = analizar_sentimiento(texto_usuario)
        print(f"Resultado: {resultado}  (puntaje: {puntaje})\n")