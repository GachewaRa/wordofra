from django.contrib.auth import get_user_model

User = get_user_model()

username = "Ra"  # Change as needed
email = "gachewaadrian@gmail.com"  # Change as needed
password = "SuperScribe#001"  # Change as needed

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
