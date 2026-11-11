#!/usr/bin/env python3
"""
Servidor TCP (ejecutar en la VM 1).
Uso: python3 servidor.py [puerto]
"""
import socket
import sys
import threading

HOST = "0.0.0.0"  # Escucha en todas las interfaces de la VM
PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 5000


def atender_cliente(conn, addr):
    print(f"[+] Conectado: {addr[0]}:{addr[1]}")
    with conn:
        while True:
            datos = conn.recv(1024)
            if not datos:
                break
            mensaje = datos.decode("utf-8").strip()
            print(f"[{addr[0]}] {mensaje}")
            if mensaje.lower() == "salir":
                conn.sendall("Adiós".encode("utf-8"))
                break
            conn.sendall(f"Servidor recibió: {mensaje}".encode("utf-8"))
    print(f"[-] Desconectado: {addr[0]}:{addr[1]}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PUERTO))
        s.listen()
        print(f"Servidor escuchando en {HOST}:{PUERTO} (Ctrl+C para detener)")
        try:
            while True:
                conn, addr = s.accept()
                threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServidor detenido.")


if __name__ == "__main__":
    main()
