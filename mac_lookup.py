from flask import Flask, request, jsonify
import csv
import re
import socket
import sys
import os

app = Flask(__name__)

# Configuration
API_KEY = "XXXXX"  # Replace with your actual API key
MANID_CSV_PATH = "/home/arrel/gits/maclookup/ieee-oui.csv"

def load_mac_vendor_data(csv_file_path):
    """Load MAC vendor data from the CSV file."""
    try:
        data = []
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        return None

def find_mac_vendor(mac, data):
    """Find the vendor for a given MAC address in the loaded CSV data."""
    mac = mac.replace('-', '').replace(':', '').lower()
    if len(mac) != 12:
        return None

    for item in data:
        if 'Assignment' in item:
            # Convert the assignment (hexadecimal) to a zero-padded 6-byte hex string.
            start = f"{int(item['Assignment'], 16):06x}"
            if mac.startswith(start):
                return {
                    "vendor": item.get('Organization Name', 'Unknown'),
                    "company": item.get('Organization Name', 'Unknown'),
                    "start": start,
                    "end": start + "ff" * (6 - len(start) // 2)
                }

    return None

@app.route('/', methods=['GET'])
def api():
    cmd = request.args.get('cmd')
    key = request.args.get('key')
    mac = request.args.get('m')

    if key != API_KEY:
        return jsonify({"response_code": "403", "response_message": "Forbidden"}), 403

    if cmd == 'mac-lookup':
        if not mac:
            return jsonify({"response_code": "400", "response_message": "Bad Request: Missing MAC address"}), 400

        # Validate MAC address format
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
            return jsonify({"response_code": "400", "response_message": "Bad Request: Invalid MAC address format"}), 400

        data = load_mac_vendor_data(MANID_CSV_PATH)
        if data is None:
            return jsonify({"response_code": "500", "response_message": "Internal Server Error: Could not load CSV file"}), 500

        vendor_info = find_mac_vendor(mac, data)

        if vendor_info:
            return jsonify({
                "mac": mac,
                "vendor": vendor_info["vendor"],
                "company": vendor_info["company"],
                "start": vendor_info["start"],
                "end": vendor_info["end"],
                "result": "1",
                "response_code": "200",
                "response_message": "OK"
            }), 200
        else:
            return jsonify({
                "mac": mac,
                "vendor": "Unknown",
                "company": "Unknown",
                "result": "0",
                "response_code": "200",
                "response_message": "OK"
            }), 200
    else:
        return jsonify({"response_code": "404", "response_message": "Not Found: Command not found"}), 404

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == "__main__":
    port = 5000

    if is_port_in_use(port):
        print(f"Port {port} is already in use.  Exiting.")
        sys.exit(1)

    print(f"Starting web API on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)