import cloudinary
import cloudinary.uploader


class CloudinaryHandle:
    def __init__(self):
        self.__cloud_config = cloudinary.config(
            cloud_name='projectl',
            api_key='688722485286563',
            api_secret='rwk4YMdvr3Q3X4VE0sP0CaXoeys'
        )

    def upload_image(self, image_file) -> None:
        result = cloudinary.uploader.upload(image_file)
        image_url = result.get('secure_url')

        return image_url
