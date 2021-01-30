#! /bin/bash
cd api && celery -A app worker -B 
