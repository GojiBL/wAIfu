# wAIfu
El codigo funciona utilizando GPT3.5 de OpenAi como modelo de conversación para simular la personalidad de algún personaje mediante un prompt o contexto (similar a CharacterAi), usando reconocimiento de voz (Speech Recognition) se grabará un audio de tu voz utilizando el microfono por defecto del equipo, el audio se guardará en un archivo el cual luego será transcrito con el SpeechRecognition de Google. GPT leerá ese texto transcrito como mensaje de entrada y su respuesta será leída con un TTS gracias a ElevenLabs.

# Instalación
° Copiar el repositorio a un equipo local e instalar los requerimientos
```
git clone https://github.com/GojiBL/wAIfu
cd wAIfu
pip install -r requirements.txt
```
° Se necesita tener instalado [`ffmpeg`](https://ffmpeg.org/) en el equipo para funcionar.

# Como usar
° Reemplazar las variables dentro del archivo `config.py` con sus respectivas API-KEYs y el contexto/prompt del personaje
```
api_key = "ApiKeyOpenAi" --> Aquí debe ir la Api key de OpenAi
EL_api = "ApiKeyElevenLabs" --> Aquí debe ir la Api key de ElevenLabs

waifu_context = "Contexto PJ" --> Aquí debe ir el contexto/personalidad de su personaje 
```
Las API-KEYs pueden ser encontradas en los ajustes de sus perfiles de los respectivos sitios webs.

° Luego de eso pueden ejecutar el archivo `respuesta.py`, o en su lugar crear un archivo .bat en la siguiente forma
```
@echo off
"Ubicación de Python en su equipo\python.exe" "Ubicación donde copiaron el repositorio\respuesta.py"
pause
```
# Demostración
Video de documentación y resumen del proyecto (NO ES UN TUTORIAL)

[![Cómo Hice UNA WAIFU Con IA](https://img.youtube.com/vi/leK5dPTb8t8/0.jpg)](https://www.youtube.com/watch?v=leK5dPTb8t8 "Cómo Hice UNA WAIFU Con IA")

# Detalles
La voz pueden cambiarla a la de su elección modificando la siguiente línea de texto dentro del archivo `respuesta.py` (Line 113)
```
voice = voices[1]
```
Donde el número entre corchetes corresponde al de la voz según su posición en el índice de voces del usuario. Pueden obtener su índice de voces ejecutando el siguiente código
```
from elevenlabs.api import Voices
from elevenlabs import set_api_key

set_api_key("ApiKeyElevenLabs")

voices = Voices.from_api()
print(voices)
```
En su lugar, en vez de usar el número del índice, pueden escribir el nombre de la voz en cuestión, pero esto solo funciona con las voces predeterminadas de ElevenLabs.
Pueden encontrar información más detallada en el respositorio [`elevenlabs-python`](https://github.com/elevenlabs/elevenlabs-python)

# Extra
Pueden usar el driver de [VB Audio cable](https://vb-audio.com/Cable/) para lograr que el modelo mueva la boca en Vtube Studio como lo hice yo.

# Comentarios
Por favor entiendan que este fue un proyecto que comenzó como una broma entre amigos y escaló hasta convertirse en algo personal hecho meramente por diversión, nunca hubo una intención de crear algo masivo o profesional, por lo que es muy probable que se encuentren ante un código amateur y mal optimizado. Sin embargo, debido al apoyo en Youtube he decidido hacer pública la primera versión funcional del codigo con la intención de que aquellos interesados y con mayor experiencia puedan hacer aportes si así lo desean, en mi perfil pueden encontrar las redes por las cuales pueden contactarme.

Abajo hay una lista de cosas que me gustaría lograr:

- [ ] Personaje con "memoria" (Recordar contextos de la conversación anterior luego de cerrar el programa)
- [ ] Interfaz gráfica
- [ ] Capturar imagen Spout2 desde VTube Studio
- [ ] Optimizar código
- [ ] Optimizar velocidad de respuesta
- [ ] (OPCIONAL) Integración con Discord
