import os

# Model helper methods
# Some of these tend to get part of migrations, so be careful with namings!


def entry_image_upload_path(instance, filename):
    return os.path.join('entry', instance.slug, 'images', filename)
