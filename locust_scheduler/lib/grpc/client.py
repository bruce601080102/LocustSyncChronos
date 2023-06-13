import grpc
# import dockerInfo_pb2
# import dockerInfo_pb2_grpc
from lib.grpc.dockerInfo_pb2_grpc import DockerInfoStub
from lib.grpc.dockerInfo_pb2 import DockerInfoRequest


def connect_grpc(value):
    # 連接到 localhost:50051
    channel = grpc.insecure_channel('192.168.10.111:50051')

    stub = DockerInfoStub(channel)

    request = DockerInfoRequest(value=value)

    response = stub.DockerInfo(request)

    return response.value


def connect_grpc_execute_update(value):
    # 連接到 localhost:50051
    channel = grpc.insecure_channel('192.168.10.111:50051')
    stub = DockerInfoStub(channel)

    request = DockerInfoRequest(value=value)

    response = stub.ExecuteUpdate(request)

    return response.value
