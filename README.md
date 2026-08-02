# Shelly IoT Simulation Pipeline | Docker Compose Homelab Project
![Grafana Dashboard Preview]
> Adapted for mainland China home network constraints | No physical Shelly hardware required

## 🎯 Project Overview
This project builds a complete containerized IoT metrics collection & observability pipeline.
Since physical Shelly smart devices are unavailable, a custom Python sensor simulator continuously generates synthetic sensor data (temperature, power consumption).
All services run on Proxmox VE virtualization platform.

### Key Environment Challenges Solved
1. ❌ No physical IoT hardware → Custom Python data simulator
2. ❌ China Mobile DHCP broadband with CGNAT, no static public IP
3. ❌ Restricted outbound network → Clash Verge LAN proxy integration
4. ❌ Cannot perform port forwarding on ZTE home router → Cloudflare Tunnel remote access solution

## 🧱 Architecture Flow
`Python Sensor Simulator → Mosquitto MQTT Broker → PostgreSQL Database → Grafana Visual Dashboard`

## 🛠 Tech Stack
- Docker & Docker Compose (Container orchestration)
- Eclipse Mosquitto (MQTT Message Broker)
- PostgreSQL (Time series metric storage)
- Grafana (Observability & visualization)
- Python (IoT sensor data simulation)
- Proxmox VE (Virtualization Host)
- Cloudflare Tunnel (Zero-trust remote access)


