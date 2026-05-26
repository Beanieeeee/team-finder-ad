from io import BytesIO
from random import choice
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.forms import ValidationError
from PIL import Image, ImageDraw, ImageFont


PHONE_LENGTH_WITH_EIGHT = 11
PHONE_LENGTH_WITH_PLUS = 12
AVATAR_SIZE = 256
AVATAR_FONT_SIZE = 120
AVATAR_VERTICAL_OFFSET = 10
DEFAULT_AVATAR_LETTER = "U"
GITHUB_HOSTS = ("github.com", "www.github.com")
AVATAR_COLORS = (
    "#B8D8D8",
    "#F4D06F",
    "#FFB997",
    "#CDB4DB",
    "#A8DADC",
    "#BDE0FE",
)


def normalize_phone(phone):
    phone = phone.strip()

    if not phone:
        return phone

    if (
        phone.startswith("8")
        and len(phone) == PHONE_LENGTH_WITH_EIGHT
        and phone.isdigit()
    ):
        return "+7" + phone[1:]

    if (
        phone.startswith("+7")
        and len(phone) == PHONE_LENGTH_WITH_PLUS
        and phone[1:].isdigit()
    ):
        return phone

    raise ValidationError(
        "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
    )


def validate_github_url(github_url):
    github_url = github_url.strip()

    if not github_url:
        return github_url

    parsed_url = urlparse(github_url)

    if parsed_url.netloc not in GITHUB_HOSTS:
        raise ValidationError("Ссылка должна вести на GitHub.")

    return github_url


def generate_avatar_file(name, email):
    background_color = choice(AVATAR_COLORS)
    letter = name[0].upper() if name else DEFAULT_AVATAR_LETTER

    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), background_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", AVATAR_FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_position = (
        (AVATAR_SIZE - text_width) / 2,
        (AVATAR_SIZE - text_height) / 2 - AVATAR_VERTICAL_OFFSET,
    )

    draw.text(text_position, letter, fill="#FFFFFF", font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    file_name = f"avatar_{email}.png"

    return file_name, ContentFile(buffer.getvalue())
