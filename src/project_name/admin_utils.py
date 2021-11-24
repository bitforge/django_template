from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _


def thumbnail_field(image_name: str, field_name: str) -> str:
    """
    Combines a field with a thumbnail image
    """
    def thumbnail(instance):
        try:
            display_name = str(getattr(instance, field_name, None))
            image_field = getattr(instance, image_name, None)
            if not image_field.name or not image_field.thumb:
                return display_name
            img_html = f'<img class="list-thumb" src="{image_field.thumb}" alt="{display_name}" />'
            return format_html(f'{img_html} {display_name}')
        except Exception as e:
            return mark_safe('<p>%s</p>' % e)

    thumbnail.short_description = field_name.capitalize()
    thumbnail.admin_order_field = field_name
    return thumbnail