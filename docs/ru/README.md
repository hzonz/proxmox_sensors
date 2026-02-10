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

---

### 🟦 1. Сервис индивидуального резервного копирования  
Создаёт резервную копию выбранной VM или CT.

**Сервис:** `proxmox_sensors.create_vzdump_backup`

**Доступные параметры:**

- **Узел** – Выберите узел Proxmox.  
- **Целевое хранилище** – Любое хранилище, поддерживающее резервные копии (local, NFS, PBS и т.д.).  
- **ID VM/CT** – ID машины, для которой создаётся резервная копия.  
- **Режим резервного копирования:**  
  - `snapshot`  
  - `suspend`  
  - `stop`  
- **Сжатие:**  
  - `zstd`  
  - `gzip`  
  - `lzo`  
  - `none`

Резервные копии, созданные из Home Assistant, автоматически получают имя:  
**HA-{{vmid}}-{{guestname}}**

Это обеспечивает удобную идентификацию и **полную совместимость с существующими резервными копиями Proxmox**.

<details>
  <summary>📦 Индивидуальный сервис резервного копирования</summary>
  <p align="center">
    <img src="../../img/pve/single_backup.png" alt="Индивидуальный сервис резервного копирования" width="600">
  </p>
</details>

---

### 🟩 2. Сервис массового резервного копирования  
Создаёт резервные копии **всех VM и/или CT** на выбранном узле.

**Сервис:** `proxmox_sensors.backup_all`

**Доступные параметры:**

- **Узел** – Выберите узел, с которого нужно сделать резервные копии.  
- **Целевое хранилище** – Любое хранилище, поддерживающее резервное копирование.  
- **Режим резервного копирования:** snapshot / suspend / stop.  
- **Сжатие:** zstd / gzip / lzo / none.  
- **Максимальное количество одновременных резервных копий** – Контролирует параллельное выполнение.  
- **Задержка между резервными копиями** – В секундах.  
- **Включить VM** – Переключатель (Да/Нет).  
- **Включить CT** – Переключатель (Да/Нет).

Этот сервис идеально подходит для ночных автоматических резервных копий или регулярного обслуживания.

<details>
  <summary>📦 Сервис массового резервного копирования</summary>
  <p align="center">
    <img src="../../img/pve/massive_backups.png" alt="Сервис массового резервного копирования" width="600">
  </p>
</details>

---

### 🟧 Совместимость с PBS и дедупликация

Резервные копии, созданные этими сервисами:

- Хранятся точно так же, как созданные через Proxmox VE  
- Используют ту же структуру имён и метаданных  
- Автоматически поддерживают **дедупликацию PBS**  
- Бесшовно интегрируются в существующие цепочки резервных копий  
- Отображаются в PBS datastore с полной совместимостью  

Никаких дополнительных настроек не требуется — PBS выполняет дедупликацию и индексацию так же, как если бы резервная копия была создана через GUI или CLI Proxmox.

---

### 🗄️ Proxmox Backup Server (PBS)

**Глубокий мониторинг datastore и задач:**

- Использование datastore (GB и %), всего, занято и свободно.  
- Коэффициент дедупликации и количество резервных копий.  
- Время, размер и статус последней резервной копии.  
- Ошибки резервного копирования и сводка задач.  
- Статус Garbage Collector (GC) и связанные датчики.  
- Последняя задача: тип, статус, сообщение и длительность.

<details>
  <summary>🗄️ Обзор Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore.png" alt="Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Сервер PBS</summary>
  <p align="center">
    <img src="../../img/pbs/pbs_server.png" alt="PBS Server" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Детали задач</summary>
  <p align="center">
    <img src="../../img/pbs/task.png" alt="PBS Task" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Статус Garbage Collector</summary>
  <p align="center">
    <img src="../../img/pbs/gc_status_attr.png" alt="GC Status" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Обслуживание Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Datastore Maintenance" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Сводка последней задачи</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Last Task" width="600">
  </p>
</details>

---

## Действия управления PBS:

- Запустить **Garbage Collector (GC)**  
- Запустить **Prune**  
- Запустить **Verify**  
- Запустить **Sync**  

<details>
  <summary>🗄️ Обслуживание Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Datastore Maintenance" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Последняя задача</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Last Task" width="600">
  </p>
</details>

---

### 🎛️ Действия управления (PVE & PBS)

**Управление узлом:**

- Выключить узел  
- Перезагрузить узел  

**Управление виртуальными машинами (QEMU):**

- Запуск, Остановка, Выключение, Перезагрузка, Reset  
- Пауза, Возобновление, Гибернация  

**Управление контейнерами (LXC):**

- Запуск, Остановка, Выключение, Перезагрузка  

**Управление PBS:**

- GC, Prune, Verify, Sync (для каждого datastore)

---

### 🎨 Визуальная организация и именование

- Датчики автоматически группируются в логические устройства:
  1. Узел  
  2. Физические диски  
  3. Виртуальные машины  
  4. Контейнеры  
  5. Хранилища / Datastores  
  6. Сервер PBS и задачи  

- Чистые и последовательные имена сущностей и устройств обеспечивают удобство чтения и масштабируемость dashboard.

---

## 🧩 Установка

### 🔹 Через HACS (рекомендуется)

1. Откройте **HACS → Integrations**  
2. Нажмите на три точки (⋮) → **Custom repositories**  
3. Добавьте репозиторий:  
   - URL: `https://github.com/Javisen/proxmox_sensors`  
   - Категория: **Integration**  
4. Найдите **“Proxmox Extended Sensors”** в HACS и установите  
5. Перезапустите Home Assistant  
6. Перейдите в **Настройки → Устройства и сервисы → Добавить интеграцию** и найдите **Proxmox Extended Sensors**

### 🔹 Ручная установка

1. Скопируйте папку `custom_components/proxmox_sensors` в:  
   - `/config/custom_components/proxmox_sensors`  
2. Перезапустите Home Assistant  
3. Добавьте интеграцию через **Настройки → Устройства и сервисы**

---

## 🧭 Визуальное руководство по настройке

Ниже приведено полное визуальное руководство по процессу настройки, включая методы входа, выбор ресурсов и шаги установки.

<details>
  <summary>🪪 Подключение к серверу</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Не нужно вводить "http://" или "https://". Это выполняется автоматически.
</details>

<details>
  <summary>🪪 Вход по имени пользователя и паролю (только PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Убедитесь, что используете правильный realm (`pam` или `pve`).
</details>

<details> 
  <summary>🪪 Вход по пользователю и токену (PVE и PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **В поле Token_id вводится только имя токена.**
</details>

<details>
  <summary>⚙️ Выбор ресурсов</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Выбор ресурсов" width="600">
  </p>
  *Примечание: выберите CT, VM и хранилища, которые хотите добавить, а также нужные параметры.*
</details>

---

**Если вам нравится эта интеграция или она оказалась полезной, пожалуйста, поставьте ⭐ на GitHub.**  
**Это помогает развитию проекта, повышает его видимость и поддерживает будущие функции.**

## 🤝 Вклад и сообщество

Вклад приветствуется! Вы можете открыть issue или pull request.  
**[Перейти в репозиторий GitHub](https://github.com/Javisen/proxmox_sensors)**

---

<p align="center"><i>Поддерживается Javisen — лицензия MIT</i></p>
