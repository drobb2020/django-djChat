# from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from server.models import Server
from server.schema import server_list_docs
from server.serializers import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """Viewsets for Server List"""

    # query for all the servers in the database
    queryset = Server.objects.all()

    # Defining list method to get all servers.
    @server_list_docs
    def list(self, request):
        """
        Retrieves a list of items based on query parameters and returns a serialized response.

        This method retrieves a queryset of servers based on the query parameters provided in the 'request' object.
        The following query parameters are supported:

            - `category`: Filters servers by their category
            - `qty`: Limits the number of servers returned
            - `by_user`: Filters servers by user ID, only returning servers that the user is a member of
            - `by_serverid`: Filters servers by server ID
            - `with_num_members`: Annotates each server with the number of members it has

        Args:

            request: A Django Request object containing query parameters.

        Parameters:

            request (HttpRequest): The HTTP request object containing query parameters.

        Raises:

            AuthenticationFailed: If by_user or by_serverid is set to true and the user is not authenticated.
            ValidationError: If the provided by_serverid is not a valid server ID.

        Returns:

            Response: The serialized data response containing the list of items.

        Description:

            This method handles the retrieval of items based on query parameters passed in the HTTP request.
            The available query parameters include 'category', 'qty', 'by_user', 'by_serverid', and 'with_num_members'.

            The 'category' parameter allows filtering the items based on their category.

            The 'qty' parameter limits the number of items to be retrieved.

            The 'by_user' parameter filters the items based on the ID of the authenticated user.
            If the 'by_user' or 'by_serverid' parameter is set to true and the user is not authenticated,
            an AuthenticationFailed error will be raised.

            The 'by_serverid' parameter filters the items based on the server ID.
            If the provided server ID is not found, a ValidationError is raised.

            The 'with_num_members' parameter enables annotating the items with the count of members.

            After applying the filters and annotations, the resulting queryset is serialized using
            the ServerSerializer,
            and a serialized data response is returned.

        Examples:

            To retrieve all servers in the 'gaming' category with at least 5 members, you can make
            the following request:

                GET /servers/?category=gaming&with_num_members=true&num_members__gte=5

            To retrieve the first 10 servers that the authenticated user is a member of, you can
            make the following request:

                GET /servers/?by_user=true&qty=10

        """
        # Extracting query parameters from the request
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # If category query parameter is provided then filter based on category
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # If by_user query parameter is given then filter based on member id
        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()

        # If qty query parameter is provided then filter based on quantity
        if qty:
            self.queryset = self.queryset[: int(qty)]

        # if by_serverid query parameter is given then filter based on server id
        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()

            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server {by_serverid} not found.")
            except ValueError:
                raise ValidationError(detail=f"Server {by_serverid} generated a value error.")

        # If with_num_members query parameter is given then annotate based on number of members
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Serializing queryset and returning response with serialized data
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
