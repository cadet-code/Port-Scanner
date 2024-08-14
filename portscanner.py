import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging to write to a file
logging.basicConfig(filename='port_scan_results.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "No banner available"
            print(f"Port {port}: OPEN - Banner: {banner}")
            logging.info(f"Port {port}: OPEN - Banner: {banner}")
        sock.close()
    except Exception as e:
        logging.error(f"Error scanning port {port}: {e}")

def main(target_ip, start_port, end_port, timeout, max_threads):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, target_ip, port, timeout): port for port in range(start_port, end_port + 1)}
        for future in as_completed(futures):
            port = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error scanning port {port}: {e}")
                logging.error(f"Error scanning port {port}: {e}")

if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    timeout = float(input("Enter timeout (seconds): "))
    max_threads = int(input("Enter number of threads: "))
    
    print(f"Scanning {target_ip} from port {start_port} to {end_port} with a timeout of {timeout} seconds using {max_threads} threads...")
    main(target_ip, start_port, end_port, timeout, max_threads)
    print("Scan complete. Results logged to port_scan_results.log.")
