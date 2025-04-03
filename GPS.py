import time
import paho.mqtt.client as mqtt  # type: ignore

# Configuración del broker de Wokwi (Mosquitto)
WOKWI_BROKER = "test.mosquitto.org"
WOKWI_TOPIC = "gps/coordinates"  # Asegúrate de que este tópico coincida con el del ESP32

# Configuración del broker de Flespi
FLESPI_BROKER = "mqtt.flespi.io"
FLESPI_TOPIC = "gps"  # Tópico en Flespi donde se enviarán los datos
FLESPI_TOKEN = "N1jjPhpPJOlsDOb67SCRqfRDpiNNfsETkHn8ioNoJbJK2kchzca0e0FlU9mMviwg"  # Reemplazar con tu token de Flespi

# Función que se llama cuando el cliente MQTT de Python se conecta al broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker con código {rc}")
    # Suscribir al tópico donde el ESP32 publicará las coordenadas
    client.subscribe(WOKWI_TOPIC)

# Función cuando se recibe un mensaje desde Wokwi
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"📥 Recibido de Wokwi: {payload}")

        # Enviar a Flespi
        flespi_client.publish(FLESPI_TOPIC, payload)
        print(f"📤 Enviado a Flespi: {payload}")

    except Exception as e:
        print(f"⚠ Error al procesar mensaje: {e}")

# Configurar cliente para Wokwi
wokwi_client = mqtt.Client()
wokwi_client.on_connect = on_connect
wokwi_client.on_message = on_message

# Configurar cliente para Flespi
flespi_client = mqtt.Client()
flespi_client.username_pw_set(FLESPI_TOKEN)

try:
    # Conectar a Flespi
    flespi_client.connect(FLESPI_BROKER, 1883)
    flespi_client.loop_start()

    # Conectar a Wokwi
    wokwi_client.connect(WOKWI_BROKER, 1883)
    wokwi_client.loop_start()

    # Mantener el script en ejecución para recibir mensajes
    print("📡 Escuchando datos de Wokwi...")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🔌 Desconectando...")
    wokwi_client.disconnect()
    flespi_client.disconnect()
except Exception as e:
    print(f"❌ Error crítico: {e}")