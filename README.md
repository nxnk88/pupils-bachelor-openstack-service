# Отчет по дисциплине
"Технология проектирования автоматизированных систем в защищенном исполнении"

## Тема работы

Разработка и деплой веб-сервиса для аудита защищенности рабочих станций

## Студентs


`gofman03`
`aksenov04`
`kopan05`
## Дата выполнения

`17.06.2026`

## Название проекта

`protected-workstation-audit-service`

## 1. Цель работы

Цель работы - разработать учебный DevOps-проект
`protected-workstation-audit-service`, который демонстрирует полный цикл
подготовки приложения к запуску:

- создание REST API на FastAPI;
- обработка данных рабочих станций с помощью pandas;
- упаковка приложения в Docker-образ;
- публикация Docker-образа в Docker Hub;
- описание инфраструктуры OpenStack через Terraform;
- запуск приложения на виртуальной машине через cloud-init;
- подготовка Kubernetes-манифестов для запуска в Minikube.

## 2. Описание проекта

Проект представляет собой FastAPI-сервис для аудита рабочих станций и
определения систем, готовых к вводу в защищенный контур.

В приложении используется тестовый набор рабочих станций. Для каждой станции
хранятся поля:

- `hostname` - имя рабочей станции;
- `department` - подразделение;
- `hardening_score` - оценка защищенности конфигурации;
- `antivirus_enabled` - признак активного антивируса;
- `disk_encryption` - признак включенного шифрования диска.

Готовыми к вводу в защищенный контур считаются рабочие станции, для которых:

- `hardening_score >= 85`;
- `antivirus_enabled = true`;
- `disk_encryption = true`.

Эндпоинт `/audit-ready` возвращает сообщение:

```text
Рабочая станция готова к вводу в защищенный контур
```

Также он возвращает общее количество готовых станций, распределение по
подразделениям и список рабочих станций, прошедших аудит.

## 3. Используемые технологии

- Python 3.11;
- FastAPI;
- Uvicorn;
- pandas;
- Docker;
- Docker Hub;
- Terraform `>= 1.5.0`;
- OpenStack Terraform provider `terraform-provider-openstack/openstack`;
- OpenStack;
- cloud-init;
- Kubernetes;
- Minikube;
- kubectl.

## 4. Репозиторий и иллюстрации

Проект размещен в учебном GitHub-репозитории:

```text
https://github.com/nxnk88/pupils-bachelor-openstack-service
```

URL репозитория сохранен прежним, но содержимое проекта, API и отчет были
переработаны под новую тему `protected-workstation-audit-service`.

Скриншоты в отчете сохранены как иллюстрации этапов технологического контура
Docker, Terraform, OpenStack и Kubernetes. Они фиксируют последовательность
развертывания и проверки инфраструктуры, поэтому в отдельных архивных снимках
могут встречаться старые технические имена.

![Рисунок 1. Репозиторий проекта на GitHub](screenshots/01-github-repository.jpg)
*Рисунок 1. Учебный репозиторий проекта на GitHub.*

Структура локального проекта:

```text
.
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
├── DEFENSE.md
├── screenshots/
├── terraform-openstack/
└── k8s/
```

![Рисунок 2. Структура проекта](screenshots/02-project-tree.jpg)
*Рисунок 2. Структура локального проекта.*

## 5. Описание API

| Метод | Путь | Назначение |
| --- | --- | --- |
| `GET` | `/` | Главная страница сервиса |
| `GET` | `/health` | Проверка состояния приложения |
| `GET` | `/workstations` | Получение списка всех рабочих станций |
| `GET` | `/workstations?department=...` | Фильтрация по подразделению |
| `GET` | `/workstation/{hostname}` | Поиск рабочей станции по имени |
| `GET` | `/audit-ready` | Получение списка станций, прошедших аудит |

Если рабочая станция найдена через `/workstation/{hostname}`, сервис возвращает
ее данные. Если запись не найдена, возвращается HTTP-ответ `404`.

Пример проверки API:

```bash
curl.exe http://127.0.0.1:8000/
curl.exe http://127.0.0.1:8000/health
curl.exe http://127.0.0.1:8000/workstations
curl.exe http://127.0.0.1:8000/audit-ready
```

В PowerShell рекомендуется использовать именно `curl.exe`, потому что команда
`curl` может быть псевдонимом `Invoke-WebRequest`.

## 6. Локальный запуск

Для локального запуска нужно создать виртуальное окружение, установить
зависимости и запустить приложение через Uvicorn.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI подтверждает, что приложение успешно запущено и все эндпоинты
доступны для тестирования.

![Рисунок 3. Swagger UI FastAPI](screenshots/03-swagger-ui.jpg)
*Рисунок 3. Swagger UI приложения.*

## 7. Docker

Docker используется для упаковки FastAPI-приложения в переносимый контейнер.

