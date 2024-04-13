import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2

# Inicialização de variáveis globais
toggle_alert = True
manual_move = None
cap = cv2.VideoCapture(5)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Função para captura contínua da câmera
def capture_video():
    global toggle_alert, manual_move, cap
    ret, frame = cap.read()
    if not ret:
        root.after(10, capture_video)
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Após processar, convertemos o frame para formato do Tkinter
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    label_video.imgtk = imgtk
    label_video.configure(image=imgtk)

    # Agendamos a próxima captura
    root.after(10, capture_video)

# Função para alternar alertas
def toggle_alert_status():
    global toggle_alert
    toggle_alert = not toggle_alert
    button_toggle_alert.config(text='Desativar Alerta' if toggle_alert else 'Ativar Alerta')

# Função para mover a câmera manualmente
def move_camera(direction):
    global manual_move
    manual_move = direction
    # Aqui você implementaria a função que move a câmera
    print(f"Mover câmera para: {direction}")

# Função para sair da aplicação
def on_closing():
    if messagebox.askokcancel("Sair", "Deseja fechar o aplicativo?"):
        global cap
        cap.release()
        cv2.destroyAllWindows()
        root.destroy()

# Configuração da janela principal do Tkinter
root = tk.Tk()
root.title("Controle da Câmera")

# Criação do label onde o vídeo será exibido
label_video = tk.Label(root)
label_video.pack()

# Botões
button_frame = tk.Frame(root)  # Frame para conter os botões
button_frame.pack(side=tk.BOTTOM)  # Coloca o frame na parte inferior da janela

button_toggle_alert = tk.Button(button_frame, text="Ativar Alerta", command=toggle_alert_status)
button_toggle_alert.pack(side=tk.LEFT)

button_left = tk.Button(button_frame, text="Esquerda", command=lambda: move_camera('left'))
button_left.pack(side=tk.LEFT)

button_right = tk.Button(button_frame, text="Direita", command=lambda: move_camera('right'))
button_right.pack(side=tk.LEFT)

# Inicia a captura de vídeo com a função after em vez de usar uma thread
root.after(0, capture_video)

# Tratamento do evento de fechamento da janela
root.protocol("WM_DELETE_WINDOW", on_closing)

# Inicia o loop principal do Tkinter
root.mainloop()
