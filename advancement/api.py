from advancement.models import Scout
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'

class ScoutResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = Scout.objects.all() #filter(id=1)
        resource_name = 'scouts'
        authorization = Authorization()
        always_return_data = True

        authentication = BasicAuthentication()