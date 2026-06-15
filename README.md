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
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/students
curl http://127.0.0.1:8000/bachelor
```

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
curl http://127.0.0.1:8000/health
docker rm -f pupils-bachelor
```

После запуска контейнера сервис должен отвечать на порту `8000`.

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
curl http://<FLOATING_IP>:8000/health
curl http://<FLOATING_IP>:8000/bachelor
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

```bash
minikube start
kubectl apply -f k8s/
kubectl get pods -n pupils-bachelor
kubectl get svc -n pupils-bachelor
minikube service pupils-bachelor-service -n pupils-bachelor
```

Сервис Kubernetes использует:

- `port: 8000`;
- `targetPort: 8000`;
- `nodePort: 30080`.

## 12. Скриншоты для отчета

Для отчета студент должен сделать и сохранить скриншоты в каталог `screenshots/`:

1. GitHub-репозиторий.
2. Локальный запуск FastAPI.
3. Swagger UI `/docs`.
4. Проверка `/health`.
5. Проверка `/students`.
6. Проверка `/bachelor`.
7. Сборка Docker-образа.
8. Запуск Docker-контейнера.
9. Docker Hub с опубликованным образом.
10. `terraform init`.
11. `terraform plan`.
12. `terraform apply`.
13. VM в OpenStack Dashboard.
14. Security Group в OpenStack.
15. Floating IP.
16. Проверка сервиса по Floating IP.
17. SSH-подключение к VM.
18. `docker ps` на VM.
19. `kubectl get pods`.
20. `kubectl get svc`.

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
kubectl delete -f k8s/
minikube stop
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
