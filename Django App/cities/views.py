from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib import messages


from cities.forms import cityForm
from cities.models import City

# Create your views here.
__all__ = (
    'home',
    'CityDetailView',
    'CityCreateView',
    'CityUpdateView',
    'CityDeleteView',
    'CityListView',
    )

def home(request,pk = None):
    if request.method == 'POST':
        form  = cityForm(request.POST)
        if form.is_valid():
            print (form.cleaned_data)
            form.save()
    form = cityForm()


    qs = City.objects.all()
    lst = Paginator(qs,5)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)
    context = {'page_obj': page_obj,'form': form}
    return render(request, 'cities/home.html', context)

class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin,CreateView):
    model = City
    form_class = cityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Город успешно создан'

class CityUpdateView(SuccessMessageMixin,UpdateView):
    model = City
    form_class = cityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Город успешно обновлен'

class CityDeleteView(DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')
    

    def get(self,request, *args, **kwargs):
        messages.success(request,'City deleted')
        return self.post(request, *args, **kwargs)

class CityListView(ListView):
    paginate_by = 2
    model = City
    template_name = 'cities/home.html'