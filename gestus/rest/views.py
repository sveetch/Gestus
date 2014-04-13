from cStringIO import StringIO

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, renderers
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from gestus.models import Website, WebsiteEnvironment, Egg, EggVersion
from gestus.rest import serializers as gestus_serializers

@api_view(('GET',))
def api_root(request, format=None):
    """
    This is the entry point that display available endpoints for this API
    """
    return Response({
        'websites': reverse('gestus:api-website-list', request=request, format=format),
        'environments': reverse('gestus:api-environment-list', request=request, format=format),
        'eggs': reverse('gestus:api-egg-list', request=request, format=format),
    })


#class WebsiteList(APIView):
    #"""
    #List all available websites
    #"""
    #def get(self, request, format=None):
        #websites = Website.objects.all()
        #serializer = gestus_serializers.WebsiteSerializer(websites, many=True, context={'request': request})

        #return Response(serializer.data)

class WebsiteList(generics.ListCreateAPIView):
    """
    List all available websites and create a new one
    """
    serializer_class = gestus_serializers.WebsiteSerializer
    model = Website

class WebsiteDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a website object
    """
    serializer_class = gestus_serializers.WebsiteDetailSerializer
    model = Website


class WebsiteEnvironmentList(generics.ListCreateAPIView):
    """
    List all available Websites environments and create a new one
    """
    serializer_class = gestus_serializers.EnvironmentSerializer
    model = WebsiteEnvironment

    
class WebsiteEnvironmentDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a WebsiteEnvironment object
    """
    serializer_class = gestus_serializers.EnvironmentDetailSerializer
    model = WebsiteEnvironment


class EggList(APIView):
    """
    List all available eggs
    """
    def get(self, request, format=None):
        eggs = Egg.objects.all()
        serializer = gestus_serializers.EggSerializer(eggs, many=True, context={'request': request})

        return Response(serializer.data)

class EggDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a egg object
    """
    serializer_class = gestus_serializers.EggDetailSerializer
    model = Egg
