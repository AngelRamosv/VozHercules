import random
import speech_recognition as sr
import pyttsx3
import time
import datetime

# Lista de chistes
chistes = [
    "Están dos piojos en la cabeza de un señor calvo, y uno le dice al otro: Luis, vámonos de aquí que este terreno ya está pavimentado jajaja rianse un poquito y no sean amargados por favor",
    "¿Por qué un huevo fue al banco a pedir dinero prestado? Porque estaba quebrado. la neta este esta muy bueno amiguito así que riete un poquito quieres",
    "¡Mamá, mamá, he sacado un 10! ¡Ah, sí! ¿En qué asignatura? Pues... un 3 en matemáticas, un 2 en lengua, un 3 en inglés y un 2 en geografía. Este si da risa alegrate un poquito la vida",
    "¡Me tienes harta, Pedro! Lo único que haces es comer. A lo que Pedro responde: ¿A que te refieres croquetamente?muy buen chiste para alegrar el día jejeje",
    "Los alumnos de la uam llevan una uea, sin saber que significa, universidad especialista de alcolicos jijiji si a ti no te gusto pues a mi si y te toca soportar",
    "Acabo de escribir un libro. ¿Y por qué has dibujado un dedo en la primera página? Es el índice. jajaja este es otro de mis chascarrillos más famosos",
    "Carlos le dice a María ¿Y cómo va tu vida amorosa? a lo que María responde pues como la Coca-Cola: primero normal, luego light y ahora zero. Este si da risa y si no te dió risa pues creo que el soltero eres tu por amargado jajaja"
]

# Lista de curiosidades
curiosidades = [
    "El río Amazonas: Este río es el más largo y caudaloso del mundo, con una longitud aproximada de 7,062 kilómetros. Lo que lo hace aún más fascinante es que también es el hogar de una increíble diversidad de vida acuática y terrestre, muchas de las cuales son especies endémicas.",
    "La miel nunca se echa a perder. Se han encontrado frascos de miel en tumbas egipcias que tienen más de 3000 años y aún son comestibles.",
    "Los pulpos tienen tres corazones y la sangre azul, un animal único en su especie y bastante interesante.",
    "El estado de Alaska es el estado más grande de los Estados Unidos por área total, pero tiene la menor población de todos los estados.",
    "La Gran Muralla China tiene más de 2.000 años y es la estructura hecha por el hombre más larga del mundo.",
    "En la época de su construcción, el Titanic era el barco más grande y lujoso del mundo.",
    "El Gran Cañón del Colorado: Ubicado en el estado de Arizona, Estados Unidos, este impresionante cañón tiene una profundidad de hasta 1,800 metros y una longitud de aproximadamente 446 kilómetros. Lo sorprendente es que estas formaciones rocosas revelan millones de años de historia geológica de la Tierra."
]

# Función para detectar cualquier palabra de inicio
def esperar_inicio(recognizer):
    print("Esperando saludo...")
    while True:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            palabra = recognizer.recognize_google(audio, language="es-ES").lower()
            print(f"Palabra reconocida: {palabra}")
            return True
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Error en la solicitud de reconocimiento de voz:", e)

# Función para configurar el motor de síntesis de voz
def configurar_motor():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Cambiar el índice si no te gusta la voz
    engine.setProperty('rate', 125)  # Velocidad de la voz
    engine.setProperty('pitch', 5)   # Tono de la voz
    return engine

# Lista de respuestas para la bienvenida
respuestas_bienvenida = [
    "Hola a todos, bienvenidos a la universidad autónoma metropolitana, unidad Iztapalapa, referente al evento de ingeniería Carlos Gref..."
]

# Lista de respuestas para despedida
respuestas_despedida = [
    "Hemos llegado al laboratorio principal, me despido de todos ustedes. ¡Hasta luego!"
]

# Función para construir y reproducir la respuesta de manera aleatoria
def responder_aleatorio(respuestas, engine):
    respuesta = random.choice(respuestas)
    engine.say(respuesta)
    engine.runAndWait()

# Función para reconocer la orden del usuario
def reconocer_orden(recognizer, engine):
    engine.say("Dame una orden para realizarla")
    engine.runAndWait()

    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        orden = recognizer.recognize_google(audio, language="es-ES").lower()
        return orden
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Error en la solicitud de reconocimiento de voz:", e)
        return None

# Función para obtener la hora actual
def obtener_hora_actual():
    now = datetime.datetime.now()
    hora = now.strftime("%I:%M %p")
    return hora

# Función para contar una curiosidad
def contar_curiosidad(respuestas, engine):
    curiosidad = random.choice(respuestas)
    engine.say(curiosidad)
    engine.runAndWait()

# Función principal
def main():
    recognizer = sr.Recognizer()
    engine = configurar_motor()

    if esperar_inicio(recognizer):
        responder_aleatorio(respuestas_bienvenida, engine)

        time.sleep(2)  # Pausa antes de preguntar

        responder_aleatorio(["Les tengo un menú de opciones que pueden elegir para que yo realice una tarea para ustedes. (Puedo dar la hora del día, puedo contar un chiste, puedo decir alguna curiosidad del mundo)"], engine)

        while True:
            orden_encontrada = None
            orden = None
            while not orden:
                orden = reconocer_orden(recognizer, engine)
                if not orden:
                    responder_aleatorio(["No pude entender la orden. ¿Podrías repetirla?"], engine)
            
            if "chiste" in orden or "chistes" in orden:
                chiste = random.choice(chistes)
                responder_aleatorio([chiste], engine)
                responder_aleatorio(["He dicho el chiste, ¿Quieren que haga algo más? Responde si quiero otra orden o no quiero otra orden"], engine)

            elif "hora" in orden:
                hora_actual = obtener_hora_actual()
                responder_aleatorio([f"Son las {hora_actual}. He dicho la hora. ¿Quieren que haga algo más?"], engine)

            elif "curiosidad" in orden or "curiosidades" in orden:
                contar_curiosidad(curiosidades, engine)
                responder_aleatorio(["He dicho la curiosidad. ¿Quieres que haga algo más?"], engine)

            else:
                responder_aleatorio(["Lo siento, no entiendo la orden. ¿Puedes intentar con otra cosa?"], engine)

            # Escuchar la respuesta del usuario
            respuesta_usuario = None
            while respuesta_usuario is None:
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                try:
                    respuesta_usuario = recognizer.recognize_google(audio, language="es-ES").lower()
                    if respuesta_usuario == "no quiero otra orden":
                        responder_aleatorio(respuestas_despedida, engine)
                        return  # Salir del programa
                    elif respuesta_usuario == "si quiero otra orden":
                        responder_aleatorio(["Dime qué otra cosa hago por ti"], engine)
                        break  # Salir del bucle actual y esperar una nueva orden
                    else:
                        responder_aleatorio(["En qué más te puedo servir?"], engine)
                except sr.UnknownValueError:
                    responder_aleatorio(["No pude entender tu respuesta. ¿Quieres que haga algo más por ti?"], engine)
                except sr.RequestError as e:
                    print("Error en la solicitud de reconocimiento de voz:", e)
                    responder_aleatorio(["Lo siento, ocurrió un error. Intenta de nuevo."], engine)

# Ejecutar el programa desde el main
if __name__ == "__main__":
    main()
