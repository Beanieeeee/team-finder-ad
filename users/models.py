from io import BytesIO
from random import choice

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def generate_avatar(self):
        colors = [
            "#B8D8D8",
            "#F4D06F",
            "#FFB997",
            "#CDB4DB",
            "#A8DADC",
            "#BDE0FE",
        ]

        image_size = 256
        background_color = choice(colors)
        letter = self.name[0].upper() if self.name else "U"

        image = Image.new("RGB", (image_size, image_size), background_color)
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except OSError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_position = (
            (image_size - text_width) / 2,
            (image_size - text_height) / 2 - 10,
        )

        draw.text(text_position, letter, fill="#FFFFFF", font=font)

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        file_name = f"avatar_{self.email}.png"

        self.avatar.save(
            file_name,
            ContentFile(buffer.getvalue()),
            save=False,
        )

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.generate_avatar()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email