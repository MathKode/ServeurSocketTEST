import argparse

parser = argparse.ArgumentParser(description='LOLLLL')
parser.add_argument('-s','--server',metavar='IP',type=str,help="The IP of the server machine")
parser.add_argument('-f','--file',metavar='name',default="File Value by default",type=str,help="The name of the file")

args = parser.parse_args()

if __name__ == "__main__":
    print("Connection to the server : ", args.server)
    print(args.file)