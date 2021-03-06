from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _

from ..models import Person
from ..forms import UnsubscribeForm


def unsubscribe(request, token):
    if not token:
        raise Http404()

    try:
        person = Person.objects.get(token=token)
    except Person.DoesNotExist:
        return render(request, 'news/unsubscribe.html')
    except ValidationError:
        raise Http404()

    form = UnsubscribeForm(request.POST or None)
    if form.is_valid():
        person.delete()
        return HttpResponseRedirect(reverse('news:subscription_deleted'))

    context = {'person': person}
    return render(request, 'news/unsubscribe.html', context)
