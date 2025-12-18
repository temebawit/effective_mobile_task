# High-Availability Reverse Proxy & Backend Service

## Overview
Данный проект представляет собой отказоустойчивую микросервисную архитектуру, реализованную с помощью Docker Compose. Проект демонстрирует применение паттерна **Reverse Proxy** для изоляции бэкенд-приложений, управления трафиком и обеспечения безопасности сетевого периметра.

## Architecture & Design Decisions
Система разделена на два изолированных уровня (tiers):
1.  **Proxy Tier (Nginx):** * Базируется на `nginx:1.25.3-alpine` для минимизации размера образа и поверхности атаки.
    * Выполняет роль терминатора трафика и проксирует запросы на upstream-сервисы по внутренней сети Docker.
    * Сконфигурирован с удалением стандартных `default.conf` для исключения утечки информации о версии сервера и предотвращения конфликтов конфигурации.
2.  **Application Tier (Python):**
    * Базируется на **Python 3.11.7-slim**, что обеспечивает оптимальный баланс между производительностью среды исполнения и безопасностью дистрибутива (Debian Bookworm).
    * Запускается от имени **non-root пользователя** (`appuser`), что минимизирует риски при потенциальной компрометации приложения.
    * Реализован декларативный механизм **Healthchecks**, гарантирующий доступность upstream-сервиса перед началом маршрутизации трафика на уровне прокси.

## Security & Networking
* **Network Isolation:** Используется кастомная bridge-сеть `internal_net`. Бэкенд-сервис лишен прямого доступа из внешних сетей (отсутствует директива `ports`), взаимодействие возможно строго через Nginx.
* **Configuration Management:** Все чувствительные параметры (порты, окружения) вынесены в `.env`.

## Deployment

### Prerequisites
* Docker Engine >= 20.10
* Docker Compose v2.x+

### Quick Start
1.  Клонируйте репозиторий:
    ```bash
    git clone [https://github.com/temebawit/effective_mobile_task.git](https://github.com/temebawit/effective_mobile_task.git)
    cd effective_mobile_task
    ```

2.  Подготовьте окружение:
    ```bash
    # Убедитесь, что EXTERNAL_PORT в .env не конфликтует с системными службами
    docker compose up -d --build
    ```

## API Specification
Сервис предоставляет эндпоинт, возвращающий состояние системы в формате JSON.

**Request:** `GET /`

**Response (200 OK):**
```json
{
    "message": "hello from effective mobile!",
    "user": "appuser",
    "status": "operational"
}
```
Maintenance & Monitoring
Просмотр состояния сервисов и логов:

```bash
docker compose ps
docker compose logs -f nginx
```
Валидация состояния Healthcheck:

```bash
docker inspect --format='{{json .State.Health.Status}}' python_backend
```
Cleanup
Для полной деструкции окружения:
```bash
docker compose down --rmi local
```
Bash

docker compose down --rmi local
