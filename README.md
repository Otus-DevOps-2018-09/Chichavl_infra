# Chichavl_infra
Chichavl Infra repository
[![Build Status](https://travis-ci.org/Otus-DevOps-2018-02/Chichavl_infra.svg?branch=master)](https://travis-ci.org/Otus-DevOps-2018-02/Chichavl_infra)

# Подключение через bastion host

## Подключение одной командой
`ssh -i ~/.ssh/appuser -A appuser@104.155.36.168 'ssh -tt 10.128.0.2'` - используем ssh, чтобы запустить комманду ssh -tt 10.128.0.2 на бастион хосте, -tt нужны для корректного выделеления tty на внутреннем хосте
Но оно отдает душком и с ним есть проблема, команды сначала выводятся в консоль, потом выводится результат их исполнения
```
Last login: Tue Mar 13 21:22:36 2018 from 10.132.0.2
appuser@someinternalhost:~$ hostname
hostname
someinternalhost
appuser@someinternalhost:~$ ls -al
ls -al
total 32
drwxr-xr-x 4 appuser appuser 4096 Mar 13 22:21 .
drwxr-xr-x 5 root root 4096 Mar 13 22:16 ..
-rw------- 1 appuser appuser 16 Mar 13 22:21 .bash_history
-rw-r--r-- 1 appuser appuser 220 Aug 31 2015 .bash_logout
-rw-r--r-- 1 appuser appuser 3771 Aug 31 2015 .bashrc
drwx------ 2 appuser appuser 4096 Mar 13 11:15 .cache
-rw-r--r-- 1 appuser appuser 655 May 16 2017 .profile
drwx------ 2 appuser appuser 4096 Mar 13 11:10 .ssh
appuser@someinternalhost:~$
```
Не могу понять почему так происходит

И я бы решил первое задание также через ProxyCommand, как и второе, так как оно работает более ожидаемо и стабильно
`ssh -o ProxyCommand="ssh -W %h:%p appuser@104.155.36.168" appuser@10.128.0.2`

## Подключение через алиас
Добавляем пользователю конфиг ssh следующего содержания
```
$ cat ~/.ssh/config
Host internalhost
User appuser
Hostname 10.128.0.2 # internal host IP
ProxyCommand ssh -W %h:%p appuser@104.155.36.168 # Bastion external IP
```
После этого соединяемся командой `$ ssh internalhost` и попадаем сразу в консоль на внутренний хост, не имеющий доступа к интернету

bastion_IP = 104.155.36.168
someinternalhost_IP = 10.128.0.2

# Работа с gcloud
## Создание инстанса со startup-script
```
gcloud compute instances create reddit-app --boot-disk-size=10GB --image-family ubuntu-1604-lts --image-project=ubuntu-os-cloud --machine-type=g1-small --tags puma-server --restart-on-failure --metadata startup-script='wget -O - https://gist.githubusercontent.com/Chichavl/43179235635ac934b6780a03cbee1ec8/raw/34cdc303ffbeb8aff4362515318db599d8b72ec2/startup_script.sh | bash'
```
## Создание правила Firewall`а
```
gcloud compute --project=infra-197910 firewall-rules create default-puma-server --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:9292 --source-ranges=0.0.0.0/0 --target-tags=puma-server
```
testapp_IP = 35.189.216.200
testapp_port = 9292

# Terraform

## Добавление SSH ключей в метаданные проекта
Для добавления используем ресурс google_compute_project_metadata_item
```
resource "google_compute_project_metadata_item" "default" {
  key = "ssh-keys"
  value = "appuser:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDPidPiD0QVEH/SPgcTwdaPVbxniLQznseoDh33tk7dOKF31cl4+nQ7tAo/XEkAPQg82qYT6O4RyMJxzAgBokCv0kp+w9g7kZG/Pb8+fTi8/hSczn0+rN93VG4/LIkth0DLzSkhIBCZge1G/SA52bUbg2BLE61IaItl1OgNhNbv+Pw0JHmkEtDBoRLljajnjJ/L18kxdgZihtDXA0FlN/ttuItNtlBOrPTMQaoteIyiTS9Yy8a4MBESjy3tvFCZqt0+F6DC0vVvCLHOn5dXAF1mQNpYBgutDICUO/gczp/gB5GSllZRxo0zf/bXrBuojDpRp0wOI4nf2uSdfaVT7aaL appuser"
}
```
Если необходимо добавить несколько ключей, разделяем их символом переноса каретки `\n`
```
resource "google_compute_project_metadata_item" "default" {
  key = "ssh-keys"
  value = "appuser1:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDPidPiD0QVEH/SPgcTwdaPVbxniLQznseoDh33tk7dOKF31cl4+nQ7tAo/XEkAPQg82qYT6O4RyMJxzAgBokCv0kp+w9g7kZG/Pb8+fTi8/hSczn0+rN93VG4/LIkth0DLzSkhIBCZge1G/SA52bUbg2BLE61IaItl1OgNhNbv+Pw0JHmkEtDBoRLljajnjJ/L18kxdgZihtDXA0FlN/ttuItNtlBOrPTMQaoteIyiTS9Yy8a4MBESjy3tvFCZqt0+F6DC0vVvCLHOn5dXAF1mQNpYBgutDICUO/gczp/gB5GSllZRxo0zf/bXrBuojDpRp0wOI4nf2uSdfaVT7aaL appuser1\nappuser2:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDPidPiD0QVEH/SPgcTwdaPVbxniLQznseoDh33tk7dOKF31cl4+nQ7tAo/XEkAPQg82qYT6O4RyMJxzAgBokCv0kp+w9g7kZG/Pb8+fTi8/hSczn0+rN93VG4/LIkth0DLzSkhIBCZge1G/SA52bUbg2BLE61IaItl1OgNhNbv+Pw0JHmkEtDBoRLljajnjJ/L18kxdgZihtDXA0FlN/ttuItNtlBOrPTMQaoteIyiTS9Yy8a4MBESjy3tvFCZqt0+F6DC0vVvCLHOn5dXAF1mQNpYBgutDICUO/gczp/gB5GSllZRxo0zf/bXrBuojDpRp0wOI4nf2uSdfaVT7aaL appuser2\nappuser3:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDPidPiD0QVEH/SPgcTwdaPVbxniLQznseoDh33tk7dOKF31cl4+nQ7tAo/XEkAPQg82qYT6O4RyMJxzAgBokCv0kp+w9g7kZG/Pb8+fTi8/hSczn0+rN93VG4/LIkth0DLzSkhIBCZge1G/SA52bUbg2BLE61IaItl1OgNhNbv+Pw0JHmkEtDBoRLljajnjJ/L18kxdgZihtDXA0FlN/ttuItNtlBOrPTMQaoteIyiTS9Yy8a4MBESjy3tvFCZqt0+F6DC0vVvCLHOn5dXAF1mQNpYBgutDICUO/gczp/gB5GSllZRxo0zf/bXrBuojDpRp0wOI4nf2uSdfaVT7aaL appuser3"
}
```
Обратите внимание, terraform удалит ключи, добавленные не через него! 

## Балансировка нагрузки
Балансировка нагрузки в GCP происходит через 5 слоев абстракций:
- google_compute_global_forwarding_rule
- google_compute_target_http_proxy
- google_compute_url_map
- google_compute_backend_service
- google_compute_instance_group
Добавление хостов копированием нарушает принцип программирования DRY. Так же копирование часто приносит ошибки не изменненых переменных и чрезмерного разрастания кодовой базы.

## Хранение состояния на удаленном backend
Для хранения состояния нам необходим bucket, например на gcp.
```
terraform {
  backend "gcs" {
    bucket = "chichavl-storage-bucket"
    prefix = "terraform/state"
  }
}
```
После этого необходимо переинициализировать terraform коммандой `terraform init`, если все сделано верно, программа предложит перенести локальный файл состояния в облако.

## Работа приложения и БД на разных инстансах
Для решения этой задачи нужно:
- Разрешить Mongodb принимать входящие соединения со внешних интерфейсов
- Передать приложению адрес БД
Первую задачу решим копированием файла конфигурации с bind адресом 0.0.0.0. Вторую - шаблонизацией файла unit`а для systemd.

# Ansible
При выполнении плейбука clone.yml появились изменные объекты, так как в первый раз директория с копией репозитория от скриптов провиженинга была и ansible ничего не изменял на сервере.
Пример json инвентори:
```
{
            "app": {
                "hosts": ["appserver"],
                "vars": {
                    "ansible_host": "35.195.11.128"
                }
            },
            "db": {
                "hosts": ["dbserver"],
                "vars": {
                    "ansible_host": "35.190.218.246"
                }
            }
        }
```

## Dynamic inventory
Для решения задачи с динамическим инвентори расширил скрипт-заглушку из прошлого задания на чтение выходных переменных из файла terraform.tfstate.
Для использования достаточно поднять stage окружение и выполнить `ansible-playbook site.yml` в папке ansible.

## Что сделали
- Посмотрели на hanlder, шаблоны
- Использовали динамический инвентори из данных terraform
- Изменили provision packer на ansible
