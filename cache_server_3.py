import grpc
import SDCS_pb2
import SDCS_pb2_grpc
from concurrent import futures
import json
import threading

class Cache_Server(SDCS_pb2_grpc.sdcsServicer):
    def __init__(self) -> None:
        super().__init__()
        self.dict = {}

    def search_kv(self, request, context):
        key = request.key
        if key is not None and key in self.dict.keys():   
            return SDCS_pb2.response(value=json.dumps(self.dict.get(key)))
        else:
            return SDCS_pb2.response(value=self.__search_neighbor(key))
    
    def __search_neighbor(self, key):
        temp_dict = {}

        try:
            with grpc.insecure_channel("localhost:50051") as channel:
                stub = SDCS_pb2_grpc.sdcsStub(channel)
                response = stub.search_kv(SDCS_pb2.request(key=key))
            
            if json.loads(response.value) != "not found":
                temp_dict.setdefault(key, response.value)
                return json.dumps(temp_dict)
        except Exception as e:
            pass

        try:
            with grpc.insecure_channel("localhost:50052") as channel:
                stub = SDCS_pb2_grpc.sdcsStub(channel)
                response = stub.search_kv(SDCS_pb2.request(key=key))

            if json.loads(response.value) != "not found":
                temp_dict.setdefault(key, response.value)
                return json.dumps(temp_dict)
        except Exception as e:
            pass
        
        temp_dict.setdefault(key, "not found")
        return json.dumps(temp_dict)
    
    def add_kv(self, key, value):
        self.dict.setdefault(key, value)
        return 0

    def server(self):
        port = "50053"
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        SDCS_pb2_grpc.add_sdcsServicer_to_server(self, server)
        server.add_insecure_port("[::]:" + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()

    def run(self):
        thread_server = threading.Thread(target=self.server)
        thread_server.start()
        thread_server.join()

if __name__ == "__main__":
    my_cache_server = Cache_Server()
    my_cache_server.run()