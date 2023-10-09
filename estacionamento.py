import cv2
import numpy as np

vaga1 = [1, 89, 108, 213]
vaga2 = [115, 87, 152, 211]
vaga3 = [289, 89, 138, 212]
vaga4 = [439, 87, 135, 212]
vaga5 = [591, 90, 132, 206]
vaga6 = [738, 93, 139, 204]
vaga7 = [881, 93, 138, 201]
vaga8 = [1027, 94, 147, 202]
png = True

vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8]

video = cv2.VideoCapture('video.mp4')

ret, frame = video.read()
if ret:
    largura = frame.shape[1]
    altura = frame.shape[0]
    #frame = cv2.resize(frame, (640, 480))

#Gravação do Video Resultado
# Define the codec for the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for MP4 format

# Get the frame dimensions and frame rate from the input video
frame_width = int(video.get(3))
frame_height = int(video.get(4))
frame_rate = int(video.get(5))

# Initialize the video writer for the output video
output_video = cv2.VideoWriter('output_video.mp4', fourcc, frame_rate, (frame_width, frame_height))

while True:
    ret, frame = video.read()
    if not ret:
        print("Fim do video")
        break
    
    gray =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur = cv2.medianBlur(tresh, 5)
    kernel = np.ones((3, 3), np.int8)
    Dil = cv2.dilate(blur, kernel)

    for x, y, w, h in vagas:
        recorte = Dil[y:y+h, x:x+w]
        pixels = cv2.countNonZero(recorte)
        cv2.putText(frame, str(pixels), (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        if pixels > 3000:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #Salvando frames
    output_video.write(frame)

    if png:
        cv2.imwrite("Output_image.png", frame)
    png = False
    cv2.imshow("Video_output", frame)
    cv2.imshow("Video_output_binary", Dil)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

output_video.release()
video.release()
cv2.destroyAllWindows()