# SDN-Based Access Control System

## Problem Statement

This project implements an SDN-based Access Control System using the POX controller and Mininet.

The controller dynamically installs OpenFlow rules to:
- Allow communication between authorized hosts
- Block unauthorized communication

---

## Objective

- Demonstrate SDN controller-switch interaction
- Handle PacketIn events
- Implement OpenFlow match-action rules
- Enforce whitelist-based network access control

---

## Technologies Used

- Python
- Mininet
- POX Controller
- OpenFlow Protocol

---

## Network Topology

### Devices
- 1 OpenFlow Switch (s1)
- 4 Hosts:
  - h1 → 10.0.0.1
  - h2 → 10.0.0.2
  - h3 → 10.0.0.3
  - h4 → 10.0.0.4

### Topology Type
Star Topology

---

## Allowed Communication

- h1 ↔ h2
- h2 ↔ h3

---

## Blocked Communication

- h4 → h1
- h4 → h2
- h1 → h4

---

## Project Structure

``` id="u3nldu"
SDN-Access-Control/
│
├── controller/
│   └── access_control.py
│
├── topology/
│   └── topo.py
│
├── screenshots/
│
└── README.md
```

---

## Setup and Execution Steps

### 1. Start POX Controller

```bash id="fekb7z"
cd ~/pox
python3 pox.py myapps.access_control
```

---

### 2. Start Mininet

```bash id="q1sp4o"
cd ~/sdn-project
sudo mn --custom topo.py --topo mytopo --controller=remote,ip=127.0.0.1
```

---

## Testing

### Allowed Communication

```bash id="dvc00o"
h1 ping h2
```

Expected Result:
- Ping successful

---

### Blocked Communication

```bash id="9d9rjy"
h4 ping h1
```

Expected Result:
- Destination Host Unreachable

---

## Expected Output

### Controller Logs

``` id="8f9s4o"
ALLOWED: 10.0.0.1 -> 10.0.0.2
BLOCKED: 10.0.0.4 -> 10.0.0.1
```

---

# Proof of Execution

## Allowed Ping

![Allowed Ping](screenshots/allowed_ping.png)

---

## Blocked Ping

![Blocked Ping](screenshots/blocked_ping.png)

---

## Flow Table

![Flow Table](screenshots/flow_table.png)

---

## Controller Logs

![Controller Logs](screenshots/controller_logs.png)

---

## Conclusion

This project demonstrates centralized SDN-based access control using OpenFlow flow rules installed dynamically through the POX controller.
