from django.contrib.admin import widgets as admin_widgets
from django.utils.safestring import mark_safe


class AutosizeTextArea(admin_widgets.AdminTextareaWidget):
    def __init__(self, attrs=None):
        super().__init__(
            attrs={'class': 'autosize', **(attrs or {'cols': 80, 'rows': 1})}
        )


class MarkdownTextArea(admin_widgets.AdminTextareaWidget):
    def __init__(self, attrs=None):
        super().__init__(
            attrs={'class': 'markdown', **(attrs or {'cols': 80, 'rows': 1})}
        )


class AdminImageWidget(admin_widgets.AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        html = ''
        if value and getattr(value, 'url', None):
            print(type(value))
            image_url = value.thumbnail['360x360'].url
            file_name = str(value)
            html = f'<img src="{image_url}" alt="{file_name}" class="admin-image"/>'
        html += super().render(name, value, attrs)
        return mark_safe(html)
