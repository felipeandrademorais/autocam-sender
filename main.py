import cv2
import paho.mqtt.client as mqtt
import random
import time

# Configurações do MQTT
broker_address = "broker.hivemq.com"
port = 1883
topic = "motor/control"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# Conecte-se ao broker MQTT
client = mqtt.Client(client_id)
client.connect(broker_address, port=port)

# Variáveis para controle do tempo
last_message_time = time.time()


# Carregue o modelo de detector de rostos pré-treinado do OpenCV.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Abra a webcam.
cap = cv2.VideoCapture(0)

while True:
    # Leia um frame da webcam.
    ret, frame = cap.read()
    if not ret:
        break

    # Converta o frame para escala de cinza.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecte rostos no frame.
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Desenhe as linhas que dividem a tela em três partes.
    cv2.line(frame, (int(frame.shape[1]*1/3), 0), (int(frame.shape[1]*1/3), frame.shape[0]), (255, 255, 255), 2)
    cv2.line(frame, (int(frame.shape[1]*2/3), 0), (int(frame.shape[1]*2/3), frame.shape[0]), (255, 255, 255), 2)

    current_time = time.time()
    if current_time - last_message_time >= 1:
        for (x, y, w, h) in faces:
            # Desenhe um retângulo ao redor do rosto.
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            center_x = x + w // 2

            # Se a pessoa estiver na parte esquerda.
            if center_x < frame.shape[1] * 1/3:
                cv2.rectangle(frame, (0, 0), (int(frame.shape[1]*1/3), frame.shape[0]), (0, 0, 255), -1)
                client.publish(topic, "LEFT")
                print("Mova a câmera para a esquerda!")
                last_message_time = current_time

            # Se a pessoa estiver na parte direita.
            elif center_x > frame.shape[1] * 2/3:
                cv2.rectangle(frame, (int(frame.shape[1]*2/3), 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), -1)
                client.publish(topic, "RIGHT")
                print("Mova a câmera para a direita!")
                last_message_time = current_time

        # Resetar as faces para evitar múltiplas mensagens se não houver mudança   
        faces = []

    # Mostre o frame.
    cv2.imshow('Frame', frame)

    # Feche a janela se a tecla 'q' for pressionada.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Quando terminar, libere os recursos e feche todas as janelas.
cap.release()
cv2.destroyAllWindows()
