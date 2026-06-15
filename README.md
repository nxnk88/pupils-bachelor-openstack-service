# Отчет по дисциплине
"Технология проектирования автоматизированных систем в защищенном исполнении"

## Тема работы

Разработка и деплой веб-сервиса для определения кандидатов на степень бакалавра

## Студент

`gofman03`

## Дата выполнения

`15.06.2026`

## Название проекта

`pupils-bachelor-openstack-service`

## 1. Цель работы

Цель работы - разработать учебный DevOps-проект `pupils-bachelor-openstack-service`,
который демонстрирует полный цикл подготовки приложения к запуску:

- создание REST API на FastAPI;
- обработка данных студентов с помощью pandas;
- упаковка приложения в Docker-образ;
- публикация Docker-образа в Docker Hub;
- описание инфраструктуры OpenStack через Terraform;
- запуск приложения на виртуальной машине через cloud-init;
- подготовка Kubernetes-манифестов для запуска в Minikube.

## 2. Описание проекта

Проект представляет собой FastAPI-сервис для определения студентов, которые могут
стать бакалаврами в области защищенных автоматизированных систем.

В приложении создан тестовый набор студентов. Для каждого студента хранятся поля:

- `name` - имя студента;
- `specialization` - специализация;
- `grade` - оценка;
- `course` - курс.

Кандидатами на получение бакалавра считаются студенты, у которых:

- `grade >= 4`;
- `course >= 3`.

Эндпоинт `/bachelor` возвращает сообщение:

```text
Я стану бакалавром в области защищенных автоматизированных систем
```

Также он возвращает количество кандидатов, распределение по специализациям и
полный список подходящих студентов.

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

## 4. Структура репозитория

Репозиторий проекта опубликован на GitHub и содержит все основные файлы
приложения, инфраструктуры и материалов для защиты.

![Рисунок 1. Репозиторий проекта на GitHub](screenshots/01-github-repository.jpg)
*Рисунок 1. Репозиторий `nxnk88/pupils-bachelor-openstack-service` на GitHub.*

Структура локального проекта выглядит следующим образом:

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
*Рисунок 2. Вывод `tree /F` в корне проекта.*

Основные файлы проекта:

- `app.py` - FastAPI-приложение;
- `requirements.txt` - зависимости Python;
- `Dockerfile` - инструкция сборки Docker-образа;
- `terraform-openstack/` - Terraform-конфигурация для OpenStack;
- `k8s/` - Kubernetes-манифесты;
- `DEFENSE.md` - краткий сценарий защиты;
- `screenshots/` - каталог со скриншотами для отчета.

## 5. Описание API

| Метод | Путь | Назначение |
| --- | --- | --- |
| `GET` | `/` | Главная страница сервиса |
| `GET` | `/health` | Проверка состояния приложения |
| `GET` | `/students` | Получение списка всех студентов |
| `GET` | `/students?specialization=...` | Фильтрация студентов по специализации |
| `GET` | `/student/{name}` | Поиск студента по имени |
| `GET` | `/bachelor` | Получение списка кандидатов на бакалавра |

Если студент найден через `/student/{name}`, сервис возвращает его данные. Если
студент не найден, возвращается HTTP-ответ `404`.

Пример проверки API:

