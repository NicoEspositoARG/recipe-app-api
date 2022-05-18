from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import Tag, Recipe
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(
            user=self.request.user).order_by('-name')
        # request is a class variable and user should be set when authenticated

    def perform_create(self, serializer):
        """Create a new Tag"""
        serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Override to filter user related recipes."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""

        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)