```bash
docker build -t protected-workstation-audit-service .
docker run -d --name workstation-audit -p 8000:8000 protected-workstation-audit-service
docker ps
curl.exe http://127.0.0.1:8000/health
curl.exe http://127.0.0.1:8000/audit-ready
docker rm -f workstation-audit
```

Если локальный порт `8000` занят другим сервисом, можно использовать внешний
порт `8001`:

```powershell
docker rm -f workstation-audit
docker run -d --name workstation-audit -p 8001:8000 protected-workstation-audit-service
docker ps
curl.exe http://127.0.0.1:8001/health
curl.exe http://127.0.0.1:8001/audit-ready
```

![Рисунок 4. Сборка Docker-образа](screenshots/04-docker-build.jpg)
*Рисунок 4. Сборка Docker-образа.*

![Рисунок 5. Запуск контейнера Docker](screenshots/05-docker-container.jpg)
*Рисунок 5. Запущенный контейнер с приложением.*

![Рисунок 6. Проверка API локального контейнера](screenshots/06-local-api-check.jpg)
*Рисунок 6. Проверка локального API через `curl.exe`.*

## 8. Публикация Docker-образа

Для развертывания через OpenStack VM и Kubernetes образ должен быть опубликован в
Docker Hub.

```bash
docker login
docker tag protected-workstation-audit-service YOUR_DOCKERHUB_LOGIN/protected-workstation-audit-service:v1
docker push YOUR_DOCKERHUB_LOGIN/protected-workstation-audit-service:v1
```

Пример имени образа:

```text
YOUR_DOCKERHUB_LOGIN/protected-workstation-audit-service:v1
```

![Рисунок 7. Docker Hub с опубликованным образом](screenshots/07-docker-hub.jpg)
*Рисунок 7. Docker Hub с опубликованным образом.*

После публикации этот образ используется в:

- `terraform-openstack/terraform.tfvars`;
- `k8s/deployment.yaml`.

## 9. Развертывание в OpenStack через Terraform

Terraform-конфигурация находится в каталоге `terraform-openstack/`.

Она создает:

- приватную сеть `workstation-audit-network`;
- подсеть `workstation-audit-subnet`;
- роутер `workstation-audit-router`;
- Security Group `workstation-audit-sg`;
- правила доступа по портам `22/tcp` и `8000/tcp`;
- SSH keypair;
- сетевой порт для VM;
- виртуальную машину `workstation-audit-vm`;
- Floating IP;
- привязку Floating IP к VM;
- cloud-init для установки Docker и запуска контейнера.

Команды запуска Terraform:

Если `terraform init` завершается ошибкой `Invalid provider registry host`, на
этой машине нужно использовать локальный каталог уже скачанного провайдера:

```powershell
cd terraform-openstack
.\terraform-init.ps1
```

Или напрямую:

```powershell
terraform init "-plugin-dir=.terraform\\providers"
```

После инициализации выполняются остальные шаги:

```bash
cd terraform-openstack
cp terraform.tfvars.example terraform.tfvars
terraform validate
terraform plan
terraform apply
terraform state list
terraform output
```

После успешного выполнения Terraform выводятся:

- `public_ip`;
- `service_url`;
- `health_url`;
- `audit_ready_url`;
- `ssh_command`.

![Рисунок 8. Terraform apply, state list и output](screenshots/08-terraform-apply-state-output.jpg)
*Рисунок 8. Terraform: создание ресурсов, `state list` и `output`.*

## 10. Проверка работы сервиса в OpenStack

После создания ресурсов сервис проверяется по Floating IP:

```bash
curl.exe http://<FLOATING_IP>:8000/health
curl.exe http://<FLOATING_IP>:8000/audit-ready
ssh ubuntu@<FLOATING_IP>
sudo docker ps
sudo docker logs workstation-audit
```

OpenStack Dashboard показывает, что виртуальная машина была создана и получила
внутренний и внешний IP-адреса.

![Рисунок 9. Виртуальная машина в OpenStack](screenshots/09-openstack-instance.jpg)
*Рисунок 9. Инстанс в OpenStack Dashboard.*

Проверка по Floating IP подтверждает доступность `/health` и бизнес-эндпоинта
`/audit-ready`.

![Рисунок 10. Проверка сервиса по Floating IP](screenshots/10-openstack-api-check.jpg)
*Рисунок 10. Проверка сервиса по Floating IP.*

Дополнительная проверка по SSH подтверждает, что на виртуальной машине работает
Docker-контейнер с приложением.

![Рисунок 11. Проверка контейнера на VM](screenshots/11-vm-docker-check.jpg)
*Рисунок 11. Проверка Docker-контейнера на виртуальной машине.*

## 11. Kubernetes / Minikube

В каталоге `k8s/` находятся Kubernetes-манифесты:

- `namespace.yaml` - namespace `workstation-audit`;
- `deployment.yaml` - Deployment на 2 реплики;
- `service.yaml` - NodePort Service на порту `30080`.

