from concurrent import futures
import grpc
import calc_pb2
import calc_pb2_grpc
import hashlib


class CalcerServicer(calc_pb2_grpc.CalcerServicer):
    def Add(self, request, context):
        print("ADD received:")
        print(request)
        res = request.a + request.b
        response = calc_pb2.CalcReply()
        response.c = res
        return response

    def Subtract(self, request, context):
        print("SUBTRACT received:")
        print(request)
        res = request.a - request.b
        response = calc_pb2.CalcReply()
        response.c = res
        return response

    def Multiply(self, request, context):
        print("MULTIPLY received:")
        print(request)
        res = request.a * request.b
        response = calc_pb2.CalcReply()
        response.c = res
        return response

    def Divide(self, request, context):
        print("DIVIDE received:")
        print(request)
        res = request.a / request.b
        response = calc_pb2.CalcReplyF()
        response.c = res
        return response
    
    def MultiPlus(self, request_iterator, context):
        sum = 0
        count = 1
        print(f"Receiving MULTIPLUS stream from {context.peer()}...")
        for request in request_iterator:
            print(f"This is request {request.counter} from {context.peer()}, my internal counter is {count}, the request was {request.a}")
            sum += request.a
            count += 1
        response = calc_pb2.CalcReply()
        response.c = sum
        return response
    
    def InteractiveMultiPlus(self, request_iterator, context):
        sum = 0
        count = 1
        for request in request_iterator:
            print(f"This is request {request.counter} from {context.peer()}, my internal counter is {count}, the request was {request.a}")
            sum += request.a
            count += 1
            response = calc_pb2.CalcReply()
            response.c = sum
            yield response

    def HashFile(self, request, context):
        file = request.file
        m = hashlib.sha256()
        m.update(file)
        h = m.hexdigest()
        response = calc_pb2.HashResponse()
        response.hash = h
        return response


def serve():
    print("Starting GRPC Example Server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calc_pb2_grpc.add_CalcerServicer_to_server(CalcerServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
