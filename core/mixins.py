class IsolateToUserMixin:
    """
    Mixin is solution of repeated work. Anything that repeats we can make
    a Mixin of it.
    This mixin basically provide support for Viewing and Adding any data.
    It will always add user_id while creating and for fetching it will filter
    data based on user.
    - lists/retrieves only the logged-in user's rows
    - stamps the logged-in user on create
    Use it on any view whose model has a `user` field.
    Important: write the mixin on the LEFT side, like this:

        class MyView(IsolateToUserMixin, generics.ListCreateAPIView):
            queryset = MyModel.objects.all()
    """

    def get_queryset(self):
        # super() = "whoever is next in line after me" (the generic view)
        # super() basically asking next view, give me your queryset, it get 
        # queryset() from the view and attach its filter.
        # Mixin runs first, ask view to give him queryset and the attach its logic
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        # On create, set the owner automatically from the login token.
        serializer.save(user=self.request.user)
