# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import SDCS_pb2 as SDCS__pb2


class sdcsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.search_kv = channel.unary_unary(
                '/sdcs/search_kv',
                request_serializer=SDCS__pb2.request.SerializeToString,
                response_deserializer=SDCS__pb2.response.FromString,
                )
        self.search_kv_local = channel.unary_unary(
                '/sdcs/search_kv_local',
                request_serializer=SDCS__pb2.request.SerializeToString,
                response_deserializer=SDCS__pb2.response.FromString,
                )
        self.update_kv = channel.unary_unary(
                '/sdcs/update_kv',
                request_serializer=SDCS__pb2.request.SerializeToString,
                response_deserializer=SDCS__pb2.response.FromString,
                )
        self.update_kv_local = channel.unary_unary(
                '/sdcs/update_kv_local',
                request_serializer=SDCS__pb2.request.SerializeToString,
                response_deserializer=SDCS__pb2.response.FromString,
                )
        self.delete_kv = channel.unary_unary(
                '/sdcs/delete_kv',
                request_serializer=SDCS__pb2.request.SerializeToString,
                response_deserializer=SDCS__pb2.response.FromString,
                )
        self.delete_kv_local = channel.unary_unary(
                '/sdcs/delete_kv_local',
                request_serializer=SDCS__pb2.request.SerializeToString,
                response_deserializer=SDCS__pb2.response.FromString,
                )


class sdcsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def search_kv(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def search_kv_local(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_kv(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_kv_local(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_kv(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_kv_local(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_sdcsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'search_kv': grpc.unary_unary_rpc_method_handler(
                    servicer.search_kv,
                    request_deserializer=SDCS__pb2.request.FromString,
                    response_serializer=SDCS__pb2.response.SerializeToString,
            ),
            'search_kv_local': grpc.unary_unary_rpc_method_handler(
                    servicer.search_kv_local,
                    request_deserializer=SDCS__pb2.request.FromString,
                    response_serializer=SDCS__pb2.response.SerializeToString,
            ),
            'update_kv': grpc.unary_unary_rpc_method_handler(
                    servicer.update_kv,
                    request_deserializer=SDCS__pb2.request.FromString,
                    response_serializer=SDCS__pb2.response.SerializeToString,
            ),
            'update_kv_local': grpc.unary_unary_rpc_method_handler(
                    servicer.update_kv_local,
                    request_deserializer=SDCS__pb2.request.FromString,
                    response_serializer=SDCS__pb2.response.SerializeToString,
            ),
            'delete_kv': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_kv,
                    request_deserializer=SDCS__pb2.request.FromString,
                    response_serializer=SDCS__pb2.response.SerializeToString,
            ),
            'delete_kv_local': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_kv_local,
                    request_deserializer=SDCS__pb2.request.FromString,
                    response_serializer=SDCS__pb2.response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sdcs', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class sdcs(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def search_kv(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdcs/search_kv',
            SDCS__pb2.request.SerializeToString,
            SDCS__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def search_kv_local(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdcs/search_kv_local',
            SDCS__pb2.request.SerializeToString,
            SDCS__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_kv(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdcs/update_kv',
            SDCS__pb2.request.SerializeToString,
            SDCS__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_kv_local(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdcs/update_kv_local',
            SDCS__pb2.request.SerializeToString,
            SDCS__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_kv(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdcs/delete_kv',
            SDCS__pb2.request.SerializeToString,
            SDCS__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_kv_local(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdcs/delete_kv_local',
            SDCS__pb2.request.SerializeToString,
            SDCS__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
