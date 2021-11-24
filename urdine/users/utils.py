import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from urdine import mail


def save_picture(pic):
    random_hex = secrets.token_hex(8)
    _, ext_name = os.path.splitext(pic.filename)
    picture_name = random_hex + ext_name
    pic_path = os.path.join(current_app.root_path,
                            'static/images', picture_name)
    output_size = (200, 200)
    i = Image.open(pic)
    i.thumbnail(output_size)
    i.save(pic_path)
    return picture_name


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''
To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request, then ignore this email and no changes will be made.
    '''
    mail.send(msg)
