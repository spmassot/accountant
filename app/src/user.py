from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, JSONAttribute


class User(Model):
    class Meta:
        table_name = 'voxx-users'
        region = 'us-east-1'
        read_capacity_units = 1
        write_capacity_units = 1

    username = UnicodeAttribute(hash_key=True)
    password = UnicodeAttribute()


def is_valid_user(username):
    if User.get(username):
        return True
    else:
        return False


def is_valid_login(username, password):
    try:
        user = User.get(username)
        if user.password == password:
            return True
    except User.DoesNotExist as e:
        pass
    except:
        pass
    return False


def initialize_users():
    if not User.exists():
        User.create_table()
