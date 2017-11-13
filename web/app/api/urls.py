from api import views


onderwijs_router = views.OnderwijsAPIRouter()
onderwijs_router.register(
    'vestigingen', views.VestigingViewSet, base_name='vestigingen')
onderwijs_router.register(
    'viz/vestigingen', views.VestigingVizViewSet, base_name='viz-vestigingen')
onderwijs_router.register(
    'viz/leerlingen_naar_gewicht', views.LeerlingenNaarGewichtViewSet,
    base_name='viz-leerlingen-naar-gewicht'
)
onderwijs_router.register(
    'viz/school_adviezen', views.SchoolAdviezenViewSet,
    base_name='viz-school-adviezen'
)