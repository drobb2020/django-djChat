"""
Serializers for the Server API.
"""
from rest_framework import serializers
from server.models import Channel, Server


class ChannelSerializer(serializers.ModelSerializer):
    """
        Serializer for Channels.

        Attributes:
            Meta (class): Metadata class for defining serialization behavior.

    """

    class Meta:
        """
            Metadata class for defining serialization behavior.

            Attributes:
                model (class): The Django model associated with the serializer.
                fields (tuple, str): The fields to include in the serialized representation.
                    If set to "__all__", all fields of the model will be included.
        """
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Server model.

    Attributes:
        num_members (serializers.SerializerMethodField): A serializer method field to retrieve the number of members.
        channel_server (ChannelSerializer): A serializer for the related ChannelServer instances.

    Meta:
        model (class): The Django model associated with the serializer.
        exclude (tuple): The fields to exclude from the serialized representation.

    Methods:
        get_num_members(self, obj): Retrieves the number of members for the server.
        to_representation(self, instance): Customizes the serialized representation of the server.

    """

    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        """
        Metadata class for defining serialization behavior.

        Attributes:
            model (class): The Django model associated with the serializer.
            exclude (tuple): The fields to exclude from the serialized representation.

        """
        model = Server
        exclude = ("member",)

    def get_num_members(self, obj):
        """
        Retrieves the number of members for the server.

        Parameters:
            obj (Server): The Server instance being serialized.

        Returns:
            int: The number of members for the server, or None if it does not exist.

        """
        if hasattr(obj, 'num_members'):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """
        Customizes the serialized representation of the server.

        Parameters:
            instance (Server): The Server instance being serialized.

        Returns:
            dict: The customized serialized representation of the server.

        """
        data = super().to_representation(instance)
        num_members = self.context.get('num_members')
        if not num_members:
            data.pop('num_members', None)
        return data
