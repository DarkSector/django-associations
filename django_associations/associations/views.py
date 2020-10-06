from django.http import HttpResponse

# Create your views here.
from django.views import View
from .api import get_association_list


class AssociationsView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(content=get_association_list())
