# 📚 Documentação e Guias

Para garantir uma configuração sem problemas, siga estes guias passo a passo:

---

## 🌡️ [01. Configuração dos Sensores de Hardware](01-install-sensors.md)
Como instalar e configurar **lm-sensors** no seu nó Proxmox para ativar a monitorização de temperaturas e ventoinhas.

---

## 🔑 [02. Configuração do Proxmox](02-proxmox-config.md)
Como criar um **usuário** e um **Token API** seguro no Proxmox (PVE & PBS) com as permissões mínimas necessárias.

---

## ⚙️ [03. Início de Sessão na Integração (PVE & PBS)](03-login-pve-pbs.md)
Guia do processo de configuração inicial no Home Assistant e conexão com os seus servidores.

---

## ❓ [04. Perguntas Frequentes e Solução de Problemas](04-faq.md)
Perguntas comuns, problemas conhecidos e como resolvê-los.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

**A integração mais completa, eficiente e organizada para monitorizar Proxmox VE e PBS a partir do Home Assistant.**

Esta integração foi projetada para utilizadores avançados que precisam de controlo total sobre o hardware sem sobrecarregar o servidor.  
Ao contrário de outras soluções, Proxmox Sensors Extended foca-se na eficiência energética, autenticação segura via Tokens e uma organização visual impecável.

---

## 🔥 Funcionalidades Principais

### 🌡️ Monitorização Avançada de Hardware

**Não se contente apenas com o uso de CPU. Veja o que realmente acontece “debaixo do capô”:**

* **Temperaturas em tempo real:** Núcleos da CPU, VRM e unidades NVMe/SSD/HDD.  
* **Sensores mecânicos:** Velocidade das ventoinhas (RPM) e voltagens da motherboard.  
* **Sensores inteligentes:** Apenas são criadas entidades que reportam dados válidos, mantendo o sistema limpo.

**(Nota: Requer instalar lm-sensors no host Proxmox).**

---

### 🧠 Otimizado para Desempenho

**Projetado para hardware com recursos limitados:**

* **DataUpdateCoordinator:** Minimiza chamadas à API do Proxmox para evitar sobrecarga do servidor.  
* **Silent SSL:** Verificação automática de certificados SSL (incluindo autofirmados) sem encher os logs de erros.

---

### 🗄️ Proxmox Backup Server (PBS) Avançado

* **Modo Externo:** Conecte-se facilmente a servidores PBS remotos usando apenas o domínio.  
* **Monitorização de Tarefas:** Estado detalhado do último Backup, Garbage Collector ou tarefa de Verify.

---

### 🎨 Interface Dinâmica e Organizada

* **Smart Dashboard:** Os sensores são agrupados automaticamente em dispositivos:  
  1. Nó  
  2. Discos físicos  
  3. Máquinas virtuais  
  4. Containers  
  5. Storages  
* **Auto-Naming:** Prefixos automáticos (ex.: `pv1-cpu-temp`) para manter dashboards organizados logicicamente.

---

**Exemplo de Dashboard**

<p align="center">
  <img src="/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

---

## Sensores em Destaque

## PVE

### 🖥️ Sensores de Hardware (PVE & PBS)

Temperaturas da CPU • Temperaturas VRM • Temperaturas NVMe/SSD/HDD  
Velocidade das ventoinhas (RPM) • Voltagens • Sensores de energia • Entidades `pvesensors`  
• Temperatura do chipset

---

### 🧠 Estado do Nó

Uso de CPU (%) • Uso de RAM (%) • RAM usada/total  
Tempo ativo (uptime) • Load average • CPU I/O Wait

---

### 💾 Discos

Capacidade total • Espaço usado (GB e %)  
Nível de desgaste (NVMe) • Estado SMART (se disponível)

---

### 🖥️ Máquinas Virtuais (QEMU)

Uso de CPU (%) • Uso de RAM (%) • Network Tx/Rx  
Estado (ligada/desligada) • Seleção automática/manual

---

### 📦 Containers (LXC)

Uso de CPU (%) • Uso de RAM (%) • Network Tx/Rx  
Estado • Seleção automática/manual • e muito mais

---

### 🗄️ Proxmox Backup Server (PBS)

Uso do datastore (GB e %) • Número de backups  
Estado do Garbage Collector • Estado da última tarefa de backup  
• Informações completas de tarefas e muito mais
