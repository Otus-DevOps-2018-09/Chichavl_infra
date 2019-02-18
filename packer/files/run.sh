#!/bin/bash
mv /home/appuser/puma.service /etc/systemd/system/
systemctl start puma.service 
systemctl enable puma.service 
