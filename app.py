from flask import Flask, request, jsonify
import yaml
import re

app = Flask(__name__)

# Configuration
API_KEY = "XXXXX"  # Replace with your actual API key
YAML_FILE_PATH = "/home/arrel/gits/zephyr-projects/ESP32C3_ble_serial_bridge/assigned_numbers/company_identifiers/company_identifiers.yaml"

def load_mac_vendor_data(yaml_file_path):
    """Load MAC vendor data from the YAML file."""
    try:
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        return None

def find_mac_vendor(mac, data):
    """Find the vendor for a given MAC address in the loaded data."""
    mac = mac.replace('-', '').replace(':', '').lower()
    if len(mac) != 12:
        return None

    for item in data:
        if 'value' in item:
            # Convert the hex value to a zero-padded 6-byte string (12 hex digits).
            start = f"{int(str(item['value']), 16):06x}"
            if mac.startswith(start):
                return {
                    "vendor": item.get('name', 'Unknown'),
                    "company": item.get('name', 'Unknown'),
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

        data = load_mac_vendor_data(YAML_FILE_PATH)
        if data is None:
            return jsonify({"response_code": "500", "response_message": "Internal Server Error: Could not load YAML file"}), 500

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')