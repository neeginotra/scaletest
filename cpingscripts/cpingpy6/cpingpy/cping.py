import socket
import time
import os
import sys
import datetime

target_port = 22  # Port number to connect to
timeout = 90  # 18 seconds timeout

def get_local_ip():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return host_ip
    except socket.error as e:
        print("An error occurred:", e)
        return "unknownip"

def get_source_host_name():
    try:
        source_host_name = socket.gethostname()
        return source_host_name
    except socket.error as e:
        print("An error occurred:", e)
        return "unknownhost"

        
def measure_connection_time(target_host, target_port):
    start_time = datetime.datetime.now()
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (target_host, target_port)
        print("Target : ", target_host, ":", target_port)

        # Set connect timeout
        client_socket.settimeout(timeout)

        # Three way handshake start time
        start_time = datetime.datetime.now()

        # Three way handshake
        client_socket.connect(server_address)

        # Three way handshake done time
        end_time = datetime.datetime.now()

        # Get Client Port
        client_port = client_socket.getsockname()[1]

        # close connection (fin/sync)
        client_socket.close()

        # Three way handshake + connnection close time
        end_time_with_connection_close = datetime.datetime.now()

        # Calculate connection time in seconds
        connection_time = (end_time - start_time).total_seconds() * 1000 * 1000

        # Connection time (Three way handshake + connnection close time)
        connection_open_close_time = (end_time - end_time_with_connection_close).total_seconds() * 1000 * 1000

        # If you want to include connection open and close time then you can return connection_open_close_time instead of connection_time
        return client_port, connection_time;
        
    except Exception as e:
        end_time = datetime.datetime.now()
        connection_time = (end_time - start_time).total_seconds() * 1000 * 1000

        print("An error occurred:", e)
        print("Target connection timeout : ", target_host, ":", target_port, "timeout microseconds=", connection_time)
        return -1, -1

def main():
    source_host = get_local_ip()  # Get the local machine's IP address
    source_host_name = get_source_host_name();
    
    input_filename = "input_ips.txt"  # Input file containing target IP addresses
    output_filename = "connection_times.txt"
    
    target_ips = []
    try:
        with open(input_filename, "r") as input_file:
            target_ips = input_file.read().splitlines()
    except Exception as e:
        print("Failed to open input file.")
        sys.exit(1)
    
    try:
        with open(output_filename, "a") as output_file:
            for target_ip in target_ips:
                client_port, connection_time = measure_connection_time(target_ip, target_port)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                
                if connection_time >= 0:
                    output_file.write(f'"{source_host_name}", "{current_time}","{source_host}","{target_ip}","{client_port}", "{target_port}","{connection_time}"\n')
                else:
                    output_file.write(f'"{source_host_name}", "{current_time}","{source_host}","{target_ip}","{client_port}", "{target_port}","-1"\n')
    except Exception as e:
        print("Failed to open output file.")
        sys.exit(1)

if __name__ == "__main__":
    main()

