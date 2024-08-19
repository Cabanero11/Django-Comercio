# Archivo .ps1 es powershell
# en vez de .sh
Start-Sleep -Seconds 10
python manage.py makemigrations
python manage.py migrate