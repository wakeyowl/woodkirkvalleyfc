# Woodkirk Valley FC Database

Holds all member data and digital club forms 

# Useful Commands
```
# Migrations
python manage.py makemigrations member
python manage.py migrate member

# fake migration if out of sync
python manage.py migrate member --fake

## Dump Export and Import from Database as JSON
python manage.py dumpdata > export28052017.json
python manage.py loaddata export28052017.json

## Backup the images for Kev (WGS Upload)
cd /home/wvfc/woodkirkvalleyfc/member/media
tar -zcvf profile_images.tar.gz profile_images