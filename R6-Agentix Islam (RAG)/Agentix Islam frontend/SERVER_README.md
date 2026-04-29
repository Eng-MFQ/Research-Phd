# Agentix Server Infrastructure

### 📍 How to Find Documentation

Future agents can access the `SERVER_README.md` through two primary methods:

* **Directly on the Server:**
Navigate to `/opt/agentix/SERVER_README.md`. It is available immediately upon login.
* **Via the Codebase (GitHub):**
Check the **main README.md** in the root directory. There is a direct link and reference to the server documentation there.

---

**Summary:** Whether an agent starts with the source code or logs into the terminal, the instructions are visible and accessible.

Would you like me to draft the actual content for that `SERVER_README.md` file to help get them started?

This document provides a comprehensive guide to the **Agentix Server** configuration, intended for both human developers and AI agents.

## 1. Server Details
- **Provider**: Hetzner VPS
- **IP Address**: `46.225.80.110`
- **OS**: Ubuntu 24.04 LTS
- **Hostname**: `ubuntu-4gb-nbg1-2` (Generic)
- **Primary User**: `agentix`
  - **UID**: 1000
  - **Sudo Access**: Yes (requires password/configuration)
  - **SSH Key**: Required (Password authentication disabled)

## 2. Access & Security
### SSH Access
Root login is **DISABLED**. All access must be via the `agentix` user.
```bash
ssh agentix@46.225.80.110
```

### Firewall (UFW)
The server uses UFW to strictly limit incoming traffic. Only the following ports are open:
- `22/tcp`: SSH
- `80/tcp`: HTTP (Web / Reverse Proxy)
- `443/tcp`: HTTPS (Web / Reverse Proxy)
- `8000/tcp`: Coolify UI
- `8001/tcp`: Agentix API (FastAPI)
- `8002/tcp`: Agentix Islam API (FastAPI)
- `6001-6002/tcp`: Coolify Realtime Service

### Brute Force Protection
**Fail2Ban** is installed and active. It monitors SSH logs and bans IPs that show malicious behavior (repeated failed logins).

## 3. Installed Services

### A. Coolify
- **Purpose**: Self-hosted PaaS to manage WordPress and other web apps.
- **URL**: `http://46.225.80.110:8000`
- **Infrastructure**: Runs as a set of Docker containers (`coolify`, `coolify-proxy`, `coolify-db`, etc.).
- **Proxy**: Uses Traefik on ports 80/443 to route traffic.

### B. Agentix API
- **Purpose**: The main AI backend service.
- **Location**: `/opt/agentix`
- **Port**: `8001` (Internal container port 8000 mapped to host 8001).
- **Docker Container**: `agentix-app-1`
- **Environment**:
  - Uses `.env` file in `/opt/agentix/.env` (contains API keys).
  - Credentials: `whilearn/firebase/service_account_key.json`.
- **Logs**:
  ```bash
  docker logs -f agentix-app-1
  ```
### C. Agentix Islam API
- **Purpose**: API for Agentix Islam (FiqhiNet).
- **URL**: `https://api.agentixislam.com`
- **Location**: `/opt/agentix-islam`
- **Network**: Integrated directly into Coolify's `coolify` Traefik Docker network.
- **Port**: Accessible securely via Traefik on port `443`. Internal container port `80` is proxy-passed. (Port `8002` is locally bound for internal debugging but traffic should flow through Traefik).
- **Docker Container**: `agentix-islam-api`
- **Environment**:
  - Uses `.env` file in `/opt/agentix-islam/.env` (copied from `/opt/agentix/.env`).
  - Credentials: `whilearn/firebase/service_account_key.json`.
- **Logs**:
  ```bash
  docker logs -f agentix-islam-api
  ```

## 4. Deployment Workflow

### Required One-Time Setup (Important)
For the deployment script to work without `sudo` passwords, the `agentix` user must own the project directory and be able to run Docker.
**Run this once on the server:**
```bash
# 1. Add agentix to docker group
sudo usermod -aG docker agentix

# 2. Change ownership of project directory
sudo chown -R agentix:agentix /opt/agentix

# 3. Log out and log back in for group changes to take effect
exit
```

### Automation Script (`deploy.sh`)
The project includes a `deploy.sh` script for automated updates:
1.  **Sync**: Uses `rsync` to push local files to `/opt/agentix`.
2.  **Rebuild**: SSHs into the server to run `docker compose up -d --build`.

**Usage:**
```bash
./deploy.sh
```

## 5. Maintenance Commands
Common tasks for managing the server:

**Restart Agentix API:**
```bash
ssh agentix@46.225.80.110 "cd /opt/agentix && docker compose restart"
```

**Restart Agentix Islam API:**
```bash
ssh agentix@46.225.80.110 "cd /opt/agentix-islam && docker compose restart"
```

**Check System Status:**
```bash
ssh agentix@46.225.80.110 "htop"  # CPU/RAM usage
ssh agentix@46.225.80.110 "df -h" # Disk usage
```

**Update System:**
```bash
ssh agentix@46.225.80.110 "sudo apt update && sudo apt upgrade -y"
```
