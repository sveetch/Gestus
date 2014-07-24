"""
Serializers for REST entries
"""
import ast, json

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
    
    def oldvalidate_egg_list(self, attrs, source):
        """
        Validation for a given Egg raw list
        
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
                    #print pkg, version
                    try:
                        egg_version = EggVersion.objects.get(name=version, egg__name=pkg)
                    except EggVersion.DoesNotExist:
                        egg, created = Egg.objects.get_or_create(name=pkg, defaults={'package': pkg})
                        egg_version, created = EggVersion.objects.get_or_create(egg=egg, name=version)
                    else:
                        # update url, summary, description
                        pass
                    self.computed_eggs.append(egg_version)
            
            if len(self.computed_eggs) == 0:
                raise serializers.ValidationError(u"There is no valid row")
                
        return attrs
    
    def validate_egg_list(self, attrs, source):
        """
        Validation for a given Egg list
        
        Valid format for each egg row is :
        
            egg name = version name
        
        Empty row is removed from the list, invalid row raises a validation error and commented row (with #) is not supported (and so is invalid).
        """
        value = attrs[source]
        #value = attrs[source]
        
        #print self.context['request'].DATA
        
        if value:
            self.computed_eggs = []
            
            # The following line raise a JSON error because it seems the value 
            # is Python repr (containing u'' prefixes) not a real JSON string, 
            # see: http://stackoverflow.com/questions/24899713/troubles-with-json-data-and-unicode-on-django-rest-framework
            #egg_map = json.loads(value)
            
            # This works because we safely evaluate the repr as a dict
            egg_map = ast.literal_eval(value)
            
            # Get sended packages infos
            if isinstance(egg_map, dict):
                for pkg_name, pkg_infos in egg_map.items():
                    pkg_version = pkg_infos['version']
                    pkg_url = pkg_infos['url']
                    pkg_summary = pkg_infos.get('summary','')
                    pkg_description = pkg_infos.get('description','')
                    #print pkg_name
                    #print "-"*90
                    #print pkg_description
                    #print
                    #print
                    
                    try:
                        egg_version = EggVersion.objects.get(name=pkg_version, egg__name=pkg_name)
                    except EggVersion.DoesNotExist:
                        # This egg version does not exist, we must create it
                        egg, created = Egg.objects.get_or_create(name=pkg_name, defaults={
                            'package': pkg_name, 
                            'url': pkg_url, 
                            'summary': pkg_summary, 
                            'description': pkg_description
                        })
                        egg_version, created = EggVersion.objects.get_or_create(egg=egg, name=pkg_version)
                    else:
                        # This egg version allready exists update its egg infos
                        egg = egg_version.egg
                        egg.url = pkg_url
                        egg.summary = pkg_summary
                        egg.description = pkg_description
                        egg.save()
                    self.computed_eggs.append(egg_version)
            
            if len(self.computed_eggs) == 0:
                raise serializers.ValidationError(u"There is no valid row")
                
        return attrs

    def save(self, **kwargs):
        """
        Override the save method to add the given eggs if any
        """
        super(EnvironmentSerializer, self).save(**kwargs)
        
        # If eggs are given, clean older registered eggs and add the new ones
        if hasattr(self, 'computed_eggs'):
            self.object.eggs.clear()
            self.object.eggs.add(*self.computed_eggs)
            self.object.save()
         
        return self.object
    
    class Meta:
        model = WebsiteEnvironment
        fields = ('id', 'created', 'modified', 'website', 'name', 'url', 'server', 'enabled', 'detail_url')


class EnvironmentDetailSerializer(EnvironmentSerializer):
    """
    Serializer for ``WebsiteEnvironment`` detailled model
    """
    website_name = serializers.RelatedField(source='website.name', read_only=True)
    
    eggs = serializers.RelatedField(many=True, read_only=True)
    
    class Meta:
        model = WebsiteEnvironment
        fields = ('id', 'created', 'modified', 'website', 'website_name', 'name', 'url', 'server', 'enabled', 'detail_url', 'eggs', 'egg_list')


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
        fields = ('id', 'created', 'modified', 'name', 'enabled', 'description', 'detail_url')

class WebsiteDetailSerializer(WebsiteSerializer):
    """
    Serializer for ``Website`` detailled model
    """
    environments = EnvironmentSerializer(
        many=True, read_only=True,
    )
    
    class Meta:
        model = Website
        fields = ('id', 'created', 'modified', 'name', 'enabled', 'description', 'detail_url', 'environments')
