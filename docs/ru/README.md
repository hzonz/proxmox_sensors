<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

# 🚀 Proxmox Extended Sensors

**Самая полная, эффективная и организованная интеграция для мониторинга Proxmox VE и PBS из Home Assistant.**

Эта интеграция разработана для пользователей, которым необходим полный контроль над своим оборудованием без перегрузки сервера. В отличие от других решений, **Proxmox Sensors Extended** фокусируется на энергоэффективности, безопасной аутентификации на основе токенов и безупречной визуальной организации.

---

## 📚 Документация и руководства
**Выберите ваш язык, чтобы начать установку и настройку:**

[![English](https://img.shields.io/badge/ENGLISH-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/en/README.md)
[![Español](https://img.shields.io/badge/ESPA%C3%91OL-orange?style=for-the-badge&logo=translate&logoColor=white)](docs/es/README.md)
[![Italiano](https://img.shields.io/badge/ITALIANO-green?style=for-the-badge&logo=translate&logoColor=white)](docs/it/README.md)
[![Français](https://img.shields.io/badge/FRAN%C3%87AIS-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/fr/README.md)
[![Deutsch](https://img.shields.io/badge/DEUTSCH-red?style=for-the-badge&logo=translate&logoColor=white)](docs/de/README.md)
[![Nederlands](https://img.shields.io/badge/NEDERLANDS-orange?style=for-the-badge&logo=translate&logoColor=white)](docs/nl/README.md)
[![Русский](https://img.shields.io/badge/%D0%A0%D0%A3%D0%A1%D0%A1%D0%9A%D0%98%D0%99-lightgrey?style=for-the-badge&logo=translate&logoColor=white)](docs/ru/README.md)

---

## 🖼️ Предварительный просмотр панели
*Пример современной панели управления с использованием **Card-Mod** (темный режим) и наших структурированных датчиков:*

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

---

## 🔥 Ключевые особенности

### 🌡️ Глубокий мониторинг оборудования
* **Температура в реальном времени:** Ядра процессора, VRM и накопители NVMe/SSD/HDD.
* **Механические датчики:** Скорость вращения вентиляторов (RPM) и напряжения материнской платы.
* **Умная фильтрация:** Создаются только объекты с валидными данными.
*(Примечание: требуется наличие lm-sensors на хосте Proxmox).*

### 🧠 Производительность и безопасность
* **DataUpdateCoordinator:** Минимизирует количество вызовов API для экономии ресурсов процессора.
* **Бесшумный SSL:** Работа с самоподписанными сертификатами без спама в логах.
* **Безопасная аутентификация:** Полная поддержка токенов API Proxmox (PVE и PBS).

### 🎨 Визуальная организация
* **Умная группировка:** Датчики автоматически упорядочены по категориям: **1. Узел (Node)**, **2. Физические диски**, **3. Виртуальные машины**, **4. Контейнеры**.
* **Авто-префиксы:** Список ваших объектов и панелей всегда отсортирован по умолчанию.

---

## 🚀 План развития (Roadmap)
- [ ] Датчики сети RX/TX для виртуальных машин и контейнеров.
- [ ] Расширенные метрики CPU/RAM хоста.
- [ ] Шаблоны пользовательских карт Lovelace.
- [ ] Подача заявки в официальный репозиторий HACS.

---

## 🤝 Сообщество и участие в разработке
Мы приветствуем любую помощь! Не стесняйтесь открывать Issues или создавать Pull Requests.
**[Посетить репозиторий GitHub](https://github.com/Javisen/proxmox_sensors)**

---
<p align="center"><i>Поддерживается Javisen - Лицензия MIT</i></p>
