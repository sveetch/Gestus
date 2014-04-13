"""
Serializers for REST entries
"""
from django.forms import widgets

from rest_framework import serializers

from gestus.models import Website, WebsiteEnvironment, Egg, EggVersion


class EggVersionSerializer(serializers.ModelSerializer):
    """
    Serializer for ``EggVersion`` resumed model
    """
    class Meta:
        model = EggVersion
        fields = ('id', 'name')


class EggSerializer(serializers.ModelSerializer):
    """
    Serializer for ``Egg`` resumed model
    """
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='gestus:api-egg-detail',
        lookup_field='pk'
    )
    class Meta:
        model = Egg
        fields = ('id', 'created', 'modified', 'name', 'package', 'description', 'detail_url')

class EggDetailSerializer(EggSerializer):
    """
    Serializer for ``Egg`` detailled model
    """
    versions = EggVersionSerializer(
        many=True, read_only=True,
    )
    
    class Meta:
        model = Egg
        fields = ('id', 'created', 'modified', 'name', 'package', 'description', 'detail_url', 'versions')


class EnvironmentSerializer(serializers.ModelSerializer):
    """
    Serializer for ``WebsiteEnvironment`` resumed model
    """
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='gestus:api-environment-detail',
        lookup_field='pk'
    )
    
    egg_list = serializers.CharField(
        #source="eggs",
        widget=widgets.Textarea,
        write_only=True,
        required=True,
    )
    
    def validate_egg_list(self, attrs, source):
        """
        Validation for the given Egg list
        
        Valid format for each egg row is :
        
            egg name = version name
        
        Empty row is removed from the list, invalid row raises a validation error and commented row (with #) is not supported (and so is invalid).
        """
        value = attrs[source]
        if value:
            lines = value.strip().splitlines()
            self.computed_eggs = []
            
            for l in filter(None, lines):
                try:
                    pkg, version = l.split('=')
                except ValueError:
                    raise serializers.ValidationError(u"Invalid syntax for row: {0}".format(l.strip()))
                else:
                    pkg, version = pkg.strip(), version.strip()
                    try:
                        egg_version = EggVersion.objects.get(name=version, egg__name=pkg)
                    except EggVersion.DoesNotExist:
                        egg, created = Egg.objects.get_or_create(name=pkg, defaults={'package': pkg})
                        egg_version, created = EggVersion.objects.get_or_create(egg=egg, name=version)
                    self.computed_eggs.append(egg_version)
            
            if len(self.computed_eggs) == 0:
                raise serializers.ValidationError(u"There is no valid row")
                
        return attrs

    def save(self, **kwargs):
        """
        Override the save method to add the given eggs if any
        """
        super(EnvironmentSerializer, self).save(**kwargs)
        
        if hasattr(self, 'computed_eggs'):
            self.object.eggs.clear()
            self.object.eggs.add(*self.computed_eggs)
            self.object.save()
         
        return self.object
    
    class Meta:
        model = WebsiteEnvironment
        fields = ('id', 'created', 'modified', 'website', 'name', 'server', 'enabled', 'detail_url', 'egg_list')


class EnvironmentDetailSerializer(EnvironmentSerializer):
    """
    Serializer for ``WebsiteEnvironment`` detailled model
    """
    eggs = serializers.RelatedField(many=True, read_only=True)
    
    class Meta:
        model = WebsiteEnvironment
        fields = ('id', 'created', 'modified', 'website', 'name', 'server', 'enabled', 'detail_url', 'eggs', 'egg_list')


class WebsiteSerializer(serializers.ModelSerializer):
    """
    Serializer for ``Website`` resumed model
    """
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='gestus:api-website-detail',
        lookup_field='pk'
    )
    class Meta:
        model = Website
        fields = ('id', 'created', 'modified', 'name', 'url', 'enabled', 'description', 'detail_url')

class WebsiteDetailSerializer(WebsiteSerializer):
    """
    Serializer for ``Website`` detailled model
    """
    environments = EnvironmentDetailSerializer(
        many=True, read_only=True,
    )
    
    class Meta:
        model = Website
        fields = ('id', 'created', 'modified', 'name', 'url', 'enabled', 'description', 'detail_url', 'environments')
