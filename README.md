# ARK Server Manager CLI Tool

This Python CLI tool helps you manage ARK servers.

## Features

- **Pull configurations** from remote servers
- **Create YAML configurations** from INI files
- **Create INI configurations** from YAML files
- **Push configurations** to remote servers

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/paqx/arkman.git
   cd arkman
   ```

2. **Create a Python virtual environment:**

   - **Linux/MacOS:**
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows:**
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Make the `arkman.py` file executable (Linux/MacOS only):**

   ```bash
   chmod +x arkman.py
   ```
   *Note: Windows users can skip this step and run the script directly with Python.*

5. **Create a `.env` file** to store connection details:

   ```dotenv
   ABERRATION_HOST=<your_aberration_host>
   ABERRATION_USER=<your_aberration_user>
   ABERRATION_PASS=<your_aberration_password>
   CRYSTAL_ISLES_HOST=<your_crystal_isles_host>
   CRYSTAL_ISLES_USER=<your_crystal_isles_user>
   CRYSTAL_ISLES_PASS=<your_crystal_isles_password>
   # Add entries for Extinction, Fjordur, Gen_1, Gen_2, Island, and Ragnarok
   ```

## Usage

### Running the Script

- **Linux/MacOS (executable method):**
   ```bash
   ./arkman.py <command> [options]
   ```
- **All platforms (Python interpreter method):**
   ```bash
   python arkman.py <command> [options]
   ```

### Commands

1. **Pull Configurations**

   Download configuration files from remote servers to the local `configs/ini` directory.

   ```bash
   # Pull from all servers
   python arkman.py pull

   # Pull from specific servers (space-separated list)
   python arkman.py pull -s Aberration Crystal_Isles
   # or
   python arkman.py pull --servers Aberration Crystal_Isles
   ```

2. **Create YAML Configurations**

   Generate YAML configuration files from INI configuration files.

   ```bash
   python arkman.py load
   ```

3. **Create INI Configurations**

   Generate INI configuration files from YAML configuration files.

   ```bash
   python arkman.py dump
   ```

4. **Push Configurations**

   Upload configuration files from the local `configs/ini` directory to the remote servers.

   ```bash
   # Push to all servers
   python arkman.py push

   # Push to specific servers (space-separated list)
   python arkman.py push -s Fjordur Gen_1
   # or
   python arkman.py push --servers Fjordur Gen_1
   ```

### Notes

- The `-s`/`--servers` parameter accepts one or more server names (case-sensitive).
- By default, an action is performed on all servers.

## Workflow

The goal is to use a GitOps approach for managing ARK server configurations. The configurations should be version-controlled and easily deployed.

### 1. Initial Setup (First-Time Use)

- **Import Existing Configurations**  
  Import your current server configuration files:

  ```bash
  python arkman.py pull
  python arkman.py load
  ```

  This will create:
  - INI files in `configs/ini/`
  - YAML files in `configs/yml/`

- **Sanitize and Modularize**  
  After the YAML files are generated:
  - Move sensitive or server-specific information (like passwords, admin keys, RCON ports) to the `.env` file.  
  - Move repetitive sections into includes. Use the `!include` YAML tag to reference files in `configs/yml/includes/`.

### 2. Daily Workflow

- **Edit & Version Changes**  
  Make any configuration changes by editing the YAML files. Use environment variables and YAML includes:
  ```yaml
  Message: ${MOTD}
  OverridePlayerLevelEngramPoints: !include OverridePlayerLevelEngramPoints.yml
  ```

- **Apply Configurations**  
  After making the changes, commit them to your version control repository. Then generate and deploy the updated configs:
  ```bash
  git add .
  git commit -m "fix: correct MaxPlayers setting"
  git push  # Push changes to your repo

  python arkman.py dump  # Convert YAML to INI, expanding env vars/includes
  python arkman.py push  # Upload configs to your servers
  ```
