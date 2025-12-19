import cloudinary
import cloudinary.uploader
from flask import current_app


class CloudinaryHandle:
    def __init__(self):
        self.__cloud_config = cloudinary.config(
            cloud_name=current_app.config['CLOUDNARY_NAME'],
            api_key=current_app.config['CLOUDNARY_API_KEY'],
            api_secret=current_app.config['CLOUDNARY_API_SECRET']
        )

    def upload_image(self, image_file) -> None:
        result = cloudinary.uploader.upload(image_file)
        image_url = result.get('secure_url')

        return image_url
