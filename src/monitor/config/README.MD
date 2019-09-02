# Config

## config.json
### Common
 - debug: Enable / Disable debug info shown in the console.
 - saveraw: Enable/disable raw saving of received FLEX alerts.
 - saverawdatefiles: Split received alerts in files order by date.
 - rawpath: Path to save the file to when "Saveraw" is enabled.
 - saverawunique: Save only unique alerts to a file.
 - uniquedatefiles: Split received alerts in files order by date.
 - uniquepath: Path to save the file to when "Saverawunique" is enabled.
 - onerror: // TODO

### Radio
 - command: Command executed to open the radio.
 - triggertime: Time in seconds after which we assume a FLEX group has ended.

### Api
 - endpoint: Custom endpoint where the received messages are sent to.
 - key: Api Key

### LocationIQ
 - key: API key for LocationIQ to resolve locations.

### MySQL
 - enabled: Enable / disable database access
 - host: DB Host.
 - username: DB Username.
 - password: DB Password.
 - database: Database to connect to.

### Serial
 - port: Serial port for strobe light control.
 - baudrate: Baudrate for serial.

## Triggers
### capcodes.txt
In this file you can place a list of capcodes seperated by a newline on which the monitor triggers an alert.\
Capcodes have to have a 7 digit format by adding leading zero's. This means the capcode "123456" has to be put in the file as "0123456".

### words.txt
In this file you can place a list of words seperated by a newline on which the monitor triggers an alert.\