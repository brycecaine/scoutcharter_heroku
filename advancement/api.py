from tastypie.resources import ModelResource
from advancement.models import Scout


class ScoutResource(ModelResource):
    class Meta:
        queryset = Scout.objects.all()
        resource_name = 'scout'