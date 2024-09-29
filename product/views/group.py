from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from product.serializers import GroupSerializer
from product.models import Group

class GroupDetailListApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        group_slug = self.kwargs.get('slug')
        return Group.objects.prefetch_related('products').filter(slug=group_slug)

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupAddView(generics.ListCreateAPIView):
    queryset = Group.objects.order_by('id')[:1]
    serializer_class = GroupSerializer
