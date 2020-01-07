from .environment import env, root


class S3(object):
    # S3 credentials for SQS and S3
    USE_S3 = env('USE_S3')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_LOCATION = env('AWS_LOCATION')
    AWS_REGION = env('AWS_REGION')

    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')

    @property
    def DEFAULT_FILE_STORAGE(self):
        if self.USE_S3:
            return 'storages.backends.s3boto3.S3Boto3Storage'

        # Use Django default
        return 'django.core.files.storage.FileSystemStorage'

    @property
    def MEDIA_URL(self):
        if self.USE_S3:
            return 'https://' + self.AWS_S3_CUSTOM_DOMAIN + '/'

        return '/media/'

    @property
    def MEDIA_ROOT(self):
        if self.USE_S3:
            return ''

        return root('media/')

    # This is a workaround for https://github.com/wagtail/wagtail/issues/3206
    AWS_S3_FILE_OVERWRITE = False
