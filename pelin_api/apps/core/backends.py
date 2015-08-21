from apps.core.models import User, Student, Teacher


class CustomAuthBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            try:
                usr = User.objects.get(email=username)
                if usr.check_password(password):
                    return usr
            except User.DoesNotExist:
                pass

        try:
            usr = Teacher.objects.get(username=username)
            usr = usr.user
            if usr.check_password(password):
                return usr
        except Teacher.DoesNotExist:
            try:
                usr = Student.objects.get(nim=username)
                usr = usr.user
                if usr.check_password(password):
                    return usr
            except Student.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None