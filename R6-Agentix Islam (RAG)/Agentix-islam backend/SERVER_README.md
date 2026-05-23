# Agentix Server Infrastructure


## Changelog
- **2026-02-28 03:56:27+03:00**
  - **Command Executed:** Copying binary to Docker container
  - **Logical Change:** Installed Linuxbrew (Homebrew for Linux) on the host Hetzner server and installed `steipete/tap/gogcli`. Because OpenClaw runs in an isolated Docker container, Homebrew on the host wasn't visible to it. I manually copied the newly compiled `gog` binary directly into the OpenClaw container's path (`docker cp ... openclaw:/usr/local/bin/gog`). This successfully satisfied OpenClaw's requirement, elevating eligible skills from 3 to 4.
- **2026-02-27 20:20:00+03:00**
  - **Command Executed:** Docker pull and run
  - **Logical Change:** Installed OpenClaw via Docker (`alpine/openclaw`) and exposed it locally on port `18789`. Did not expose via UFW for security; accessible only via SSH port forwarding as requested by the user.
- **2026-02-25 22:49:15+03:00**
  - **Command Executed:** `./deploy.sh`
  - **Logical Change:** Fixed a `KeyError: 'flash'` in `APIs/AiUtilis.py` inside the `calculate_gemini_cost` function by using the exact model name key `"gemini-2.5-flash"` instead of `"flash"`. This error was crashing the background task, causing Firestore (usage + conversations) to fail to update.

- **2026-02-25 22:42:00+03:00**
  - **Command Executed:** `./deploy.sh`
  - **Logical Change:** Updated `save_conversation` in `TocManager.py` to correctly extract and save only the `answer` string (`ai_answer.answer` field) instead of the entire `ai_answer` JSON object to the `conversation` Firestore collection.

- **2026-02-25 22:23:52+03:00**
  - **Command Executed:** `./deploy.sh`
  - **Logical Change:** Updated the `gemini_model` parameter in `APIs/AgenticIslam.py` from the non-existent `"gemini-3.0-pro-preview"` to `"gemini-2.0-flash"` to fix the 500 Internal Server Error when calling `/book/chat/no_stream`. Unblocked the API request so Gemini inference works now.

- **2026-02-25 22:18:19+03:00**
  - **Command Executed:** `./deploy.sh`
  - **Logical Change:** Pushed the latest local changes to the server (including updates to `APIs/AgenticIslam.py`) and rebuilt the `agentix-islam-app` container.

- **2026-02-25 22:00:00+03:00**
  - **Command Executed:** Edited `./docker-compose.yml` and ran `./deploy.sh`
  - **Logical Change:** Modified the `docker-compose.yml` file to include Traefik labels for `api.agentixislam.com` and connect the `agentix-islam-api` container to the external `coolify` network so reverse proxy requests correctly route to port 80. Fixed the 503 error returned by the endpoint.

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

### A. OpenClaw
- **Purpose**: Your personal AI assistant Gateway & Dashboard.
- **Port**: `18789` (Local only. Do not expose via UFW)
- **Docker Container**: `openclaw`
- **Access Method**:
  Access is restricted to local connections for security. Use SSH port forwarding from your local machine to access the dashboard:
  ```bash
  ssh -L 18789:localhost:18789 agentix@46.225.80.110
  ```
  Then, navigate to `http://localhost:18789` in your local browser.
- **Logs**:
  ```bash
  docker logs -f openclaw
  ```
  How to get Gateway Token from OpenClaw:
  ```bash
  docker exec openclaw cat /home/node/.openclaw/openclaw.json
  ```
  how to open Setup Wizzard
  ```bash
  ssh agentix@46.225.80.110
  docker exec -it openclaw node openclaw.mjs configure

  ```
  how to run command in openclaw
  ```bash
  ssh agentix@46.225.80.110
  docker exec -it openclaw node openclaw.mjs <command>
  ```

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
