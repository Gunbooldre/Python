from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib import messages


from plains.forms import PlainForm
from plains.models import Plain

# Create your views here.
__all__ = (
    'home',
     'PlainDetailView',
    'PlainCreateView',
    'PlainUpdateView',
    'PlainDeleteView',
    'PlainListView',
    )

def home(request,pk = None):
    qs = Plain.objects.all()
    lst = Paginator(qs,5)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'plains/home.html', context)

class PlainListView(ListView):
    paginate_by = 5
    model = Plain
    template_name = 'plains/home.html'


class PlainDetailView(DetailView):
    queryset = Plain.objects.all()
    template_name = 'plains/detail.html'



class PlainCreateView(SuccessMessageMixin,CreateView):
    model = Plain
    form_class = PlainForm
    template_name = 'plains/create.html'
    success_url = reverse_lazy('plains:home')
    success_message = 'Город успешно создан'

class PlainUpdateView(SuccessMessageMixin,UpdateView):
    model = Plain
    form_class = PlainForm
    template_name = 'plains/update.html'
    success_url = reverse_lazy('plains:home')
    success_message = 'Город успешно обновлен'

class PlainDeleteView(DeleteView):
    model = Plain
    template_name = 'plains/delete.html'
    success_url = reverse_lazy('plains:home')
    

    def get(self,request, *args, **kwargs):
        messages.success(request,'Plain deleted')
        return self.post(request, *args, **kwargs)

