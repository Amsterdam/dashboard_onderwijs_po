from django.conf.urls import url, include
from api import views

onderwijs_router = views.OnderwijsAPIRouter()
onderwijs_router.register(
    'vestiging', views.VestigingViewSet, base_name='vestiging'
)

onderwijs_router.register(
    'schooladvies', views.SchoolAdviesViewSet,
    base_name='schooladvies'
)
onderwijs_router.register(
    'leerling-naar-gewicht', views.LeerlingNaarGewichtViewSet,
    base_name='leerling-naar-gewicht'
)

onderwijs_router.register(
    'cito-score', views.CitoScoresViewSet,
    base_name='cito-score'
)

onderwijs_router.register(
    'subdsidie', views.SubsidieViewSet,
    base_name='subsidie'
)

onderwijs_router.register(
    'schoolwisselaar', views.SchoolWisselaarsViewSet,
    base_name='schoolwisselaar'
)

onderwijs_router.register(
    'toegewezen-subsidie', views.ToegewezenSubsidieViewSet,
    base_name='toegewezen-subsidie'
)

onderwijs_router.register(
    'leerling-leraar-ratio', views.LeerlingLeraarRatioViewSet,
    base_name='leerling-leraar-ratio'
)

urlpatterns = [
    url(r'^aggregated-advies/', views.AggregatedAdviesView.as_view()),
    url(r'^', include(onderwijs_router.urls)),
]
