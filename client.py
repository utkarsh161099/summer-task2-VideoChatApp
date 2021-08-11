import cv2
import socket
import pickle
import struct

client_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_IP = "192.168.237.1"
port = 1111
client_skt.connect((server_IP, port))
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_skt.recv(4*1024)
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data+=client_skt.recv(4*1024)
    img_data = data[:msg_size]
    data = data[msg_size:]
    img = pickle.loads(img_data)
    cv2.imshow("Receiving Video",img)
    if cv2.waitKey(1) == 13:
        break
client_skt.close()
cv2.destroyAllWindows()
