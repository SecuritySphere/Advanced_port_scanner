import socket  # Imports the socket module to enable network communication and connections.
import threading  # Imports the threading module to handle multithreading for faster scanning.
import argparse  # Imports the argparse module to parse command-line arguments.
import time  # Imports the time module to measure the time taken for the scan.
from queue import Queue  # Imports Queue, a thread-safe queue for storing ports to be scanned.
import os  # Imports os module for saving results to a file (if required).

# Queue for multithreading
port_queue = Queue()  # Creates a queue that will store the port numbers to be scanned.
open_ports = []  # A list to store information about open ports.
lock = threading.Lock()  # A lock object to prevent race conditions when multiple threads modify shared data.

# Function to scan a specific port
def scan_port(ip, port, protocol, timeout=1):  
    """
    Scans a single port to check if it's open, closed, or filtered.
    Uses the provided IP, port, and protocol (TCP/UDP).
    """
    try:
        # Set the socket type based on the protocol (TCP/UDP)
        if protocol == 'tcp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket.
        elif protocol == 'udp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket.

        sock.settimeout(timeout)  # Set a timeout for the socket connection.
        result = sock.connect_ex((ip, port))  # Try to connect to the given IP and port. Returns 0 if successful.
        
        if result == 0:  # If the port is open (result is 0), proceed.
            try:
                service = socket.getservbyport(port, protocol)  # Attempt to get the service name for the port.
            except:
                service = 'Unknown service'  # If the service name can't be determined, mark it as unknown.

            # Lock to ensure safe access to the shared list of open ports.
            with lock:
                open_ports.append((port, 'open', service))  # Add the open port, its status, and service to the list.

            if protocol == 'tcp':  # Perform banner grabbing only for TCP.
                banner_grabbing(sock, ip, port)  # Call the banner grabbing function to retrieve service info.
        else:
            # If the port isn't open, mark it as closed.
            with lock:
                open_ports.append((port, 'closed', ''))  # Add the closed port info.
        sock.close()  # Close the socket after the scan.

    except Exception as e:  # Handle exceptions (like timeouts, unreachable ports, etc.)
        with lock:
            open_ports.append((port, 'filtered', ''))  # If an error occurs, mark the port as filtered.

# Function for banner grabbing on open ports
def banner_grabbing(sock, ip, port):
    """
    Retrieves banner information from open ports.
    This is usually used for services like HTTP, FTP, etc., to extract server headers or protocol info.
    """
    try:
        # Send a basic HTTP request to attempt to retrieve a banner.
        sock.send(b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % ip.encode())  # Send an HTTP request to the open port.
        banner = sock.recv(1024).decode()  # Receive the banner response from the service.
        with lock:
            print(f"[+] Banner from {ip}:{port}: {banner}")  # Print the banner if received.
    except:  # If no banner is retrieved or an error occurs, do nothing.
        pass

# Worker for thread processing
def worker(ip, protocol, timeout):
    """
    Worker function for threading. Each thread will fetch a port from the queue and scan it.
    """
    while not port_queue.empty():  # Continue scanning while there are ports left in the queue.
        port = port_queue.get()  # Get a port from the queue.
        scan_port(ip, port, protocol, timeout)  # Scan the port.
        port_queue.task_done()  # Mark the port scan as done.

# Port scanning function with multithreading
def scan_ports(ip, start_port, end_port, protocol, threads, timeout):
    """
    Sets up the port scanning job with multithreading. It fills the queue with ports and starts threads.
    """
    # Put each port in the specified range into the queue for processing.
    for port in range(start_port, end_port + 1):
        port_queue.put(port)  # Add port to the queue.
    
    # Create a list of threads to handle the scan.
    thread_list = []
    for _ in range(threads):  # Start a given number of threads.
        thread = threading.Thread(target=worker, args=(ip, protocol, timeout))  # Create a thread to scan.
        thread_list.append(thread)  # Add the thread to the list.
        thread.start()  # Start the thread (begin scanning).

    for thread in thread_list:  # Wait for all threads to finish before continuing.
        thread.join()  # Ensure the current thread waits for the others to complete.

# Optionally save results to file
def save_results_to_file(ip, output_file):
    """
    Saves the scanned results to a specified output file.
    """
    with open(output_file, 'w') as file:  # Open the file for writing.
        for port, status, service in open_ports:  # Iterate over open port details.
            file.write(f"{ip}:{port} - {status} - {service}\n")  # Write each port's details to the file.
    print(f"[+] Results saved to {output_file}")  # Print confirmation that the file was saved.

# Command line argument parsing
def main():
    """
    The main function that handles argument parsing and coordinates the scanning process.
    """
    # Argument parser to read command-line arguments.
    parser = argparse.ArgumentParser(description="Advanced Python Port Scanner")
    # Add command-line arguments for various parameters (IP, port range, protocol, etc.)
    parser.add_argument("-ip", type=str, help="Target IP address", required=True)  # IP to scan.
    parser.add_argument("-sp", "--start-port", type=int, help="Start port range", default=1)  # Start port.
    parser.add_argument("-ep", "--end-port", type=int, help="End port range", default=65535)  # End port.
    parser.add_argument("-proto", "--protocol", type=str, help="Protocol (tcp/udp)", default="tcp")  # TCP or UDP.
    parser.add_argument("-t", "--threads", type=int, help="Number of threads (default: 100)", default=100)  # Threads.
    parser.add_argument("-to", "--timeout", type=int, help="Socket timeout in seconds (default: 1)", default=1)  # Timeout.
    parser.add_argument("-o", "--output", type=str, help="Output file for saving results", default=None)  # Output file.
    parser.add_argument("-s", "--stealth", action="store_true", help="Enable stealth mode (slow scanning)")  # Stealth mode.

    args = parser.parse_args()  # Parse the command-line arguments.

    # Extract values from the arguments.
    ip = args.ip
    start_port = args.start_port
    end_port = args.end_port
    protocol = args.protocol
    threads = args.threads
    timeout = args.timeout
    output_file = args.output
    stealth = args.stealth

    # Stealth mode settings: slower, cautious scanning.
    if stealth:
        print("[*] Stealth mode enabled. Scanning will be slow to avoid detection.")
        threads = 1  # Set threads to 1 for stealth mode (slow scanning).
        timeout = 5  # Increase the timeout to make it less detectable.
    
    print(f"[*] Scanning IP: {ip} | Ports: {start_port}-{end_port} | Protocol: {protocol}")
    
    start_time = time.time()  # Record the start time of the scan.
    scan_ports(ip, start_port, end_port, protocol, threads, timeout)  # Call the scanning function.
    end_time = time.time()  # Record the end time of the scan.
    
    # Print the summary of open, closed, and filtered ports.
    for port, status, service in open_ports:
        print(f"Port {port}: {status} - {service}")
    
    if output_file:
        save_results_to_file(ip, output_file)  # Save results to the specified file if needed.

    print(f"[*] Scan completed in {end_time - start_time:.2f} seconds")  # Display the scan duration.

# Entry point of the script
if __name__ == "__main__":
    main()  # Call the main function when the script is executed.
