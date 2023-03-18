from django.utils.html import format_html, mark_safe


def thumbnail_title(image_field_name: str, title_field_name: str) -> str:
    """
    Combines a title field with a thumbnail image
    """

    def thumbnail(instance):
        try:
            title = str(getattr(instance, title_field_name, None))
            image_field = getattr(instance, image_field_name, None)
            if not image_field.name:
                return title
            thumb_url = image_field.thumbnail['120x120'].url
            img_html = f'<img class="list-thumb" src="{thumb_url}" alt="{title}" />'
            return format_html(f'{img_html} {title}')
        except Exception as e:
            return mark_safe('<p>%s</p>' % e)

    thumbnail.short_description = title_field_name.capitalize()
    thumbnail.admin_order_field = image_field_name
    return thumbnail
