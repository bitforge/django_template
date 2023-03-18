
from collections import OrderedDict

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from translations import models


def serialize_pwa():
    # msgs = {'de': OrderedDict(), 'en': OrderedDict()}
    msgs = OrderedDict()
    for group in models.Group.objects.prefetch_related('messages'):
        msgs[group.key] = OrderedDict((m.key, m.de) for m in group.messages.all())
        # msgs['de'][group.key] = OrderedDict((m.key, m.de) for m in group.messages.all())
        # msgs['en'][group.key] = OrderedDict((m.key, m.en) for m in group.messages.all() if m.en)
    return msgs


@login_required
def export_pwa(request):
    msgs = serialize_pwa()
    return JsonResponse(msgs)
