import grpc
import calc_pb2
import calc_pb2_grpc
import random
from time import sleep
import time


def getInputFromUser():
    a = input("Enter value a: ")
    b = input("Enter value a: ")
    try:
        a = int(a)
        b = int(b)
    except Exception as e:
        print(e)
        print("No valid values entered, starting again!")
        return None, None
    return a, b


def randomDigits():
    i = 1
    sum = 0
    while i < 10:
        a = random.randint(1, 10)
        sum += a
        request = calc_pb2.Digits(a=a, counter=i)
        print(f"Request {i}: {a}")
        yield request
        i += 1
    print(f"Expected result: {sum}")


def readFile():
    file = "client.py"
    with open(file, 'rb') as f:
        file = f.read()
    return file


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = calc_pb2_grpc.CalcerStub(channel)
        # selection = input("What do you want to calc today + (1), - (2), * (3), / (4), stream random digits to server, get one reply (5), ... get intermediate values (6) ")
        selection = "7"
        if selection == "1":
            print("Adding it is")
            a, b = getInputFromUser()
            request = calc_pb2.CalcRequest(a=a, b=b)
            response = stub.Add(request)
            print(response)
        elif selection == "2":
            print("Subtraction it is")
            a, b = getInputFromUser()
            request = calc_pb2.CalcRequest(a=a, b=b)
            response = stub.Subtract(request)
            print(response)
        elif selection == "3":
            print("Multiplication it is")
            a, b = getInputFromUser()
            request = calc_pb2.CalcRequest(a=a, b=b)
            response = stub.Multiply(request)
            print(response)
        elif selection == "4":
            a, b = getInputFromUser()
            request = calc_pb2.CalcRequest(a=a, b=b)
            response = stub.Divide(request)
            print(response)
        elif selection == "5":
            # client streams digits to server, server creates *one* response
            print("Streaming random values")
            response = stub.MultiPlus(randomDigits())
            print(response)
        elif selection == "6":
            # client streams digits to server, server sends back intermediate responses and one final response
            print("Streaming random values")
            responses = stub.InteractiveMultiPlus(randomDigits())
            for response in responses:
                print(response)
        elif selection == "7":
            count = 10000
            durationTotal = 0
            while count > 0:
                start = time.time()
                request = calc_pb2.FileRequest(file=readFile())
                response = stub.HashFile(request)
                end = time.time()
                duration = end - start
                durationTotal += duration
                count -= 1
            print(durationTotal)
            print(response)


if __name__ == "__main__":
    run()
