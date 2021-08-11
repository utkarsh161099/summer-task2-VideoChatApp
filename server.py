import cv2
import socket
import pickle
import struct

# Socket Create
server_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Host_name = socket.gethostname()
Host_IP = socket.gethostbyname(Host_name)
print("Host IP: ", Host_IP)
port = 1111
socket_addr = (Host_IP, port)

# Socket Bind
server_skt.bind(socket_addr)

# Socket Listen
server_skt.listen()
print("Socket is listening at: ", socket_addr)

# Socket Accept
while True:
    client_skt, address = server_skt.accept()
    print("Connnected to ", address)
    if client_skt:
        cam = cv2.VideoCapture(0)
        while(cam.isOpened()):
            ret, img = cam.read()
            data = pickle.dumps(img)
            msg = struct.pack("Q",len(data))+data
            client_skt.sendall(msg)
            cv2.imshow("Transmitting video", img)
            key = cv2.waitKey(1) & 0xFF
            if key==ord('q'):
                client_skt.close()
