# Pupils Bachelor OpenStack Service

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
│   └── .gitkeep
├── terraform-openstack/
│   ├── versions.tf
│   ├── variables.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── cloud-init.yaml
│   ├── terraform.tfvars.example
│   └── README.md
└── k8s/
    ├── namespace.yaml
    ├── deployment.yaml
    └── service.yaml
```

Основные файлы проекта:

- `app.py` - FastAPI-приложение;
- `requirements.txt` - зависимости Python;
- `Dockerfile` - инструкция сборки Docker-образа;
- `terraform-openstack/` - Terraform-конфигурация для OpenStack;
- `k8s/` - Kubernetes-манифесты;
- `DEFENSE.md` - краткий сценарий защиты и список скриншотов;
- `screenshots/` - каталог для скриншотов отчета.

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

Для локального запуска нужно создать виртуальное окружение, установить зависимости
и запустить приложение через Uvicorn.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

После запуска приложение будет доступно по адресам:

- `http://127.0.0.1:8000/`;
- `http://127.0.0.1:8000/docs`;
- `http://127.0.0.1:8000/health`.

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

После запуска контейнера сервис должен отвечать на порту `8000`.

Если локальный порт `8000` уже занят другим сервисом, можно пробросить контейнер
на порт `8001`:

```powershell
docker rm -f pupils-bachelor
docker run -d --name pupils-bachelor -p 8001:8000 pupils-bachelor-openstack-service
docker ps
curl.exe http://127.0.0.1:8001/health
curl.exe http://127.0.0.1:8001/bachelor
```

## 8. Публикация Docker-образа

Для развертывания через OpenStack VM и Kubernetes образ нужно опубликовать в
Docker Hub. Вместо `YOUR_DOCKERHUB_LOGIN` необходимо указать свой логин Docker Hub.

```bash
docker login
docker tag pupils-bachelor-openstack-service YOUR_DOCKERHUB_LOGIN/pupils-bachelor-openstack-service:v1
docker push YOUR_DOCKERHUB_LOGIN/pupils-bachelor-openstack-service:v1
```

После публикации этот образ используется в:

- `terraform-openstack/terraform.tfvars`;
- `k8s/deployment.yaml`.

## 9. Развертывание в OpenStack через Terraform

Terraform-конфигурация находится в каталоге `terraform-openstack/`.

Она создает:

- приватную сеть `pupils-network`;
- подсеть `pupils-subnet`;
- роутер `pupils-router`;
- подключение роутера к внешней сети `public`;
- Security Group `pupils-bachelor-sg`;
- правила для портов `22/tcp` и `8000/tcp`;
- исходящий трафик через стандартное egress-правило OpenStack;
- SSH keypair;
- сетевой порт для VM;
- виртуальную машину `pupils-bachelor-vm`;
- Floating IP;
- привязку Floating IP к VM;
- cloud-init запуск Docker-контейнера с приложением.

Перед запуском Terraform нужно подготовить OpenStack-профиль `myopenstack` в
`clouds.yaml`. Файл `clouds.yaml` должен храниться локально и не должен попадать
в GitHub. Имя пользователя в учебных примерах обозначается как `YOUR_USERNAME`.
Учетные данные OpenStack нужно брать из личного кабинета OpenStack или RC-файла,
выданного облачной платформой.

Проверить доступ к OpenStack можно так:

```bash
openstack --os-cloud myopenstack token issue
openstack --os-cloud myopenstack image list
openstack --os-cloud myopenstack flavor list
openstack --os-cloud myopenstack network list
```

В `terraform.tfvars` нужно указать учебные значения или значения своего облака.
Пример значений:

```hcl
os_cloud              = "myopenstack"
image_name            = "Ubuntu 22.04"
flavor_name           = "m1.small"
external_network_name = "public"
public_key_path       = "~/.ssh/id_ed25519.pub"
keypair_name          = "pupils-bachelor-key"
docker_image          = "YOUR_DOCKERHUB_LOGIN/pupils-bachelor-openstack-service:v1"
ssh_cidr              = "0.0.0.0/0"
app_cidr              = "0.0.0.0/0"
subnet_cidr           = "10.10.0.0/24"
dns_nameservers       = ["1.1.1.1", "8.8.8.8"]
```

Команды запуска Terraform:

```bash
cd terraform-openstack
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform validate
terraform plan
terraform apply
terraform output
```

После успешного выполнения Terraform выведет:

