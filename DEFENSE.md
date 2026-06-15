# Сценарий защиты проекта

Проект: `pupils-bachelor-openstack-service`

GitHub: `https://github.com/nxnk88/pupils-bachelor-openstack-service`

## 1. Что сказать в начале

Это учебный DevOps-проект. В нем реализован FastAPI-сервис для определения
студентов, которые могут стать бакалаврами в области защищенных
автоматизированных систем.

Проект показывает полный цикл:

- разработка API на FastAPI;
- обработка данных студентов через pandas;
- сборка Docker-образа;
- публикация образа в Docker Hub;
- развертывание инфраструктуры OpenStack через Terraform;
- запуск контейнера на VM через cloud-init;
- развертывание приложения в Kubernetes через Minikube.

## 2. Что показать в репозитории

```powershell
cd C:\Users\bob\Documents\sharay
tree /F
git remote -v
```

Что говорить:

- `app.py` - FastAPI-приложение и бизнес-логика;
- `Dockerfile` - сборка Docker-образа;
- `terraform-openstack/` - инфраструктура OpenStack;
- `k8s/` - Kubernetes-манифесты;
- `README.md` - отчет;
- `DEFENSE.md` - сценарий защиты.

## 3. Локальная проверка Docker

На этой машине порт `8000` может быть занят другим сервисом, поэтому для
локальной демонстрации используется внешний порт `8001`.

```powershell
cd C:\Users\bob\Documents\sharay

docker build -t pupils-bachelor-openstack-service .
docker rm -f pupils-bachelor
docker run -d --name pupils-bachelor -p 8001:8000 pupils-bachelor-openstack-service

docker ps
curl.exe http://127.0.0.1:8001/health
curl.exe http://127.0.0.1:8001/bachelor
```

Что говорить:

Контейнер внутри слушает порт `8000`, а наружу на локальной машине проброшен
порт `8001`. Если `/health` возвращает `{"status":"ok"}`, приложение запущено.
Если `/bachelor` возвращает `total_candidates`, работает бизнес-логика.

## 4. Docker Hub

```powershell
docker tag pupils-bachelor-openstack-service xzxzxzxze/pupils-bachelor-openstack-service:v1
docker push xzxzxzxze/pupils-bachelor-openstack-service:v1
```

Что говорить:

Один и тот же Docker-образ используется в двух средах: в OpenStack VM через
cloud-init и в Kubernetes Deployment.

## 5. OpenStack через Terraform

```powershell
cd C:\Users\bob\Documents\sharay\terraform-openstack

terraform init
terraform validate
terraform plan
terraform apply
```

На вопрос Terraform нужно ввести:

```text
yes
```

Показать, что все создалось:

```powershell
terraform state list
terraform output
```

Что говорить:

Terraform создает сеть `pupils-network`, подсеть `pupils-subnet`, роутер
`pupils-router`, security group `pupils-bachelor-sg`, SSH keypair, сетевой порт,
VM `pupils-bachelor-vm`, Floating IP и привязку Floating IP к VM. Через
`cloud-init` на VM устанавливается Docker и запускается контейнер
`pupils-bachelor`.

Проверка сервиса в OpenStack:

```powershell
curl.exe http://<FLOATING_IP>:8000/health
curl.exe http://<FLOATING_IP>:8000/bachelor
```

`<FLOATING_IP>` нужно взять из `terraform output`.

## 6. Проверка VM по SSH

```powershell
ssh ubuntu@<FLOATING_IP>
sudo docker ps
sudo docker logs pupils-bachelor
```

Что говорить:

Эта проверка показывает, что на виртуальной машине действительно работает
Docker-контейнер с приложением.

## 7. Kubernetes / Minikube

Важно применять манифесты по одному, чтобы namespace точно был создан до
Deployment и Service.

```powershell
cd C:\Users\bob\Documents\sharay

& "$env:TEMP\minikube-check\minikube-v1.34.0.exe" start --driver=docker --container-runtime=docker

kubectl apply -f .\k8s\namespace.yaml
kubectl apply -f .\k8s\deployment.yaml
kubectl apply -f .\k8s\service.yaml

kubectl rollout status deployment/pupils-bachelor-deployment -n pupils-bachelor
kubectl get pods -n pupils-bachelor
kubectl get svc -n pupils-bachelor
kubectl get endpoints -n pupils-bachelor
```

Что говорить:

Deployment запускает две реплики приложения. Service типа `NodePort` направляет
трафик на pod'ы. Команда `kubectl get endpoints` подтверждает, что service
действительно связан с работающими pod'ами.

Проверка через port-forward:

```powershell
kubectl port-forward -n pupils-bachelor service/pupils-bachelor-service 18080:8000
```

В другом окне PowerShell:

```powershell
curl.exe http://127.0.0.1:18080/health
curl.exe http://127.0.0.1:18080/bachelor
```

## 8. Что показать в OpenStack Dashboard

- VM `pupils-bachelor-vm`;
- сеть `pupils-network`;
- подсеть `pupils-subnet`;
- роутер `pupils-router`;
- security group `pupils-bachelor-sg`;
- правила security group для портов `22` и `8000`;
- Floating IP, привязанный к VM.

## 9. Какие скриншоты сделать

1. GitHub-репозиторий с файлами проекта.
2. `tree /F` в корне проекта.
3. Swagger UI `/docs`.
4. `curl.exe http://127.0.0.1:8001/health`.
5. `curl.exe http://127.0.0.1:8001/bachelor`.
6. `docker build -t pupils-bachelor-openstack-service .`.
7. `docker ps` с контейнером `pupils-bachelor`.
8. Docker Hub с образом `pupils-bachelor-openstack-service:v1`.
9. `terraform init`.
10. `terraform validate`.
11. `terraform plan`.
12. `terraform apply`.
13. `terraform state list`.
14. `terraform output`.
15. VM в OpenStack Dashboard.
16. Network/Subnet/Router в OpenStack Dashboard.
17. Security Group с портами `22` и `8000`.
18. Floating IP.
19. `curl.exe http://<FLOATING_IP>:8000/health`.
20. `curl.exe http://<FLOATING_IP>:8000/bachelor`.
21. SSH на VM.
22. `sudo docker ps` на VM.
23. `sudo docker logs pupils-bachelor` на VM.
24. `kubectl get pods -n pupils-bachelor`.
25. `kubectl get svc -n pupils-bachelor`.
26. `kubectl get endpoints -n pupils-bachelor`.
27. Проверка Kubernetes через `curl.exe http://127.0.0.1:18080/health`.
28. Проверка Kubernetes через `curl.exe http://127.0.0.1:18080/bachelor`.

## 10. Очистка ресурсов

OpenStack:

```powershell
cd C:\Users\bob\Documents\sharay\terraform-openstack
terraform destroy
```

Kubernetes и локальный Docker:

```powershell
cd C:\Users\bob\Documents\sharay
kubectl delete -f .\k8s\service.yaml --ignore-not-found=true
kubectl delete -f .\k8s\deployment.yaml --ignore-not-found=true
kubectl delete -f .\k8s\namespace.yaml --ignore-not-found=true
& "$env:TEMP\minikube-check\minikube-v1.34.0.exe" delete
docker rm -f pupils-bachelor
```

## 11. Финальная фраза

В результате один FastAPI-сервис проходит полный DevOps-цикл: код приложения,
Docker-образ, публикация образа, инфраструктура OpenStack через Terraform,
автоматический запуск контейнера на VM и Kubernetes-развертывание в Minikube.
