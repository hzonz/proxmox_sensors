# 📚 Documentação e Guias

Para garantir uma configuração sem problemas, siga estes guias passo a passo:

---

## 🌡️ [01. Configuração dos Sensores de Hardware](01-install-sensors.md)
Como instalar e configurar **lm-sensors** no seu nó Proxmox para ativar o monitoramento de temperatura e ventoinhas.

---

## 🔑 [02. Configuração do Proxmox](02-proxmox-config.md)
Como criar um **usuário** e um **API Token** seguros no Proxmox (PVE e PBS) com as permissões mínimas necessárias.

---

## ⚙️ [03. Login da Integração (PVE e PBS)](03-login-pve-pbs.md)
Guia pelo processo de configuração inicial no Home Assistant e conexão com seus servidores.

---

## ❓ [04. Perguntas Frequentes e Solução de Problemas](04-faq.md)
Perguntas comuns, problemas conhecidos e como resolvê-los.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

## Introdução

**Proxmox Extended Sensors é a integração mais completa, eficiente e avançada para Home Assistant, projetada para fornecer controle real e monitoramento profundo do Proxmox VE e Proxmox Backup Server (PBS).**

Esta integração vai muito além da simples visualização de dados: oferece **visibilidade total** da sua infraestrutura e adiciona **capacidades reais de controle**, permitindo gerenciar nós, máquinas virtuais, contêineres, discos, datastores e tarefas do PBS diretamente pelo Home Assistant.

Ao contrário de outras soluções, Proxmox Extended Sensors foi construída com uma abordagem profissional:

- **Monitoramento avançado** de hardware, VMs, CTs, discos e PBS.  
- **Ações completas de controle** (iniciar, parar, desligar, reiniciar, resetar, pausar, hibernar…).  
- **Serviços de backup totalmente integrados**, tanto individuais quanto em massa.  
- **Compatibilidade total com PBS**, incluindo deduplicação e nomeação automática.  
- **Autenticação segura baseada em Tokens**.  
- **Estrutura limpa e organizada** de entidades e dispositivos.  
- **Uso mínimo de recursos** graças a um polling otimizado.

Os backups criados pelo Home Assistant se integram perfeitamente aos criados pelo Proxmox VE, usando nomes identificáveis como:  
**HA-{{vmid}}-{{guestname}}**  
e mantêm **todas as vantagens do PBS**, incluindo deduplicação e compatibilidade com cadeias de backup existentes.

Em resumo, esta integração transforma o Home Assistant em um **painel de controle completo para Proxmox**, combinando monitoramento detalhado, automação avançada e controle total da infraestrutura.

---

## 🧩 Versões Suportadas

- Proxmox VE 7.x / 8.x / 9.x  
- Proxmox Backup Server 3.x / 4.x  
- Home Assistant 2024.x ou superior

---

## 📑 Tabela de Conteúdos

