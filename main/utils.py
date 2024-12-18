from PIL import Image 
import os
import uuid
from django.core.exceptions import ValidationError

def image_upload(instance, filename, dir):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join(dir, filename)

def validate_image(image, max_size_kb=1024, max_width=400, max_height=400):
    if image.size > max_size_kb * 1024:
        raise ValidationError(f"Image size should not exceed {max_size_kb}KB.")

    img = Image.open(image)
    width, height = img.size
    if width > max_width or height > max_height:
        raise ValidationError(f"Image dimensions should not exceed {max_width}x{max_height}px.")
    