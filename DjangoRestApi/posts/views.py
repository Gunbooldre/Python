from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,viewsets


from .serializer import BlogSerializer

from .models import Posts
# Create your views here.

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = BlogSerializer

# class PostsApiList(generics.ListCreateAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = BlogSerializer


# class PostsUpdate(generics.UpdateAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = BlogSerializer

# class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = BlogSerializer


# class BlogApi(APIView):
#     def get(self, request):
#         lst = Posts.objects.all()
#         return Response({"GET":BlogSerializer(lst,many = True).data})
    
#     def post(self, request):
#         serializer = BlogSerializer(data = request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response({"POST":serializer.data})

#     def put(self,request,*args, **kwargs):
#         pk = kwargs.get('pk',None)
#         if not pk:
#             return Response({"PUT":'Method Not Allowed'})
#         try:
#             instance = Posts.objects.get(pk=pk)
#         except:
#             return Response({"PUT":"Object does not exist"})
#         serializer = BlogSerializer(data = request.data,instance=instance)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response({"PUT":serializer.data})

#     def delete(self, request,*args, **kwargs):
#         pk = kwargs.get('pk',None)
#         if not pk:
#             return Response({"DELETE":"Method is not allowed"})
#         try:
#             instance = Posts.objects.get(pk=pk)
#             instance.delete()
#         except:
#             return Response({"DELETE":"object does not exist"})
#         return Response({"DELETE":"DELETE post"+str(pk)})