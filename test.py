# obj = {"tom":"18","mary":"19"}
# obj.keys()
# for key in obj.keys():
#     print(key)
# import SDCS_pb2_grpc
# import SDCS_pb2

# import grpc


# with grpc.insecure_channel("127.0.0.1:50052") as channel:
#     stub = SDCS_pb2_grpc.sdcsStub(channel)
#     response = stub.search_kv_local(SDCS_pb2.request(key="tom1"))
# print(response)

import json

temp = {}

for i in range(10):
    temp.setdefault("tom%s"%(str(i)),i)

if "tom2" in temp.keys():
    print(temp.get("tom2"))
    del temp["tom2"]

print(temp)