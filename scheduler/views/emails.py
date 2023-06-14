from django.core.mail import send_mail


def send_password_create_email(type, user_email, username, password):
    subject = 'Bienvenu'
    message = f"Votre nouveau compte de type :{type} :\n nom d'utilisateur: {username}.\n mot de passe: {password}\n ceci est un message automatique, merci de ne pas répondre"
    from_email = 'akliyalaoui16@gmail.com'  # your Gmail email address
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)


def send_password_update_email(first_name, user_email, username, password):
    subject = 'Mot de passe modifié'
    message = f"Bonjour {first_name}, \n Votre nouveau nom d'utilisateur: {username} \nVotre nouveau mot de passe : {password}\n ceci est un message automatique, merci de ne pas répondre"
    from_email = 'akliyalaoui16@gmail.com'  # your Gmail email address
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)