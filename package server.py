import socket
import random
def encode(data):
    d = list(map(int,data))

    p1 = (d[0]+d[1]+d[3]+d[4]+d[6]+d[8]+d[10]) % 2
    p2 = (d[0]+d[2]+d[3]+d[5]+d[6]+d[9]+d[10]) % 2
    p4 = (d[1]+d[2]+d[3]+d[7]+d[8]+d[9]+d[10]) % 2
    p8 = (d[4]+d[5]+d[6]+d[7]+d[8]+d[9]+d[10]) % 2

    return str(p1)+str(p2)+data[0]+str(p4)+data[1]+data[2]+data[3]+str(p8)+data[4]+data[5]+data[6]+data[7]+data[8]+data[9]+data[10]
def introduce_error(code):
    code = list(code)
    pos = random.randint(0,14)   # random position
    code[pos] = '1' if code[pos]=='0' else '0'
    return "".join(code), pos+1
def detect_correct(code):
    c = list(map(int,code))

    p1 = (c[0]+c[2]+c[4]+c[6]+c[8]+c[10]+c[12]+c[14]) % 2
    p2 = (c[1]+c[2]+c[5]+c[6]+c[9]+c[10]+c[13]+c[14]) % 2
    p4 = (c[3]+c[4]+c[5]+c[6]+c[11]+c[12]+c[13]+c[14]) % 2
    p8 = (c[7]+c[8]+c[9]+c[10]+c[11]+c[12]+c[13]+c[14]) % 2

    error = p1 + p2*2 + p4*4 + p8*8

    code = list(code)
    if error != 0:
        i = error-1
        code[i] = '1' if code[i]=='0' else '0'

    return "".join(code), error
def decode(code):
    return code[2]+code[4]+code[5]+code[6]+code[8]+code[9]+code[10]+code[11]+code[12]+code[13]+code[14]
HOST = "127.0.0.1"
PORT = 5000

server = socket.socket()
server.bind((HOST,PORT))
server.listen(1)

print("Server running...")

while True:
    conn,addr = server.accept()

    data = conn.recv(1024).decode()

    encoded = encode(data)
    corrupted, pos = introduce_error(encoded)
    corrected, error = detect_correct(corrupted)
    decoded = decode(corrected)

    result = f"""
Original: {data}
Encoded: {encoded}
Corrupted: {corrupted}
Error Position: {error}
Corrected: {corrected}
Decoded: {decoded}
"""

    conn.send(result.encode())
    conn.close()