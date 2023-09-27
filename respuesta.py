import speech_recognition as sr
import pyaudio
import wave
import audioop
import openai
import typer
import config
from rich import print
import time
from elevenlabs import voices, generate, play
from elevenlabs.api import User
from elevenlabs import set_api_key
from elevenlabs.api import Voices


set_api_key(config.EL_api)#Cargar Api Key de Eleven Labs desde el archivo config
user = User.from_api()#Cargar datos del usuario desde la Api de Eleven Labs
voices = Voices.from_api()#Cargar voces desde la Api de Eleven Labs
openai.api_key = config.api_key#Cargar Api Key de OpenAi desde el archivo config

def main():
    # Contexto del asistente
    context = {"role": "user", "content": config.waifu_context}
    messages = [context]

    while True:
        record_audio()
        transcribe_audio(messages)
        generate_response(messages)
        time.sleep(2)  # Esperar 2 segundos antes de volver a grabar

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 2  # Duración máxima de grabación en silencio (segundos)
    THRESHOLD = 1000  # Umbral de amplitud para detectar sonido
    WAVE_OUTPUT_FILENAME = "record.wav"

    p = pyaudio.PyAudio()

    # Configurar los parámetros de grabación de audio
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Grabando audio...")

    frames = []
    silent_frames = 0  # Contador de frames sin sonido

    # Capturar audio del micrófono y almacenar los frames en una lista
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Obtener la amplitud del audio actual
        rms = audioop.rms(data, 2)  # 2 representa el ancho de muestra en bytes (16 bits)

        # Si la amplitud es menor que el umbral, incrementar el contador de frames sin sonido
        if rms < THRESHOLD:
            silent_frames += 1
        else:
            silent_frames = 0  # Restablecer el contador si se detecta sonido

        # Si se alcanza el límite de frames sin sonido, detener la grabación
        if silent_frames >= int(RATE / CHUNK * RECORD_SECONDS):
            break

    print("Grabación finalizada.")

    # Detener y cerrar el stream de audio
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Guardar los frames de audio en un archivo WAV
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(messages):
    # Crear un objeto Recognizer
    r = sr.Recognizer()

    # Especificar el archivo de audio a transcribir
    audio_file = "record.wav"

    # Leer el archivo de audio
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # Leer el audio del archivo

    try:
        # Transcribir el audio utilizando el reconocimiento de voz de Google
        text = r.recognize_google(audio, language="es-ES")
        print("Texto transcrito:")
        print(text)
        messages.append({"role": "user", "content": text})
    except sr.UnknownValueError:
        print("No se pudo transcribir el audio.")

    # Generar respuesta con GPT3.5
def generate_response(messages):
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response_content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_content})
    print(f"[bold green]> [/bold green] [green]{response_content}[/green]")

    # Generar audio con ElevenLabs, definir modelo de voz, elegir voz desde el índice, texto,etc

    voice = voices[10]#voices[N° de la voz en el índice]

    audio = generate(text=response_content, voice=voice, model='eleven_multilingual_v1')#Generar el audio, usando el texto de fuente, la voz elegida y el modelo de preferencia

    #Reproducir audio (depende de ffmpeg, usando ffplay)
    play(audio)

if __name__ == "__main__":
    typer.run(main)
