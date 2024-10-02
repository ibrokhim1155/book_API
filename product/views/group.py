from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from product.serializers import GroupSerializer
from product.models import Group


class GroupDetailListApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Group.objects.prefetch_related('products').filter(slug=self.kwargs['slug'])

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


class GroupAddView(generics.CreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
