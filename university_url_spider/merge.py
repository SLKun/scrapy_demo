import sys
import json



def main():
    arg_list = ["A_filename", "B_filename", "AandB_filename", "AexB_filename", "BexA_filename"]
    if len(sys.argv) <= 1:
        A_filename = "A.json"
        B_filename = "B.json"
        AandB_filename = "A+B.json"
        AexB_filename = "A-B.json"
        BexA_filename = "B-A.json"
    else:
        for i in range(1, len(sys.argv)):
            setattr(self, "test", "wqqw")

    print(vars())

    A = open(A_filename).read()
    B = open(B_filename).read()
    A_json = json.loads(A)
    B_json = json.loads(B)

if __name__ == '__main__':
    main()