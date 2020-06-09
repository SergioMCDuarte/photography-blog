import os
from PIL import Image
#from flask import url_for, current_app
from datetime import datetime
from werkzeug.security import hashlib

def add_photo(photo_upload):
    filename = photo_upload.filename
    ext_type = filename.split('.')[-1]
    storage_file_name = '{}.{}'\
                            .format(
                            hashlib.md5(filename.split('.')[0].encode('utf-8')).hexdigest(),
                            ext_type
                            )
    image_path = os.path.join(
        os.path.abspath('static'),
        'img',
        storage_file_name
    )

    thumbnail_path = os.path.join(
        os.path.abspath('static'),
        'img/thumbnail',
        storage_file_name
    )

    pic = Image.open(photo_upload)
    pic.save(image_path)  # original image
    outputsize = (200,200)
    pic.thumbnail(outputsize)
    pic.save(thumbnail_path)  # thumbnail for index page

    return storage_file_name
