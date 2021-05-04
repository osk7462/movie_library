from rest_framework import viewsets
from .models import Collection
from .serializers import CollectionSerializer
from rest_framework.response import Response
import json
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from requests.auth import HTTPBasicAuth


class MovieList(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def list(self, request):
        url = 'https://demo.credy.in/api/v1/maya/movies/'
        page = request.GET.get('page')
        page_number = 1
        if page:
            url = "https://demo.credy.in/api/v1/maya/movies/?page={}".format(
                page)
            page_number = int(page)

        username = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
        password = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        response = response.json()
        response['next'] = "http://127.0.0.1:8000/movies/?page={}".format(
            page_number+1)
        if page_number > 1:
            response['previous'] = "http://127.0.0.1:8000/movies/?page={}".format(
                page_number-1)
        return Response({'data': response})


class CollectionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        response = {'is_success': True}
        collection = Collection.objects.filter(user=request.user)

        serializer = CollectionSerializer(
            collection, user=request.user, many=True)
        data = json.loads(json.dumps(serializer.data))
        collections = []
        for collection in data:
            collections.append({'uuid': collection.get('uuid'), 'title': collection.get(
                'title'), 'description': collection.get('description')})
        top_genre = collection.get('top_genre') if len(collection) > 0 else ''
        response['data'] = {"collections": collections,
                            'favourite_genre': top_genre}
        return Response(response)   

    def create(self, request):
        serializer = CollectionSerializer(
            data=request.data, user=request.user, action='create')
        if serializer.is_valid():
            collection = serializer.save()
            return Response({'collection_uuid': collection.uuid})
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(collection, user=request.user)
        data = json.loads(json.dumps(serializer.data))
        del data['user']
        del data['top_genre']
        return Response(data)

    # this response will be send when user try to update his collection
    def response(self, serializer):
        if serializer.is_valid():
            serializer.save()
            data = json.loads(json.dumps(serializer.data))
            del data['user']
            del data['top_genre']
            return Response(data)
        return Response(serializer.errors)

    def update(self, request, pk=None):
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(
            collection, data=request.data, user=request.user)
        return self.response(serializer)

    def partial_update(self, request, pk=None):
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(
            collection, data=request.data, user=request.user, partial=True)
        return self.response(serializer)

    def destroy(self, request, pk=None):
        collection = Collection.objects.get(pk=pk)
        collection.delete()
        return Response({})
