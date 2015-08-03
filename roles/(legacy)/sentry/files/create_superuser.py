import sys
sys.path.append('/etc/sentry')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf'

USERNAME, PASSWORD, EMAIL = sys.argv[1:]

def main():
    from django.contrib.auth import get_user_model
    User = get_user_model()

    super_user = User.objects.filter(username=USERNAME)

    if super_user:
        super_user = super_user[0]
        super_user.username = USERNAME
        super_user.password = PASSWORD
        super_user.email = EMAIL
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save()

        sys.exit(0)

    for user in User.objects.filter(is_superuser=True):
        user.delete(save=True)

    super_user = User.objects.create_user(
        username=USERNAME,
        password=PASSWORD,
        email=EMAIL,
    )
    super_user.is_staff = True
    super_user.is_superuser = True
    super_user.save()

    sys.exit(0)

main()
