from django.contrib.auth.models import User


def get_login_data_formate(data):
    data = {
        "username": data.get('username', None),
        "password": data.get('password', None)
    }

    return data


def get_user_data(data):


    data = {
        'user':{
            "username": data['username'],
            "password": data['password'],
            'email': data['email'],
        },
        'type':data.get('type',1),
        'password':data['password'],
        'confirm_password':data['confirm_password']
    }

    return data

def set_user_active(data):
    user = User.objects.get(id=data['id'])

    if user.is_active == True:
        user.info.status = 1
        user.info.save()
        return True
    else:
        return False
