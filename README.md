Advanced Python Port Scanner

Overview
The Advanced Python Port Scanner is a multithreaded, customizable tool that allows users to scan specific IP addresses or a range of IPs for open, closed, and filtered ports. The tool supports scanning over both TCP and UDP protocols and includes advanced features like banner grabbing and stealth mode for slow, cautious scans to avoid detection by firewalls.
The scanner is designed to be efficient by using multithreading for faster scanning, and provides detailed information about the services running on open ports. It also includes options for error handling, timeout management, and saving scan results to a file.

Features
IP Scanning: Scan a specific IP address or a range of IP addresses.
Port Range: Scan a range of ports (from 1 to 65535) for open, closed, or filtered status.
Protocol Support: Scans ports using both TCP and UDP protocols.
Multithreading: Perform faster scans using multiple threads.
Banner Grabbing: Retrieve service banners from open ports (e.g., HTTP, FTP).
Stealth Mode: Slow down scans and limit packets to avoid detection by firewalls.
Custom Timeouts: Set timeout periods to avoid hanging on unresponsive ports.
Error Handling: Graceful handling of socket timeouts, connection refusals, and unreachable hosts.
Service Detection: Identifies services running on open ports using socket.getservbyport().
Result Saving: Option to save scan results to a text file.

Installation
Clone the repository:
git clone https://github.com/your-username/advanced-python-port-scanner.git
cd advanced-python-port-scanner

Install required dependencies (if any):
The scanner uses Python's built-in libraries such as socket, threading, argparse, and time. No external libraries are required for basic functionality.



If you need to ensure Python is installed, you can use:
sudo apt-get install python3  # For Linux
brew install python3  # For Mac
python -v #For Windows

Run the script:
python advanced_port_scanner.py -ip <target_ip> -sp 1 -ep 1000 -proto tcp -t 100 -o results.txt

Usage:
The scanner supports several options to customize the scan:
python advanced_port_scanner.py -ip <target_ip> [options]
Command-line Options:
-ip <target_ip>: (Required) Specify the target IP address to scan.
-sp, --start-port: Set the starting port for the scan (default is 1).
-ep, --end-port: Set the ending port for the scan (default is 65535).
-proto, --protocol: Choose the protocol to use for scanning (tcp or udp), default is tcp.
-t, --threads: Number of threads to use for the scan (default is 100).
-to, --timeout: Set the socket timeout for each connection (default is 1 second).
-o, --output: Save the scan results to a specified file (optional).
-s, --stealth: Enable stealth mode for slow scanning to avoid detection.

Example Usage:
Basic TCP Scan:
python advanced_port_scanner.py -ip 192.168.1.1 -sp 1 -ep 1024 -proto tcp -t 50
Save Results to File:
python advanced_port_scanner.py -ip 192.168.1.1 -sp 1 -ep 1024 -proto tcp -t 50 -o results.txt
Enable Stealth Mode:
python advanced_port_scanner.py -ip 192.168.1.1 -sp 1 -ep 1024 -proto tcp -t 1 -s




How It Works
The scanner uses the Python socket module to establish connections to the specified IP and port range. It determines if the port is open, closed, or filtered by attempting to create a connection and analyzing the response. Multithreading is implemented using Python s threading module to enhance performance, allowing multiple ports to be scanned simultaneously.
For open ports, the tool attempts to identify the service running on the port using socket.getservbyport() and, if applicable, retrieves banners via simple HTTP/FTP requests.

Error Handling:
The scanner is designed to handle the following errors gracefully:
Timeouts: Handles socket timeouts and unresponsive ports.
Connection Refusals: Marks ports as closed if a connection is refused.
Unreachable Hosts: Catches and logs errors when the target host is unreachable.

Contributions:
Feel free to fork this repository and submit pull requests if you want to contribute new features or improvements. Open issues for any bugs or requests you encounter.

Author
Kunika H Patil

Acknowledgments
Special thanks to the Python community for their excellent documentation and libraries.

Future Enhancements:
Add support for scanning over a range of IPs.
Implement more sophisticated vulnerability detection features.
Add logging for stealth mode scans.