- `public_ip`;
- `service_url`;
- `health_url`;
- `ssh_command`.

## 10. Проверка работы сервиса в OpenStack

После создания ресурсов нужно взять Floating IP из `terraform output` или из
OpenStack Dashboard и выполнить проверки.

```bash
curl.exe http://<FLOATING_IP>:8000/health
curl.exe http://<FLOATING_IP>:8000/bachelor
ssh ubuntu@<FLOATING_IP>
sudo docker ps
sudo docker logs pupils-bachelor
```

Если `/health` возвращает `{"status":"ok"}`, приложение успешно запущено на VM.

## 11. Kubernetes / Minikube

В каталоге `k8s/` находятся Kubernetes-манифесты:

- `namespace.yaml` - namespace `pupils-bachelor`;
- `deployment.yaml` - Deployment на 2 реплики;
- `service.yaml` - NodePort Service на порту `30080`.

В текущей конфигурации `k8s/deployment.yaml` использует опубликованный образ
`xzxzxzxze/pupils-bachelor-openstack-service:v1`. При запуске из своего Docker Hub
аккаунта замените image на свой логин.

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

Сервис Kubernetes использует:

- `port: 8000`;
- `targetPort: 8000`;
- `nodePort: 30080`.

Для локальной проверки API через Kubernetes удобно использовать `port-forward`:

```powershell
kubectl port-forward -n pupils-bachelor service/pupils-bachelor-service 18080:8000
```

В другом окне PowerShell:

```powershell
curl.exe http://127.0.0.1:18080/health
curl.exe http://127.0.0.1:18080/bachelor
```

Если `kubectl port-forward` сообщает `timed out waiting for the condition`,
проверьте, что Deployment создан и Service имеет endpoints:

```powershell
kubectl get deployment -n pupils-bachelor
kubectl get pods -n pupils-bachelor
kubectl get endpoints -n pupils-bachelor
```

## 12. Скриншоты для отчета

Для отчета студент должен сделать и сохранить скриншоты в каталог `screenshots/`.
Минимальный набор скриншотов:

1. GitHub-репозиторий `nxnk88/pupils-bachelor-openstack-service` с файлами проекта.
2. `tree /F` в корне проекта.
3. Swagger UI `/docs` локального или OpenStack-сервиса.
4. Проверка `/health`: `curl.exe http://127.0.0.1:8001/health` или `curl.exe http://<FLOATING_IP>:8000/health`.
5. Проверка `/students`.
6. Проверка `/bachelor` с `total_candidates`.
7. Сборка Docker-образа: `docker build -t pupils-bachelor-openstack-service .`.
8. Запуск Docker-контейнера и `docker ps`.
9. Docker Hub с опубликованным образом `pupils-bachelor-openstack-service:v1`.
10. `terraform init`.
11. `terraform validate`.
12. `terraform plan` с планом создания ресурсов.
13. `terraform apply` с успешным завершением.
14. `terraform state list` со списком ресурсов OpenStack.
15. `terraform output` с `public_ip`, `service_url`, `health_url`, `ssh_command`.
16. VM `pupils-bachelor-vm` в OpenStack Dashboard.
17. Сеть `pupils-network`, подсеть `pupils-subnet` и роутер `pupils-router` в OpenStack Dashboard.
18. Security Group `pupils-bachelor-sg` с портами `22` и `8000`.
19. Floating IP, привязанный к VM.
20. Проверка сервиса по Floating IP: `/health` и `/bachelor`.
21. SSH-подключение к VM: `ssh ubuntu@<FLOATING_IP>`.
22. `sudo docker ps` и `sudo docker logs pupils-bachelor` на VM.
23. `kubectl get pods -n pupils-bachelor` с двумя pod'ами `Running`.
24. `kubectl get svc -n pupils-bachelor` с `NodePort`.
25. `kubectl get endpoints -n pupils-bachelor` с IP pod'ов.
26. Проверка Kubernetes через port-forward: `curl.exe http://127.0.0.1:18080/health` и `/bachelor`.

Краткий сценарий показа преподавателю вынесен в файл `DEFENSE.md`.

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

Важно: не храните в GitHub пароли, токены, `clouds.yaml`, `.env`,
`terraform.tfstate` и приватные SSH-ключи. Файл `terraform.tfvars` также не должен
попадать в репозиторий, если содержит реальные данные OpenStack или другие
персональные значения.