- [Funcionalidades Principais](#-características-clave-v200)  
- [Estado e Desempenho do Nó](#-estado-y-rendimiento-del-nodo)  
- [Discos e SMART](#-discos-y-smart)  
- [Máquinas Virtuais (QEMU)](#-máquinas-virtuales-qemu)  
- [Contêineres (LXC)](#-contenedores-lxc)  
- [Serviços de Backup](#-servicios-de-backup-vms-y-cts)  
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)  
- [Ações de Controle (PVE e PBS)](#-acciones-de-control-pve-y-pbs)  
- [Instalação](#-instalación)  
- [Guia Visual de Configuração](#-guía-visual-de-configuración)  
- [Contribuições](#-contribuciones-y-comunidad)

---

<details>
  <summary>🖼️ Pré‑visualização do Dashboard</summary>
  <p align="center">
  <img src="/img/Dashboard.png" alt="Login Proxmox">
  </p>
  *Exemplo de um dashboard moderno usando **Card‑Mod** (Modo Escuro) e nossos sensores estruturados:*
</details>

---

## 🔥 Funcionalidades Principais (v2.0.0)

### 🌡️ Monitoramento Avançado de Hardware (PVE e PBS)

- **Temperaturas em tempo real:** núcleos da CPU, VRM, chipset, NVMe/SSD/HDD.  
- **Sensores mecânicos:** velocidades das ventoinhas (RPM), voltagens e outros sensores da placa‑mãe.  
- **Filtragem inteligente:** apenas entidades com dados válidos são criadas, mantendo o sistema limpo.  
  > Requer `lm-sensors` no host Proxmox.

---

### 🧠 Estado e Desempenho do Nó

- Uso de CPU, I/O wait, load average.  
- RAM total/usada/livre e porcentagem.  
- Tempo de atividade (uptime) e versão do kernel/PVE.  
- Sensores de rede RX/TX para o nó, VMs e contêineres.

<details>
  <summary>🔳 Atributos do Nó</summary>
  <p align="center">
    <img src="../../img/pve/node_attr.png" alt="Atributos do Nó" width="600">
  </p>
</details>

<details>
  <summary>⭕ Controles do Nó</summary>
  <p align="center">
    <img src="../../img/pve/node_controls.png" alt="Controles do Nó" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Temperatura da CPU</summary>
  <p align="center">
    <img src="../../img/pve/cpu_temp_attr.png" alt="Temperatura da CPU" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Temperatura do Chipset</summary>
  <p align="center">
    <img src="../../img/pve/chipset_temp.png" alt="Temperatura do Chipset" width="600">
  </p>
</details>

<details>
  <summary>⏳ CPU I/O Wait</summary>
  <p align="center">
    <img src="../../img/pve/cpu_wait.png" alt="CPU I/O Wait" width="600">
  </p>
</details>

---

### 💾 Discos & SMART

- Sensores de discos físicos agrupados como dispositivos dedicados.  
- Espaço total/usado, nível de desgaste (NVMe wear level) e mais.  
- Atributos SMART para HDD/SSD/NVMe (quando disponíveis).  
- Sensores de temperatura dedicados por tipo de disco (SATA, NVMe, etc.).

<details>
  <summary>💾 Sensores de Disco</summary>
  <p align="center">
    <img src="../../img/pve/disks_sensors.png" alt="Sensores de Disco" width="600">
  </p>
</details>

<details>
  <summary>🩺 Atributos SMART HDD/SSD</summary>
  <p align="center">
    <img src="../../img/pve/disk_hd_smart_attr.png" alt="SMART HDD" width="600">
  </p>
</details>

<details>
  <summary>🩺 Atributos SMART NVMe</summary>
  <p align="center">
    <img src="../../img/pve/disk_nvme_smart_attr.png" alt="SMART NVMe" width="600">
  </p>
</details>

---

### 🖥️ Máquinas Virtuais (QEMU)

- Estado, uso de CPU, RAM usada/total, disco usado/total.  
- Rede RX/TX por VM.  
- Uptime e sensores de informação básica.  
- Agrupamento limpo de dispositivos por VM no Home Assistant.

<details>
  <summary>🖥️ Controles e Sensores da VM</summary>
  <p align="center">
    <img src="../../img/pve/vm_control.png" alt="Controle da VM" width="600">
  </p>
</details>

---

### 📦 Contêineres (LXC)

- Estado, uso de CPU, RAM usada/total, disco usado/total.  
- Rede RX/TX por contêiner.  
- Uptime e sensores de informação básica.  
- Mesma estrutura limpa das VMs.

<details>
  <summary>📦 Controles e Sensores do Contêiner</summary>
  <p align="center">
    <img src="../../img/pve/ct_control.png" alt="Controle do CT" width="600">
  </p>
</details>

---

## 💾 Serviços de Backup (VMs e CTs)

A integração inclui dois poderosos serviços de backup que permitem criar **backups Proxmox diretamente pelo Home Assistant**, totalmente compatíveis com Proxmox VE e Proxmox Backup Server (PBS).
