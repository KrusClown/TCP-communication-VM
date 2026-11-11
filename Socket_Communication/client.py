#!/usr/bin/env python3
"""
Cliente TCP (ejecutar en la VM 2).
Uso: python3 cliente.py <IP_de_la_VM1> [puerto]
"""
import socket
import sys

if len(sys.argv) < 2:
    print("Uso: python3 cliente.py <IP_servidor> [puerto]")
    sys.exit(1)

SERVIDOR = sys.argv[1]
PUERTO = int(sys.argv[2]) if len(sys.argv) > 2 else 5000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        try:
            s.connect((SERVIDOR, PUERTO))
        except (ConnectionRefusedError, socket.timeout, OSError) as e:
            print(f"No se pudo conectar a {SERVIDOR}:{PUERTO} -> {e}")
            sys.exit(1)
        s.settimeout(None)
        print(f"Conectado a {SERVIDOR}:{PUERTO}. Escribe mensajes ('salir' para terminar).")

        while True:
            mensaje = input("> ")
            if not mensaje:
                continue
            s.sendall(mensaje.encode("utf-8"))
            respuesta = s.recv(1024)
            if not respuesta:
                print("El servidor cerró la conexión.")
                break
            print(respuesta.decode("utf-8"))
            if mensaje.lower() == "salir":
                break


if __name__ == "__main__":
    main()
