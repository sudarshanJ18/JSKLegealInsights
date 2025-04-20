from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = False
    # Custom domain if using CloudFront
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    
    def __init__(self, *args, **kwargs):
        kwargs['gzip'] = getattr(settings, 'AWS_IS_GZIPPED', True)
        super().__init__(*args, **kwargs)

class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    
    def get_available_name(self, name, max_length=None):
        """Prevent overwriting existing files"""
        if self.file_overwrite:
            return super().get_available_name(name, max_length)
        return name