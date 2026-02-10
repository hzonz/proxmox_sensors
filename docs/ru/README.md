# 📚 Документация и Руководства

Чтобы обеспечить корректную и беспроблемную настройку, пожалуйста, следуйте этим пошаговым руководствам:

---

## 🌡️ [01. Настройка аппаратных датчиков](01-install-sensors.md)
Как установить и настроить **lm-sensors** на вашем узле Proxmox для включения мониторинга температуры и вентиляторов.

---

## 🔑 [02. Настройка Proxmox](02-proxmox-config.md)
Как создать безопасного **пользователя** и **API Token** в Proxmox (PVE и PBS) с минимально необходимыми правами.

---

## ⚙️ [03. Вход в интеграцию (PVE и PBS)](03-login-pve-pbs.md)
Пошаговое руководство по первичной настройке в Home Assistant и подключению к вашим серверам.

---

## ❓ [04. Часто задаваемые вопросы и устранение неполадок](04-faq.md)
Распространённые вопросы, известные проблемы и способы их решения.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

## Введение

**Proxmox Extended Sensors — это самая полная, эффективная и продвинутая интеграция для Home Assistant, созданная для обеспечения реального контроля и глубокого мониторинга Proxmox VE и Proxmox Backup Server (PBS).**

Эта интеграция выходит далеко за рамки простой визуализации данных: она предоставляет **полную видимость** вашей инфраструктуры и добавляет **реальные возможности управления**, позволяя контролировать узлы, виртуальные машины, контейнеры, диски, datastores и задачи PBS напрямую из Home Assistant.

В отличие от других решений, Proxmox Extended Sensors разработана с профессиональным подходом:

- **Расширенный мониторинг** оборудования, ВМ, CT, дисков и PBS.  
- **Полный набор управляющих действий** (запуск, остановка, выключение, перезагрузка, сброс, пауза, гибернация…).  
- **Полностью интегрированные сервисы резервного копирования**, как одиночные, так и массовые.  
- **Полная совместимость с PBS**, включая дедупликацию и автоматическое именование.  
- **Безопасная аутентификация на основе токенов**.  
- **Чистая и организованная структура** сущностей и устройств.  
- **Минимальная нагрузка на систему** благодаря оптимизированному опросу (polling).

Резервные копии, созданные из Home Assistant, полностью совместимы с копиями, созданными в Proxmox VE, используют понятные имена, например:  
**HA-{{vmid}}-{{guestname}}**  
и сохраняют **все преимущества PBS**, включая дедупликацию и совместимость с существующими цепочками резервных копий.

В итоге эта интеграция превращает Home Assistant в **полноценную панель управления Proxmox**, объединяя детальный мониторинг, продвинутую автоматизацию и полный контроль инфраструктуры.

---

## 🧩 Поддерживаемые версии

- Proxmox VE 7.x / 8.x / 9.x  
- Proxmox Backup Server 3.x / 4.x  
- Home Assistant 2024.x или новее

---

## 📑 Содержание

