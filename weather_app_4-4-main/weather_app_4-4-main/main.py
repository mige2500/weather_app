from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather_data(city: str):
    """
    Función que consulta el clima de una ciudad utilizando la API de OpenWeatherMap.
    """
    API_KEY = 'de6f109f28b47876e622310e65fe093b' 
    idioma = 'es'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang={idioma}&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Devuelve los datos en formato JSON si la petición fue exitosa
    return None  # Devuelve None si hubo un error

@app.route("/cv")
def cv():
    return render_template('cv.html')  # Renderiza la página de tu hoja de vida

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Renderiza la página inicial con datos vacíos
        return render_template('index.html', ciudad='', temperatura='', humedad='', presion='', descripcion='', icon='', latitud='', longitud='', temp_min='', temp_max='', feels_like='', clouds='', cod='')

    ciudad = request.form.get('txtCiudad')
    if ciudad:
        data = get_weather_data(ciudad)  # Llama a la API para obtener los datos
        if data and data.get('cod') == 200:
            # Extraer información del JSON
            temperatura = round(data.get('main', {}).get('temp', 'N/A'))  # Temperatura
            humedad = data.get('main', {}).get('humidity', 'N/A')  # Humedad
            presion = data.get('main', {}).get('pressure', 'N/A')  # Presión
            descripcion = data.get('weather', [{}])[0].get('description', 'N/A')  # Descripción
            icon = data.get('weather', [{}])[0].get('icon', 'N/A')  # Icono del clima
            latitud = data.get('coord', {}).get('lat', 'N/A')  # Latitud
            longitud = data.get('coord', {}).get('lon', 'N/A')  # Longitud
            temp_min = round(data.get('main', {}).get('temp_min', 'N/A'))  # Temperatura mínima
            temp_max = round(data.get('main', {}).get('temp_max', 'N/A'))  # Temperatura máxima
            feels_like = round(data.get('main', {}).get('feels_like', 'N/A'))  # Sensación térmica
            clouds = data.get('clouds', {}).get('all', 'N/A')  # Nubosidad

            # Renderiza la página con los datos obtenidos
            return render_template('index.html', ciudad=ciudad, temperatura=temperatura, humedad=humedad, presion=presion, descripcion=descripcion, icon=icon, latitud=latitud, longitud=longitud, temp_min=temp_min, temp_max=temp_max, feels_like=feels_like, clouds=clouds, cod=200)
        else:
            # Renderiza un error si la ciudad no se encontró o hubo algún problema
            return render_template('index.html', ciudad=ciudad, temperatura='', humedad='', presion='', descripcion='', icon='', latitud='', longitud='', temp_min='', temp_max='', feels_like='', clouds='', cod='404')

    # Renderiza la página inicial si no se ingresó ninguna ciudad
    return render_template('index.html', ciudad='', temperatura='', humedad='', presion='', descripcion='', icon='', latitud='', longitud='', temp_min='', temp_max='', feels_like='', clouds='', cod='')

if __name__ == "__main__":
    app.run(debug=True)
