import grpc
import dockerInfo_pb2
import dockerInfo_pb2_grpc
import dockerInfo
from concurrent import futures


class DockerInfoServicer(dockerInfo_pb2_grpc.DockerInfoServicer):
    def DockerInfo(self, request, context):
        response = dockerInfo_pb2.DockerInfoResponse()
        response.value = dockerInfo.dockerinfo(request.value)
        return response

    def ExecuteUpdate(self, request, context):

        response1 = dockerInfo_pb2.DockerInfoResponse()
        response1.value = dockerInfo.executeupdate(request.value)
        return response1


def serve_start():
    server_1 = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dockerInfo_pb2_grpc.add_DockerInfoServicer_to_server(DockerInfoServicer(), server_1)
    server_1.add_insecure_port('[::]:50051')
    server_1.start()
    server_1.wait_for_termination()


if __name__ == '__main__':
    print("grpc server is starting")
    serve_start()
