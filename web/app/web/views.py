from django.views.generic import ListView, DetailView
from dataset.models import Vestiging


class VestigingListView(ListView):
    model = Vestiging


class VestigingDetailView(DetailView):
    model = Vestiging