```bash
curl.exe http://127.0.0.1:8000/
curl.exe http://127.0.0.1:8000/health
curl.exe http://127.0.0.1:8000/students
curl.exe http://127.0.0.1:8000/bachelor
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
*Рисунок 3. Интерфейс Swagger UI по адресу `/docs`.*

## 7. Docker

Docker используется для упаковки FastAPI-приложения в переносимый контейнер.

```bash
docker build -t pupils-bachelor-openstack-service .
docker run -d --name pupils-bachelor -p 8000:8000 pupils-bachelor-openstack-service
docker ps
curl.exe http://127.0.0.1:8000/health
curl.exe http://127.0.0.1:8000/bachelor
docker rm -f pupils-bachelor
```

На локальной машине порт `8000` уже был занят другим сервисом, поэтому для
демонстрации использовался внешний порт `8001`.

```powershell
docker rm -f pupils-bachelor
docker run -d --name pupils-bachelor -p 8001:8000 pupils-bachelor-openstack-service
docker ps
curl.exe http://127.0.0.1:8001/health
curl.exe http://127.0.0.1:8001/bachelor
```

![Рисунок 4. Сборка Docker-образа](screenshots/04-docker-build.jpg)
*Рисунок 4. Сборка Docker-образа `pupils-bachelor-openstack-service`.*

![Рисунок 5. Запуск контейнера Docker](screenshots/05-docker-container.jpg)
*Рисунок 5. Контейнер `pupils-bachelor` запущен и слушает порт `8001`.*

![Рисунок 6. Проверка API локального контейнера](screenshots/06-local-api-check.jpg)
*Рисунок 6. Проверка `/health` и `/bachelor` для локального Docker-контейнера.*

## 8. Публикация Docker-образа

Для развертывания через OpenStack VM и Kubernetes образ был опубликован в Docker
Hub.

```bash
docker login
docker tag pupils-bachelor-openstack-service YOUR_DOCKERHUB_LOGIN/pupils-bachelor-openstack-service:v1
docker push YOUR_DOCKERHUB_LOGIN/pupils-bachelor-openstack-service:v1
```

В текущем проекте используется образ:

```text
xzxzxzxze/pupils-bachelor-openstack-service:v1
```

![Рисунок 7. Docker Hub с опубликованным образом](screenshots/07-docker-hub.jpg)
*Рисунок 7. Репозиторий Docker Hub с опубликованным образом проекта.*

После публикации этот образ используется в:

- `terraform-openstack/terraform.tfvars`;
- `k8s/deployment.yaml`.

## 9. Развертывание в OpenStack через Terraform

Terraform-конфигурация находится в каталоге `terraform-openstack/`.

Она создает:

- приватную сеть `pupils-network`;
- подсеть `pupils-subnet`;
- роутер `pupils-router`;
- подключение роутера к внешней сети;
- Security Group `pupils-bachelor-sg`;
- правила для портов `22/tcp` и `8000/tcp`;
- SSH keypair;
- сетевой порт для VM;
- виртуальную машину `pupils-bachelor-vm`;
- Floating IP;
- привязку Floating IP к VM;
- cloud-init для установки Docker и запуска контейнера.

Команды запуска Terraform:

```bash
cd terraform-openstack
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform validate
terraform plan
terraform apply
terraform state list
terraform output
```

После успешного выполнения Terraform были выведены:

- `public_ip`;
- `service_url`;
- `health_url`;
- `ssh_command`.

![Рисунок 8. Terraform apply, state list и output](screenshots/08-terraform-apply-state-output.jpg)
*Рисунок 8. Успешное выполнение `terraform apply`, список ресурсов и outputs.*

## 10. Проверка работы сервиса в OpenStack

После создания ресурсов сервис был проверен по Floating IP.

```bash
curl.exe http://<FLOATING_IP>:8000/health
curl.exe http://<FLOATING_IP>:8000/bachelor
ssh ubuntu@<FLOATING_IP>
sudo docker ps
sudo docker logs pupils-bachelor
```

В OpenStack Dashboard видно, что виртуальная машина `pupils-bachelor-vm`
создана, активна и получила внутренний и внешний IP-адреса.

![Рисунок 9. Виртуальная машина в OpenStack](screenshots/09-openstack-instance.jpg)
*Рисунок 9. Инстанс `pupils-bachelor-vm` в OpenStack Dashboard.*

Проверка по Floating IP показывает, что `/health` возвращает статус `ok`, а
`/bachelor` отдает корректный список кандидатов.

![Рисунок 10. Проверка сервиса по Floating IP](screenshots/10-openstack-api-check.jpg)
*Рисунок 10. Проверка `/health` и `/bachelor` на развернутом OpenStack-сервисе.*

Дополнительная проверка по SSH подтверждает, что на виртуальной машине работает
Docker-контейнер `pupils-bachelor`.

![Рисунок 11. Проверка контейнера на VM](screenshots/11-vm-docker-check.jpg)
*Рисунок 11. Вывод `sudo docker ps` и `sudo docker logs pupils-bachelor` на VM.*

## 11. Kubernetes / Minikube

В каталоге `k8s/` находятся Kubernetes-манифесты:

- `namespace.yaml` - namespace `pupils-bachelor`;
- `deployment.yaml` - Deployment на 2 реплики;
- `service.yaml` - NodePort Service на порту `30080`.

Для корректного развертывания манифесты применялись по отдельности в правильном
порядке:

```powershell
& "$env:TEMP\minikube-check\minikube-v1.34.0.exe" start --driver=docker --container-runtime=docker
kubectl apply -f .\k8s\namespace.yaml
kubectl apply -f .\k8s\deployment.yaml
kubectl apply -f .\k8s\service.yaml
kubectl rollout status deployment/pupils-bachelor-deployment -n pupils-bachelor
kubectl get pods -n pupils-bachelor
kubectl get svc -n pupils-bachelor
kubectl get endpoints -n pupils-bachelor
```

Результат развертывания показывает, что Deployment успешно раскатился, два pod'а
перешли в состояние `Running`, а Service получил endpoints.

![Рисунок 12. Развертывание в Kubernetes](screenshots/12-k8s-rollout-pods-service.jpg)
*Рисунок 12. Rollout Deployment, список pod'ов, Service и endpoints в Kubernetes.*

Для локальной проверки API через Kubernetes использовался `port-forward`.

```powershell
kubectl port-forward -n pupils-bachelor service/pupils-bachelor-service 18080:8000
```

В другом окне PowerShell:

```powershell
curl.exe http://127.0.0.1:18080/health
curl.exe http://127.0.0.1:18080/bachelor
```

![Рисунок 13. Проверка Kubernetes через port-forward](screenshots/13-k8s-port-forward-check.jpg)
*Рисунок 13. Проверка `/health` и `/bachelor` через `kubectl port-forward`.*

## 12. Скриншоты, включенные в отчет

В отчет включены следующие подтверждающие материалы:

1. [screenshots/01-github-repository.jpg](screenshots/01-github-repository.jpg) - репозиторий проекта на GitHub.
2. [screenshots/02-project-tree.jpg](screenshots/02-project-tree.jpg) - структура локального проекта.
3. [screenshots/03-swagger-ui.jpg](screenshots/03-swagger-ui.jpg) - Swagger UI FastAPI.
4. [screenshots/04-docker-build.jpg](screenshots/04-docker-build.jpg) - сборка Docker-образа.
5. [screenshots/05-docker-container.jpg](screenshots/05-docker-container.jpg) - работающий Docker-контейнер.
6. [screenshots/06-local-api-check.jpg](screenshots/06-local-api-check.jpg) - локальная проверка `/health` и `/bachelor`.
7. [screenshots/07-docker-hub.jpg](screenshots/07-docker-hub.jpg) - опубликованный образ в Docker Hub.
8. [screenshots/08-terraform-apply-state-output.jpg](screenshots/08-terraform-apply-state-output.jpg) - `terraform apply`, `terraform state list`, `terraform output`.
9. [screenshots/09-openstack-instance.jpg](screenshots/09-openstack-instance.jpg) - виртуальная машина в OpenStack Dashboard.
10. [screenshots/10-openstack-api-check.jpg](screenshots/10-openstack-api-check.jpg) - проверка сервиса по Floating IP.
11. [screenshots/11-vm-docker-check.jpg](screenshots/11-vm-docker-check.jpg) - `docker ps` и `docker logs` на VM.
12. [screenshots/12-k8s-rollout-pods-service.jpg](screenshots/12-k8s-rollout-pods-service.jpg) - Kubernetes rollout, pod'ы, service и endpoints.
13. [screenshots/13-k8s-port-forward-check.jpg](screenshots/13-k8s-port-forward-check.jpg) - проверка Kubernetes через `port-forward`.

## 13. Очистка ресурсов

Локальный Docker-контейнер:

```bash
docker rm -f pupils-bachelor
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

После удаления ресурсов рекомендуется проверить, что в OpenStack не остались
виртуальные машины, Floating IP, роутеры, сети и Security Group, созданные в
рамках этой работы.

## 14. Вывод

В ходе работы был создан самодостаточный учебный DevOps-проект. Приложение на
FastAPI реализует API для работы со студентами и отбора кандидатов на получение
бакалавра. Проект подготовлен к локальному запуску, контейнеризации через Docker,
публикации в Docker Hub, развертыванию в OpenStack с помощью Terraform и запуску
в Kubernetes / Minikube.

По итогам выполнения работы были подтверждены все основные этапы:

- разработка веб-сервиса на FastAPI;
- сборка и запуск Docker-контейнера;
- публикация образа в Docker Hub;
- автоматическое создание инфраструктуры в OpenStack через Terraform;
- запуск контейнера на VM через cloud-init;
- развертывание приложения в Kubernetes и проверка его доступности.

Краткий сценарий показа преподавателю вынесен в файл `DEFENSE.md`.

Важно: не хранить в GitHub пароли, токены, `clouds.yaml`, `.env`,
`terraform.tfstate` и приватные SSH-ключи. Файл `terraform.tfvars` также не
должен попадать в репозиторий, если содержит реальные данные OpenStack.
