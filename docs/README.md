# Cloud Monitoring Tool

## Project overview

This project aims at monitoring runtime health of virtual machines deployed on
any cloud platform such as openstack, opennebula, etc. It is loosely based on
the CloudMonatt architecture for openstack infrastructure. The term _loosely_
is used because it does not provide a customized API for services provided by
openstack, i.e., it is not strictly bound to the openstack infrastructure. The
following figure shows the high level design of the CloudMonatt architecture
(source: Monitoring and attestation of virtual machine security health,
_Tianwei Zhang_, _Ruby B. Lee_)

<img alt="CloudMonatt architecture" src="./images/cloud-monatt.png" width="800">

---

## Application design

This application is uses a client-server model to monitor the virtual machines.
It contains two major components:

- **Attestation agent**: A multi-threaded application that runs on each virtual machine.
  It collects relevant system attributes and sends them to the attestation server.
- **Attestation server**: A web server which receives runtime system information sent
  by the attestation agent, saves them in a database and provides access to them via a
  web API.

```
 ________________________
|                        |
|  Cloud infrastructure  |
|  ____________________  |  HTTP traffic   ______________________          _________________
| |                    |-|----------------|                      |        |                 |
| |  Virtual Machine   | |                |  Attestation server  |--------|  Web interface  |
| |____________________|-|----------------|______________________|        |_________________|
|                        | Socket traffic
|________________________|
```

---

## Setup instructions

### Attestation server

Requires:

- `node v18.16.0 (LTS)`
- See `package.json` for all dependencies.

Setup process:

- Clone the `attestation-server` directory on a machine that will act as
  the attestation server.
- Install required dependencies:
  `$ npm install`
- Start server: `$ node app.js`

### Attestation agent

Requires:

- `python v3.9+`
- `python-socketio v5.8.0`
- `requests v2.29.0`

Setup process:

- Install and enable auditd for system auditing (requires `sudo` privileges):  
  `$ apt install auditd audispd-plugins`  
  `$ systemctl enable auditd`
- Clone the `attestation_agent` directory on a virtual machine.
- Install required packages:
  `$ pip install -r attestation_agent/requirements.txt`
- Configure parameters in `attestation_agent/config.py`:
  - `ATTESTATION_HOST`: IPv4 address of the attestation server.
  - `ATTESTATION_PORT`: Port on which attestation server API is available.
- Other parameters can also be changed based on system configuration.
- Run the agent: `$ python -m attestation_agent`

### Dashboard

Requires:

- `node v18.16.0 (LTS)`
- See `package.json` for all dependencies.

Setup process:

- Clone the `frontend` directory on some machine (can be same as the attestation server).
- Install required dependencies:
  `$ npm install`
  - If this does not work due to mismatched versions, use: `$ npm install --legacy-peer-deps`
- Start server: `$ npm start`
