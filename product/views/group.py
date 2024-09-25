from rest_framework import generics, status
from rest_framework.response import Response
from product import serializers
from product.models import Group


class GroupDetailListApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.GroupSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Group.objects.prefetch_related('products').all()

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupAddView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
