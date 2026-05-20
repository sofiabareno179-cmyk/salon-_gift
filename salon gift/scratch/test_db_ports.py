import socket

ports = [500, 5431, 5432, 5000]
for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        s.connect(('127.0.0.1', port))
        print(f"Port {port} is OPEN")
        s.close()
    except Exception as e:
        print(f"Port {port} is CLOSED: {e}")
