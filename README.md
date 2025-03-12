# IP Parser

- **Extracts IPv4, IPv6, and CIDR blocks** – Detects standalone IPs and network ranges for both IPv4 and IPv6.  
- **Captures link-local IPv6 addresses (`fe80::/10`)** – Ensures addresses like `fe80::1` are properly extracted.  
- **Removes trailing punctuation** – Strips unnecessary periods (`.`) that may interfere with IP detection.  
- **Sorts and deduplicates extracted addresses** – Organizes IPv4 first, followed by IPv6, maintaining correct numerical order.  
- **Provides a modern Tkinter GUI** – Built with `ttkbootstrap` using the "darkly" theme for a sleek interface.  
- **Supports direct text input and parsing** – Users can paste mixed content, and the tool extracts only valid IPs.  
- **Copy extracted IPs to clipboard** – One-click functionality to copy all parsed results for easy use.  
- **Export parsed IPs to an Excel file** – Saves extracted data in `.xlsx` format with a timestamped filename.  
- **Lightweight and standalone** – Requires minimal dependencies and runs locally without an internet connection.  

