# MAC Vendor Lookup API

This API will find a MAC address vendor for the MAC address provided by searching for a matching mac vendor in the file at /home/arrel/gits/maclookup/ieee-oui.csv (Downloaded from https://standards-oui.ieee.org/oui/oui.csv)

See also:

- https://standards-oui.ieee.org/oui28/mam.csv
- https://standards-oui.ieee.org/oui36/oui36.csv

## API Usage

### Example Request:

Browser: http://localhost:5000/?cmd=mac-lookup&key=XXXXX&m=F8-B1-56-B8-5F-55

Powershell: Invoke-RestMethod -Uri "http://192.168.0.100:5000/?cmd=mac-lookup&key=XXXXX&m=D8:3B:DA:31:A0:E0" -Method GET

Bash: curl -X GET "http://localhost:5000/?cmd=mac-lookup&key=XXXXX&m=D8:3B:DA:31:A0:E0"

### Example Response:

{
"company": "Dell Inc.",
"end": "f8b156ffffff",
"mac": "F8-B1-56-B8-5F-55",
"response_code": "200",
"response_message": "OK",
"result": "1",
"start": "f8b156",
"vendor": "Dell Inc."
}

## API Endpoint:

https://api.localhost/?cmd=mac-lookup&m=AA-BB-CC-DD-EE-FF

## Request parameters:

| Name        | Required | Description                                   | Default |
| ----------- | -------- | --------------------------------------------- | ------- |
| mac address | yes      | A MAC address (either separated by : or dash) |         |

## Output format

- json

## Response Parameters:

Name Description

- mac The MAC address provided for lookup
- vendor Vendor of the MAC address
- company A full company name of the MAC address
- result The indication of whether the vendor for the - MAC address was found (1=Yes, 0=No).
- response_code Response status code to indicate success or failed completion of the API call.
- response_message Response message to indicate success or failed completion of the API call.

## Response Codes & Messages:

| Name | Message     | Description                         |
| ---- | ----------- | ----------------------------------- |
| 200  | OK          | Successfully processed the request. |
| 400  | Bad Request | Failed to complete the request.     |
| 404  | Not Found   | Command not found.                  |
