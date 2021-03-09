import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)   #creates a unique filename so no duplicates exist between users
    _, ext = os.path.splitext(form_picture.filename)    #decomposes output of os.path into filename and file ext
    picture_filename = random_hex + ext #new filename with ext
    picture_path = os.path.join(current_app.root_path, 'static','profile_pictures', picture_filename) #joins the path to where image will be saved
    
    #Resizing our picture 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) #actually saving image to location
    return picture_filename

def send_reset_email(user):
    reset_token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender='noreply@demo.com', 
                    recipients = [user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=reset_token, _external = True)}
If you did not make this request, then just ignore this email :((
    '''
    mail.send(msg)