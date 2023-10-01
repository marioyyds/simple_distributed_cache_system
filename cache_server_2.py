import grpc
import SDCS_pb2
import SDCS_pb2_grpc
from concurrent import futures
import json

class Cache_Server(SDCS_pb2_grpc.sdcsServicer):
    def search_kv(self, request, context):
        my_dict = {"name":"Tom","age":18,"hometown":"China"}

        return SDCS_pb2.response(value=json.dumps(my_dict))

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = SDCS_pb2_grpc.sdcsStub(channel)
        response = stub.search_kv(SDCS_pb2.request("my_request_id"))
    
    print("response message: " + response)

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    SDCS_pb2_grpc.add_sdcsServicer_to_server(Cache_Server(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    # run()
    serve()