import grpc
import SDCS_pb2
import SDCS_pb2_grpc
import json

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = SDCS_pb2_grpc.sdcsStub(channel)
        response = stub.search_kv(SDCS_pb2.request(key="my_request_id"))
    
    obj = json.loads(response.value)
    print("response message: " + response.value)

    print("json name is %s" % (obj["name"]))

if __name__ == "__main__":
    run()
    # my_dict = {"name":["Tom", "Jhon", "CC"],"age":18,"hometown":"China"}
    # print(json.dumps(my_dict))
    # my_dict.setdefault("major","Math")
    # print(json.dumps(my_dict))
    # print(json.dumps(my_dict["name"]))
    # dict2 = {}
    # dict2.setdefault("name", my_dict["name"])
    # print(json.dumps(dict2))