Для корректного развертывания манифесты применяются по отдельности в правильном
порядке:

```powershell
& "$env:TEMP\minikube-check\minikube-v1.34.0.exe" start --driver=docker --container-runtime=docker
kubectl apply -f .\k8s\namespace.yaml
kubectl apply -f .\k8s\deployment.yaml
kubectl apply -f .\k8s\service.yaml
kubectl rollout status deployment/workstation-audit-deployment -n workstation-audit
kubectl get pods -n workstation-audit
kubectl get svc -n workstation-audit
kubectl get endpoints -n workstation-audit
```

Результат развертывания показывает, что Deployment успешно раскатился, два pod'а
перешли в состояние `Running`, а Service получил endpoints.

![Рисунок 12. Развертывание в Kubernetes](screenshots/12-k8s-rollout-pods-service.jpg)
*Рисунок 12. Kubernetes: rollout, pod'ы, Service и endpoints.*

Для локальной проверки API через Kubernetes используется `port-forward`.

```powershell
kubectl port-forward -n workstation-audit service/workstation-audit-service 18080:8000
```

В другом окне PowerShell:

```powershell
curl.exe http://127.0.0.1:18080/health
curl.exe http://127.0.0.1:18080/audit-ready
```

![Рисунок 13. Проверка Kubernetes через port-forward](screenshots/13-k8s-port-forward-check.jpg)
*Рисунок 13. Проверка API через `kubectl port-forward`.*

## 12. Скриншоты, включенные в отчет

В отчет включены следующие иллюстрации этапов развертывания:

1. [screenshots/01-github-repository.jpg](screenshots/01-github-repository.jpg) - репозиторий проекта на GitHub.
2. [screenshots/02-project-tree.jpg](screenshots/02-project-tree.jpg) - структура локального проекта.
3. [screenshots/03-swagger-ui.jpg](screenshots/03-swagger-ui.jpg) - Swagger UI приложения.
4. [screenshots/04-docker-build.jpg](screenshots/04-docker-build.jpg) - сборка Docker-образа.
5. [screenshots/05-docker-container.jpg](screenshots/05-docker-container.jpg) - запущенный Docker-контейнер.
6. [screenshots/06-local-api-check.jpg](screenshots/06-local-api-check.jpg) - локальная проверка API.
7. [screenshots/07-docker-hub.jpg](screenshots/07-docker-hub.jpg) - опубликованный образ в Docker Hub.
8. [screenshots/08-terraform-apply-state-output.jpg](screenshots/08-terraform-apply-state-output.jpg) - `terraform apply`, `terraform state list`, `terraform output`.
9. [screenshots/09-openstack-instance.jpg](screenshots/09-openstack-instance.jpg) - виртуальная машина в OpenStack Dashboard.
10. [screenshots/10-openstack-api-check.jpg](screenshots/10-openstack-api-check.jpg) - проверка сервиса по Floating IP.
11. [screenshots/11-vm-docker-check.jpg](screenshots/11-vm-docker-check.jpg) - `docker ps` и `docker logs` на VM.
12. [screenshots/12-k8s-rollout-pods-service.jpg](screenshots/12-k8s-rollout-pods-service.jpg) - Kubernetes rollout, pod'ы, Service и endpoints.
13. [screenshots/13-k8s-port-forward-check.jpg](screenshots/13-k8s-port-forward-check.jpg) - проверка Kubernetes через `port-forward`.

## 13. Очистка ресурсов

Локальный Docker-контейнер:

```bash
docker rm -f workstation-audit
```

Ресурсы OpenStack, созданные Terraform:

```bash
cd terraform-openstack
terraform destroy
```

Ресурсы Kubernetes:

```bash
kubectl delete -f .\k8s\service.yaml --ignore-not-found=true
kubectl delete -f .\k8s\deployment.yaml --ignore-not-found=true
kubectl delete -f .\k8s\namespace.yaml --ignore-not-found=true
& "$env:TEMP\minikube-check\minikube-v1.34.0.exe" delete
```

## 14. Вывод

В ходе работы был создан учебный DevOps-проект для аудита защищенности рабочих
станций. Приложение на FastAPI реализует API для инвентаризации систем и отбора
рабочих станций, готовых к вводу в защищенный контур.

Проект подготовлен к:

- локальному запуску;
- контейнеризации через Docker;
- публикации в Docker Hub;
- развертыванию в OpenStack с помощью Terraform;
- запуску в Kubernetes / Minikube.

Краткий сценарий показа преподавателю вынесен в файл `DEFENSE.md`.

Важно: не хранить в GitHub пароли, токены, `clouds.yaml`, `.env`,
`terraform.tfstate` и приватные SSH-ключи. Файл `terraform.tfvars` также не
должен попадать в репозиторий, если содержит реальные данные OpenStack.
