# Terraform OpenStack

Эта конфигурация создает инфраструктуру OpenStack для сервиса
`pupils-bachelor-openstack-service`: приватную сеть, подсеть, роутер,
Security Group, SSH keypair, порт VM, виртуальную машину, Floating IP и запуск
Docker-контейнера через cloud-init.

## 1. Подготовка clouds.yaml

Создайте файл `clouds.yaml` с профилем `myopenstack` в одном из стандартных мест:

- `~/.config/openstack/clouds.yaml`;
- текущий каталог запуска Terraform;
- путь из переменной окружения `OS_CLIENT_CONFIG_FILE`.

Пример структуры:

```yaml
clouds:
  myopenstack:
    auth:
      auth_url: https://openstack.example.com:5000/v3
      username: YOUR_USERNAME
      project_name: YOUR_USERNAME
      user_domain_name: Default
      project_domain_name: Default
    region_name: RegionOne
    interface: public
    identity_api_version: 3
```

## 2. Проверка OpenStack CLI

```bash
openstack --os-cloud myopenstack token issue
openstack --os-cloud myopenstack image list
openstack --os-cloud myopenstack flavor list
openstack --os-cloud myopenstack network list
```

Убедитесь, что нужные image, flavor и external network существуют.

## 3. Подготовка переменных

```bash
cp terraform.tfvars.example terraform.tfvars
```

Отредактируйте `terraform.tfvars`: укажите реальные значения `image_name`,
`flavor_name`, `external_network_name` и `docker_image`. Если OpenStack API
медленно отдает список flavor, можно дополнительно указать `flavor_id`.
Для корректной установки пакетов через cloud-init подсеть также задает DNS
серверы через `dns_nameservers`.

## 4. Запуск Terraform

```bash
terraform init
terraform validate
terraform plan
terraform apply
terraform state list
terraform output
```

После выполнения Terraform выведет `public_ip`, `service_url`, `health_url` и
`ssh_command`.

## 5. Проверка приложения

```bash
curl.exe http://<FLOATING_IP>:8000/health
curl.exe http://<FLOATING_IP>:8000/bachelor
```

В PowerShell лучше использовать `curl.exe`, чтобы не попасть в псевдоним
`Invoke-WebRequest`.

## 6. Удаление ресурсов

```bash
terraform destroy
```
