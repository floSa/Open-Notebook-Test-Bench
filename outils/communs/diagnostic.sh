#!/usr/bin/env bash
# Diagnostic de la machine : écrit outils/resultats/machine/diagnostic-<date>.json
set -u
cd "$(dirname "$0")/../.."
sortie="outils/resultats/machine/diagnostic-$(date +%F).json"
mkdir -p "$(dirname "$sortie")"

essai() { timeout "${2:-20}" bash -c "$1" 2>&1 | head -c 4000; }

wsl_version=$(essai 'wsl.exe --version 2>/dev/null | tr -d "\000\r"')
windows=$(essai 'cmd.exe /c ver 2>/dev/null | tr -d "\r"')
distrib=$(essai '. /etc/os-release; echo "$PRETTY_NAME"')
noyau=$(uname -r)
cpu=$(grep -m1 "model name" /proc/cpuinfo | cut -d: -f2- | sed 's/^ //')
coeurs=$(nproc)
ram_mo=$(free -m | awk '/Mem:/{print $2}')
swap_mo=$(free -m | awk '/Swap:/{print $2}')
disque_depot=$(df -BG --output=avail . | tail -1 | tr -d ' G')
docker_root=$(docker info --format '{{.DockerRootDir}}' 2>/dev/null)
docker_df=$(essai 'docker system df --format "{{.Type}}={{.Size}}" | paste -sd";"')
nvsmi=$(essai 'nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader')
gpu_conteneur=$(essai 'docker run --rm --gpus all --entrypoint true ollama/ollama@sha256:46399ef084d97b381955b5dc585c5d836dbe7ed3f79f170d1c04660fed511e3a && echo OK' 120)
gpu_windows=$(essai 'powershell.exe -NoProfile -Command "Get-CimInstance Win32_VideoController | ForEach-Object { \$_.Name }" | tr -d "\r" | paste -sd";"' 60)
docker_v=$(docker version --format '{{.Server.Version}}' 2>/dev/null)
compose_v=$(docker compose version --short 2>/dev/null)

code() { curl -s -o /dev/null -m 15 -w '%{http_code}' "$1"; }
hub=$(code https://registry-1.docker.io/v2/)
ghcr=$(code https://ghcr.io/v2/)
pypi=$(code https://pypi.org/simple/pip/)
ollamacom=$(code https://ollama.com/)
hf=$(code https://huggingface.co/api/models/BAAI/bge-m3)

# Port publié sur 127.0.0.1 joignable depuis WSL
docker rm -f rag-diag-port >/dev/null 2>&1
docker run -d --name rag-diag-port -p 127.0.0.1:18999:80 nginx:alpine >/dev/null 2>&1
sleep 3
port_local=$(code http://127.0.0.1:18999/)
docker rm -f rag-diag-port >/dev/null 2>&1

python3 - "$sortie" <<EOF
import json, sys
d = {
  "date": "$(date -Iseconds)",
  "windows": """$windows""".strip(),
  "wsl_version": """$wsl_version""".strip(),
  "distribution": "$distrib", "noyau": "$noyau",
  "cpu": "$cpu", "coeurs_logiques": $coeurs,
  "ram_wsl_mo": $ram_mo, "swap_wsl_mo": $swap_mo,
  "disque_libre_depot_go": $disque_depot,
  "docker_root": "$docker_root", "docker_df": "$docker_df",
  "nvidia_smi_wsl": """$nvsmi""".strip(),
  "gpu_dans_conteneur": """$gpu_conteneur""".strip(),
  "cartes_video_windows": """$gpu_windows""".strip(),
  "docker": "$docker_v", "compose": "$compose_v",
  "acces_http": {"docker_hub": "$hub", "ghcr": "$ghcr", "pypi": "$pypi", "ollama_com": "$ollamacom", "huggingface": "$hf"},
  "port_127_0_0_1_depuis_wsl": "$port_local",
}
json.dump(d, open(sys.argv[1], "w"), ensure_ascii=False, indent=2)
print(json.dumps(d, ensure_ascii=False, indent=2))
EOF
