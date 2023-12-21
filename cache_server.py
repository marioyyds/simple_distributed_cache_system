import grpc
import SDCS_pb2
import SDCS_pb2_grpc
from concurrent import futures
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

# to store key-value data
dict_buffer = {}

httpd_port = 80
httpd_bind_ip = "0.0.0.0"

gRPC_port = 50000
gRPC_local_ip = ""
gRPC_nearby_ip = []


class Cache_Server(SDCS_pb2_grpc.sdcsServicer):
    def __init__(self) -> None:
        super().__init__()

    def search_kv(self, request, context):
        response = self.search_kv_local(request=request,context=context)
        key = request.key
        if json.loads(response.value).get(key) != "not found":
            temp_dict = {}
            temp_dict.setdefault(key,dict_buffer.get(key))
            return SDCS_pb2.response(value=json.dumps(temp_dict, ensure_ascii=False))
        else:
            return self.__search_neighbor(key)
    
    def search_kv_local(self, request, context):
        key = request.key
        temp_dict = {}
        if key is not None and key in dict_buffer.keys():
            temp_dict.setdefault(key,dict_buffer.get(key))
            return SDCS_pb2.response(value=json.dumps(temp_dict, ensure_ascii=False))
        else:
            temp_dict.setdefault(key, "not found")
            return SDCS_pb2.response(value=json.dumps(temp_dict, ensure_ascii = False))

    def __search_neighbor(self, key):
        temp_dict = {}

        for nearby in gRPC_nearby_ip:
            try:
                with grpc.insecure_channel(nearby) as channel:
                    stub = SDCS_pb2_grpc.sdcsStub(channel)
                    response = stub.search_kv_local(SDCS_pb2.request(key=key))
                
                if json.loads(response.value).get(key) != "not found":
                    return SDCS_pb2.response(value=response.value)
            except Exception as e:
                print(e)
        
        temp_dict.setdefault(key, "not found")
        return SDCS_pb2.response(value=json.dumps(temp_dict, ensure_ascii = False))
    
    def update_kv(self, request, context):
        self.update_kv_local(request = request,context = context)
        for nearby in gRPC_nearby_ip:
            try:
                with grpc.insecure_channel(nearby) as channel:
                    stub = SDCS_pb2_grpc.sdcsStub(channel)
                    response = stub.delete_kv_local(request)
            except Exception as e:
                pass
        return

    def update_kv_local(self, request, context):
        key = request.key
        obj = json.loads(context)
        dict_buffer.setdefault(key, obj.get(key))

    def delete_kv(self, request, context):
        key = request.key
        self.delete_kv_local(request, context=context)
        
        for nearby in gRPC_nearby_ip:
            try:
                with grpc.insecure_channel(nearby) as channel:
                    stub = SDCS_pb2_grpc.sdcsStub(channel)
                    response = stub.delete_kv_local(SDCS_pb2.request(key=key))
            except Exception as e:
                pass
    
    def delete_kv_local(self, request, context):
        key = request.key
        if key in dict_buffer.keys():
            del dict_buffer[key]

    def server(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        SDCS_pb2_grpc.add_sdcsServicer_to_server(self, server)
        server.add_insecure_port(gRPC_local_ip)
        server.start()
        print("Server started, listening on " + gRPC_local_ip)
        server.wait_for_termination()

class Http_Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        key = self.path.strip("/")
        my_cache_server = Cache_Server()

        response = my_cache_server.search_kv(SDCS_pb2.request(key = key),None)

        if json.loads(response.value)[key] != "not found":
            self.send_response(200)

            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            self.wfile.write((str(response.value) + "\n").encode(encoding='utf-8'))
        else:
            self.send_response(404)

            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            self.wfile.write("\n".encode(encoding='utf-8'))

    def do_POST(self):
        req_datas = self.rfile.read(int(self.headers['Content-Length']))
        obj = json.loads(req_datas.decode(encoding="utf-8"))

        my_cache_server = Cache_Server()

        key = ''
        for k in obj.keys():
            key = k
        my_cache_server.update_kv(request= SDCS_pb2.request(key = key), context = json.dumps(obj, ensure_ascii = False))

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        self.wfile.write((json.dumps(obj) + "\n").encode("utf-8"))

    def do_DELETE(self):
        key = self.path.strip("/")

        my_cache_server = Cache_Server()

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        response = my_cache_server.search_kv(SDCS_pb2.request(key = key),None)
        if json.loads(response.value)[key] != "not found":
            my_cache_server.delete_kv(SDCS_pb2.request(key = key), context= None)
            self.wfile.write("1\n".encode("utf-8"))
        else:
            self.wfile.write("0\n".encode("utf-8"))

def run_httpd_server():
    httpd = HTTPServer((httpd_bind_ip, httpd_port), Http_Handler)
    httpd.serve_forever()

def run_gRPC_server():
    my_cache_server = Cache_Server()
    my_cache_server.server()

if __name__ == "__main__":
    # get my grpc ip
    gRPC_local_ip = sys.argv[1] + ":" + str(gRPC_port)
    # get nearby grpc ip
    for ip in sys.argv[2:]:
        gRPC_nearby_ip.append(ip + ":" + str(gRPC_port))

    # start gRPC and http server
    thread_gRPC_server = threading.Thread(target=run_gRPC_server)
    thread_httpd_server = threading.Thread(target=run_httpd_server)

    thread_httpd_server.start()
    thread_gRPC_server.start()
    thread_gRPC_server.join()
    thread_httpd_server.start()