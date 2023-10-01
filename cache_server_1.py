import grpc
import SDCS_pb2
import SDCS_pb2_grpc
from concurrent import futures
import json
import threading
from multiprocessing import Process
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

dict_buffer = {}

class Cache_Server(SDCS_pb2_grpc.sdcsServicer):
    def __init__(self) -> None:
        super().__init__()


    def search_kv(self, request, context):
        key = request.key
        if key is not None and key in dict_buffer.keys():
            temp_dict = {}
            temp_dict.setdefault(key,dict_buffer.get(key))
            return SDCS_pb2.response(value=json.dumps(temp_dict, ensure_ascii=False))
        else:
            return SDCS_pb2.response(value=self.__search_neighbor(key))
    
    def __search_neighbor(self, key):
        temp_dict = {}

        try:
            with grpc.insecure_channel("localhost:50052") as channel:
                stub = SDCS_pb2_grpc.sdcsStub(channel)
                response = stub.search_kv(SDCS_pb2.request(key=key))
            
            if json.loads(response.value) != "not found":
                temp_dict.setdefault(key, response.value)
                return json.dumps(temp_dict, ensure_ascii = False)
        except Exception as e:
            pass

        try:
            with grpc.insecure_channel("localhost:50053") as channel:
                stub = SDCS_pb2_grpc.sdcsStub(channel)
                response = stub.search_kv(SDCS_pb2.request(key=key))

            if json.loads(response.value) != "not found":
                temp_dict.setdefault(key, response.value)
                return json.dumps(temp_dict, ensure_ascii = False)
        except Exception as e:
            pass
        
        temp_dict.setdefault(key, "not found")
        return json.dumps(temp_dict, ensure_ascii = False)
    
    def add_kv(self, key, value):
        dict_buffer.setdefault(key, value)
        print(dict_buffer)
        return 0

    def server(self):
        port = "50051"
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

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # print(self.path.strip("/"))
        key = self.path.strip("/")
        my_cache_server = Cache_Server()
        print("request key: %s" % key)

        response = my_cache_server.search_kv(SDCS_pb2.request(key = key),None)
        print(response)

        print(str(response.value))
        if json.loads(response.value)[key] != "not found":
            self.send_response(200)

            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            self.wfile.write(str(response.value).encode(encoding='utf-8'))
        else:
            self.send_response(404)

            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            self.wfile.write("".encode(encoding='utf-8'))

    def do_POST(self):
        req_datas = self.rfile.read(int(self.headers['Content-Length']))
        # print(req_datas)
        # print(req_datas.decode(encoding="utf-8"))

        my_cache_server = Cache_Server()

        obj = json.loads(req_datas.decode(encoding="utf-8"))
        tup = obj.popitem()
        key = tup[0]
        value = tup[1]
        response = my_cache_server.add_kv(key = key, value = value)

        # print(key)
        # print(value)
        # print(obj)
        self.send_response(200)

        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        self.wfile.write(req_datas)

    def do_DELETE(self):
        self.send_response(200)

        # 2. 发送响应头
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # 3. 发送响应内容（此处流不需要关闭）
        self.wfile.write("Delete successfully".encode("utf-8"))
        pass

def run_httpd_server():
    httpd = HTTPServer(('127.0.0.1', 9527), HttpHandler)
    httpd.serve_forever()

def run_gRPC_server():
    my_cache_server = Cache_Server()
    my_cache_server.server()

if __name__ == "__main__":
    thread_gRPC_server = Process(target=run_gRPC_server)
    thread_httpd_server = Process(target=run_httpd_server)

    thread_httpd_server.start()
    thread_gRPC_server.start()