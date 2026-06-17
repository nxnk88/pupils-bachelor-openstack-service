# Сценарий защиты проекта

Проект: `protected-workstation-audit-service`

GitHub: `https://github.com/nxnk88/pupils-bachelor-openstack-service`

## 1. Что сказать в начале

Это учебный DevOps-проект для аудита защищенности рабочих станций. Сервис
определяет, какие рабочие станции готовы к вводу в защищенный контур.

Проект показывает полный цикл:

- разработка API на FastAPI;
- обработка данных рабочих станций через pandas;
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

- `app.py` - FastAPI-приложение и логика аудита;
- `Dockerfile` - сборка Docker-образа;
- `terraform-openstack/` - инфраструктура OpenStack;
- `k8s/` - Kubernetes-манифесты;
- `README.md` - отчет;
- `DEFENSE.md` - сценарий защиты.

## 3. Локальная проверка Docker

```powershell
cd C:\Users\bob\Documents\sharay

docker build -t protected-workstation-audit-service .
docker rm -f workstation-audit
docker run -d --name workstation-audit -p 8001:8000 protected-workstation-audit-service

docker ps
curl.exe http://127.0.0.1:8001/health
curl.exe http://127.0.0.1:8001/audit-ready
```

Что говорить:

Контейнер внутри слушает порт `8000`, а наружу на локальной машине используется
порт `8001`. Если `/health` возвращает `{"status":"ok"}`, приложение запущено.
Если `/audit-ready` возвращает список готовых рабочих станций, работает
бизнес-логика сервиса.

## 4. Docker Hub

```powershell
docker tag protected-workstation-audit-service YOUR_DOCKERHUB_LOGIN/protected-workstation-audit-service:v1
docker push YOUR_DOCKERHUB_LOGIN/protected-workstation-audit-service:v1
```

Что говорить:

Один и тот же Docker-образ используется в двух средах: в OpenStack VM через
cloud-init и в Kubernetes Deployment.

## 5. OpenStack через Terraform

```powershell
cd C:\Users\bob\Documents\sharay\terraform-openstack

.\terraform-init.ps1
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

Terraform создает сеть `workstation-audit-network`, подсеть
`workstation-audit-subnet`, роутер `workstation-audit-router`, security group
`workstation-audit-sg`, SSH keypair, сетевой порт, VM
`workstation-audit-vm`, Floating IP и привязку Floating IP к VM. Через
`cloud-init` на VM устанавливается Docker и запускается контейнер
`workstation-audit`.

Проверка сервиса в OpenStack:

```powershell
curl.exe http://<FLOATING_IP>:8000/health
curl.exe http://<FLOATING_IP>:8000/audit-ready
```

## 6. Проверка VM по SSH

```powershell
ssh ubuntu@<FLOATING_IP>
sudo docker ps
sudo docker logs workstation-audit
```

Что говорить:

Эта проверка показывает, что на виртуальной машине действительно работает
Docker-контейнер с приложением.

## 7. Kubernetes / Minikube

```powershell
cd C:\Users\bob\Documents\sharay

& "$env:TEMP\minikube-check\minikube-v1.34.0.exe" start --driver=docker --container-runtime=docker

kubectl apply -f .\k8s\namespace.yaml
kubectl apply -f .\k8s\deployment.yaml
kubectl apply -f .\k8s\service.yaml

kubectl rollout status deployment/workstation-audit-deployment -n workstation-audit
kubectl get pods -n workstation-audit
kubectl get svc -n workstation-audit
kubectl get endpoints -n workstation-audit
```

Что говорить:

Deployment запускает две реплики приложения. Service типа `NodePort` направляет
трафик на pod'ы. Команда `kubectl get endpoints` подтверждает, что service
связан с работающими pod'ами.

Проверка через port-forward:

```powershell
kubectl port-forward -n workstation-audit service/workstation-audit-service 18080:8000
```

В другом окне PowerShell:

```powershell
curl.exe http://127.0.0.1:18080/health
curl.exe http://127.0.0.1:18080/audit-ready
```

## 8. Что показать в OpenStack Dashboard

- VM `workstation-audit-vm`;
- сеть `workstation-audit-network`;
- подсеть `workstation-audit-subnet`;
- роутер `workstation-audit-router`;
- security group `workstation-audit-sg`;
- правила security group для портов `22` и `8000`;
- Floating IP, привязанный к VM.

## 9. Как объяснить предметную логику

В сервисе хранится набор рабочих станций. Для каждой станции есть:

- имя хоста;
- подразделение;
- оценка защищенности;
- признак включенного антивируса;
- признак шифрования диска.

Рабочая станция считается готовой к вводу в защищенный контур, если:

- `hardening_score >= 85`;
- антивирус включен;
- шифрование диска включено.

## 10. Важное замечание по скриншотам

Скриншоты в отчете сохранены как иллюстрации этапов технологического контура
Docker, Terraform, OpenStack и Kubernetes. Они показывают реальную
последовательность разворачивания и проверки, поэтому в отдельных архивных
изображениях могут встречаться старые технические имена.

## 11. Очистка ресурсов

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
docker rm -f workstation-audit
```