- [Ключевые возможности](#-характеристики-клаве-v200)  
- [Состояние и производительность узла](#-estado-y-rendimiento-del-nodo)  
- [Диски и SMART](#-discos-y-smart)  
- [Виртуальные машины (QEMU)](#-máquinas-virtuales-qemu)  
- [Контейнеры (LXC)](#-contenedores-lxc)  
- [Сервисы резервного копирования](#-servicios-de-backup-vms-y-cts)  
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)  
- [Управляющие действия (PVE и PBS)](#-acciones-de-control-pve-y-pbs)  
- [Установка](#-instalación)  
- [Визуальное руководство по настройке](#-guía-visual-de-configuración)  
- [Вклад в проект](#-contribuciones-y-comunidad)

---

<details>
  <summary>🖼️ Пример Dashboard</summary>
  <p align="center">
  <img src="/img/Dashboard.png" alt="Login Proxmox">
  </p>
  *Пример современного dashboard с использованием **Card‑Mod** (тёмная тема) и структурированных датчиков:*
</details>

---

## 🔥 Ключевые возможности (v2.0.0)

### 🌡️ Расширенный мониторинг оборудования (PVE и PBS)

- **Температуры в реальном времени:** ядра CPU, VRM, чипсет, NVMe/SSD/HDD.  
- **Механические датчики:** скорость вентиляторов (RPM), напряжения и другие датчики материнской платы.  
- **Интеллектуальная фильтрация:** создаются только сущности с валидными данными, чтобы система оставалась чистой.  
  > Требуется `lm-sensors` на хосте Proxmox.

---

### 🧠 Состояние и производительность узла

- Загрузка CPU, I/O wait, load average.  
- RAM всего/использовано/свободно и процент.  
- Время работы (uptime) и версия kernel/PVE.  
- Сетевые датчики RX/TX для узла, ВМ и контейнеров.

<details>
  <summary>🔳 Атрибуты узла</summary>
  <p align="center">
    <img src="../../img/pve/node_attr.png" alt="Атрибуты узла" width="600">
  </p>
</details>

<details>
  <summary>⭕ Управление узлом</summary>
  <p align="center">
    <img src="../../img/pve/node_controls.png" alt="Управление узлом" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Температура CPU</summary>
  <p align="center">
    <img src="../../img/pve/cpu_temp_attr.png" alt="Температура CPU" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Температура чипсета</summary>
  <p align="center">
    <img src="../../img/pve/chipset_temp.png" alt="Температура чипсета" width="600">
  </p>
</details>

<details>
  <summary>⏳ CPU I/O Wait</summary>
  <p align="center">
    <img src="../../img/pve/cpu_wait.png" alt="CPU I/O Wait" width="600">
  </p>
</details>

---

### 💾 Диски и SMART

- Датчики физических дисков сгруппированы как отдельные устройства.  
- Общий/использованный объём, уровень износа (NVMe wear level) и другое.  
- SMART‑атрибуты для HDD/SSD/NVMe (если доступны).  
- Отдельные температурные датчики для каждого типа дисков (SATA, NVMe и др.).

<details>
  <summary>💾 Датчики дисков</summary>
  <p align="center">
    <img src="../../img/pve/disks_sensors.png" alt="Датчики дисков" width="600">
  </p>
</details>

<details>
  <summary>🩺 SMART‑атрибуты HDD/SSD</summary>
  <p align="center">
    <img src="../../img/pve/disk_hd_smart_attr.png" alt="SMART HDD" width="600">
  </p>
</details>

<details>
  <summary>🩺 SMART‑атрибуты NVMe</summary>
  <p align="center">
    <img src="../../img/pve/disk_nvme_smart_attr.png" alt="SMART NVMe" width="600">
  </p>
</details>

---

### 🖥️ Виртуальные машины (QEMU)

- Статус, загрузка CPU, RAM использовано/всего, диск использовано/всего.  
- Сеть RX/TX для каждой ВМ.  
- Время работы и базовые информационные датчики.  
- Чистая структура устройств для каждой ВМ в Home Assistant.

<details>
  <summary>🖥️ Управление и датчики ВМ</summary>
  <p align="center">
    <img src="../../img/pve/vm_control.png" alt="Управление ВМ" width="600">
  </p>
</details>

---

### 📦 Контейнеры (LXC)

- Статус, загрузка CPU, RAM использовано/всего, диск использовано/всего.  
- Сеть RX/TX для каждого контейнера.  
- Время работы и базовые информационные датчики.  
- Та же чистая структура устройств, что и у ВМ.

<details>
  <summary>📦 Управление и датчики контейнеров</summary>
  <p align="center">
    <img src="../../img/pve/ct_control.png" alt="Управление CT" width="600">
  </p>
</details>

---

## 💾 Сервисы резервного копирования (ВМ и CT)

Интеграция включает два мощных сервиса резервного копирования, позволяющих создавать **резервные копии Proxmox напрямую из Home Assistant**, полностью совместимые с Proxmox VE и Proxmox Backup Server (PBS).
