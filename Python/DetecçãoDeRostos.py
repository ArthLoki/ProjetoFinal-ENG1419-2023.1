import cv2
import math

global imagem
imagem = 0
global faces
faces = []

def atualiza_valores(x,y,w,h):
    global x_novo, y_novo, w_novo, h_novo       
    x_novo = x
    y_novo = y
    w_novo = w
    h_novo = h
    
def streaming(dic, iteracoes):
    
    global x_novo, y_novo, w_novo, h_novo
    global imagem, faces
    
    stream = cv2.VideoCapture(0)
    
    while True:
    
        _, imagem = stream.read()

        # Carregar o classificador Haar Cascade pré-treinado para detecção de faces
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Carregar a imagem em escala de cinza
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        # Realizar a detecção de faces na imagem
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        dist = 1000
        x_novo = dic['x']
        y_novo = dic['y']
        w_novo = dic['w']
        h_novo = dic['h']
        
        # Iterar sobre as faces detectadas
        for (x, y, w, h) in faces:
            
            #calculando o centro da face da ultima posicao
            centro_x1 = dic['x'] + (dic['w'] // 2)
            centro_y1 = dic['y'] + (dic['h'] // 2)
            #calculando o centro da face da posicao atual
            centro_x2 = x + (w // 2)
            centro_y2 = y + (h // 2)
            #comparando a distancia entre os centros para ver se esta perto
            distancia = math.sqrt((centro_x2 - centro_x1)**2 + (centro_y2 - centro_y1)**2)

            #guardando a menor distancia e os valores associados a ela
            if distancia < dist:
                #controlando possiveis "piscadas"
                if distancia>100:
                    iteracoes = iteracoes + 1
                    if iteracoes>3:
                        dist = distancia
                        atualiza_valores(x,y,w,h)
                        iteracoes = 0
                else:
                    dist = distancia
                    atualiza_valores(x,y,w,h)

        #guardando no dicionario
        dic['x'] = x_novo
        dic['y'] = y_novo
        dic['w'] = w_novo
        dic['h'] = h_novo
        
        #calculando o angulo
        centro_x = dic['x'] + (dic['w'] / 2)
        largura_tela = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        centro_da_tela = largura_tela//2
        angulo = (90*centro_x)/centro_da_tela
        print(angulo)
        
        return angulo

def deteccao():
    global imagem, faces
    
    copia = imagem    
    
    for (x, y, w, h) in faces:
        
        cv2.rectangle(copia, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow("Minha Janela", copia)
    #cv2.waitKey(1)
        
    #cv2.stream.release()
    #cv2.destroyAllWindows()

    # Exibir a imagem com as faces detectadas
    #cv2.imshow('Detecção de Faces', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

