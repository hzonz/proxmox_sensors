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

---

### 🟦 1. Serviço de Backup Individual  
Cria um backup de uma VM ou CT específica.

**Serviço:** `proxmox_sensors.create_vzdump_backup`

**Opções disponíveis:**

- **Nó** – Seleciona o nó Proxmox.  
- **Armazenamento de Destino** – Qualquer armazenamento que suporte backups (local, NFS, PBS, etc.).  
- **ID da VM/CT** – ID da máquina a ser copiada.  
- **Modo de backup:**  
  - `snapshot`  
  - `suspend`  
  - `stop`  
- **Compressão:**  
  - `zstd`  
  - `gzip`  
  - `lzo`  
  - `none`

Os backups criados pelo Home Assistant são automaticamente nomeados como:  
**HA-{{vmid}}-{{guestname}}**

Isso garante fácil identificação e mantém **total compatibilidade com os backups existentes do Proxmox**.

<details>
  <summary>📦 Serviço de Backup Individual</summary>
  <p align="center">
    <img src="../../img/pve/single_backup.png" alt="Serviço de Backup Individual" width="600">
  </p>
</details>

---

### 🟩 2. Serviço de Backup Massivo  
Realiza backups de **todas as VMs e/ou CTs** em um nó selecionado.

**Serviço:** `proxmox_sensors.backup_all`

**Opções disponíveis:**

- **Nó** – Seleciona o nó do qual fazer o backup.  
- **Armazenamento de Destino** – Qualquer armazenamento compatível com backups.  
- **Modo de backup:** snapshot / suspend / stop.  
- **Compressão:** zstd / gzip / lzo / none.  
- **Máximo de backups simultâneos** – Controla a execução paralela.  
- **Atraso entre backups** – Segundos entre cada backup.  
- **Incluir VMs** – Alternador (Sim/Não).  
- **Incluir CTs** – Alternador (Sim/Não).

Este serviço é ideal para backups noturnos agendados ou rotinas de manutenção automatizadas.

<details>
  <summary>📦 Serviço de Backup Massivo</summary>
  <p align="center">
    <img src="../../img/pve/massive_backups.png" alt="Serviço de Backup Massivo" width="600">
  </p>
</details>

---

### 🟧 Compatibilidade PBS e Deduplicação

Os backups criados por estes serviços:

- São armazenados exatamente como os criados pelo Proxmox VE  
- Usam a mesma estrutura de nomes e metadados  
- Suportam automaticamente a **deduplicação do PBS**  
- Integram-se perfeitamente às cadeias de backup existentes  
- Aparecem no datastore do PBS com total compatibilidade  

Nenhuma configuração especial é necessária — o PBS gerencia deduplicação e indexação exatamente como se o backup tivesse sido criado pela interface gráfica ou CLI do Proxmox.

---

### 🗄️ Proxmox Backup Server (PBS)

**Monitoramento avançado do datastore e das tarefas:**

- Uso do datastore (GB e %), total, usado e livre.  
- Taxa de deduplicação e número de backups.  
- Hora, tamanho e estado do último backup.  
- Erros de backup e resumo de tarefas.  
- Estado do Garbage Collector (GC) e sensores relacionados.  
- Última tarefa: tipo, estado, mensagem e duração.

<details>
  <summary>🗄️ Visão Geral do Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore.png" alt="Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Servidor PBS</summary>
  <p align="center">
    <img src="../../img/pbs/pbs_server.png" alt="Servidor PBS" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Detalhes das Tarefas</summary>
  <p align="center">
    <img src="../../img/pbs/task.png" alt="Tarefa PBS" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Estado do Garbage Collector</summary>
  <p align="center">
    <img src="../../img/pbs/gc_status_attr.png" alt="GC Status" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Manutenção do Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Manutenção do Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Resumo da Última Tarefa</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Última Tarefa" width="600">
  </p>
</details>

---

## Ações de controle PBS:

- Executar **Garbage Collector (GC)**  
- Executar **Prune**  
- Executar **Verify**  
- Executar **Sync**  

<details>
  <summary>🗄️ Manutenção do Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Manutenção do Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Última Tarefa</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Última Tarefa" width="600">
  </p>
</details>

---

### 🎛️ Ações de Controle (PVE & PBS)

**Controles do nó:**

- Desligar nó  
- Reiniciar nó  

**Controles de máquinas virtuais (QEMU):**

- Iniciar, Parar, Desligar, Reiniciar, Resetar  
- Pausar, Retomar, Hibernar  

**Controles de contêineres (LXC):**

- Iniciar, Parar, Desligar, Reiniciar  

**Controles PBS:**

- GC, Prune, Verify, Sync (por datastore)

---

### 🎨 Organização Visual e Nomenclatura

- Sensores agrupados automaticamente em dispositivos lógicos:
  1. Nó  
  2. Discos físicos  
  3. Máquinas virtuais  
  4. Contêineres  
  5. Storages / Datastores  
  6. Servidor PBS e tarefas  

- Nomes consistentes e limpos para entidades e dispositivos, mantendo dashboards organizados e escaláveis.

---

## 🧩 Instalação

### 🔹 Via HACS (recomendado)

1. Abra **HACS → Integrações**  
2. Clique nos três pontos (⋮) → **Custom repositories**  
3. Adicione este repositório:  
   - URL: `https://github.com/Javisen/proxmox_sensors`  
   - Categoria: **Integration**  
4. Procure por **“Proxmox Extended Sensors”** no HACS e instale  
5. Reinicie o Home Assistant  
6. Vá para **Configurações → Dispositivos e Serviços → Adicionar Integração** e procure **Proxmox Extended Sensors**

### 🔹 Instalação manual

1. Copie a pasta `custom_components/proxmox_sensors` para:  
   - `/config/custom_components/proxmox_sensors`  
2. Reinicie o Home Assistant  
3. Adicione a integração em **Configurações → Dispositivos e Serviços**

---

## 🧭 Guia Visual de Configuração

A seguir, um guia visual completo do processo de configuração, incluindo métodos de login, seleção de recursos e etapas de instalação.

<details>
  <summary>🪪 Conexão com o Servidor</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Não é necessário digitar "http://" ou "https://". Isso é feito automaticamente.
</details>

<details>
  <summary>🪪 Login com Usuário e Senha (somente PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Certifique-se de usar o realm correto (`pam` ou `pve`).
</details>

<details> 
  <summary>🪪 Login com Usuário e Token (PVE e PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **No campo Token_id, insira apenas o nome do token.**
</details>

<details>
  <summary>⚙️ Seleção de Recursos</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Seleção de Recursos" width="600">
  </p>
  *Nota: selecione os CTs, VMs e Storages que deseja adicionar, juntamente com as opções desejadas.*
</details>

---

**Se você gosta desta integração ou a considera útil, deixe uma ⭐ no GitHub.**  
**Isso ajuda na visibilidade, motiva o desenvolvimento e apoia futuras funcionalidades.**

## 🤝 Contribuições & Comunidade

Contribuições são bem-vindas! Você pode abrir issues ou pull requests.  
**[Visitar o repositório no GitHub](https://github.com/Javisen/proxmox_sensors)**

---

<p align="center"><i>Mantido por Javisen – Licença MIT</i></p>
