from api import views


onderwijs_router = views.OnderwijsAPIRouter()
onderwijs_router.register(
    'vestigingen', views.VestigingViewSet, base_name='vestigingen')

onderwijs_router.register(
    'schooladvies', views.SchoolAdviesViewSet,
    base_name='school-advies'
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
    'schoolwisselaars', views.SchoolWisselaarsViewSet,
    base_name='schoolwisselaars'
)

