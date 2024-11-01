import os, argparse, dotenv

parse = argparse.ArgumentParser("run code")
parse.add_argument("prog", type=str, help="compiler/interpreter to use for runing your code [g++, python (py), node, ]")
parse.add_argument("-i", "--index", type=int, help="index of an element of a sorted list")
parse.add_argument("-n", "--name", type=str, help="name of an file of a sorted list")
parse.add_argument("-a", "--arguments", type=str, help="extra argumensts")

dotenv.load_dotenv()

PYTHON_PATH = os.getenv("PYTHON_PATH")
CPP_PATH = os.getenv("CPP_PATH")
NODE_PATH = os.getenv("NODE_PATH")
RUST_PATH = os.getenv("RUST_PATH")


PY = ["python", "py"]
CPP = ["g++", "cpp", "c++"]
JS = ["js", "node"]
RUST = ["rust", "rs"]

args = parse.parse_args()
dir = os.getcwd()



def get_items(endsW):
    files = []
    for filenames in os.listdir(dir):
        if filenames.endswith(endsW):
            files.append(filenames)
    return files

def get_user_index(lst):
    l = len(lst)
    if l < 1:
        exit("there are no items here")

    for i, item in enumerate(lst):
        print(f"{i}. {item}")

    while True:
        if l == 1:
            return 0
        
        index = int(input("index: "))
        if 0 <= index < l:
            return index 


def get_item(files, index):
    try:
        return files[index]
    except IndexError:
        print("index out of range")

def filter_items():
    items = []
    if args.prog in PY:
        items.extend(get_items(".py"))
        language = "python"
    elif args.prog in CPP:
        items.extend(get_items(".cpp"))
        language = "cpp"
    elif args.prog in JS:
        items.extend(get_items(".js"))
        language = "js"
    elif args.prog in RUST:
        items.extend(get_items(".rs"))
        language = "rust"
    else:
        print("wrong argument")
        exit(1)
        
    items.sort()
    
    if args.index:
        return (get_item(items, args.index), language)
    elif args.name:
        itms = []
        for item in items:
            if args.name in item:
                itms.append(item)
        if len(itms) == 1:
            return itms[0], language
    
    
    index = get_user_index(items)
    return get_item(items, index), language

def main():
    filename, language = filter_items()
    if not os.path.exists(filename):
        exit(2)
        
    
    full_path = os.path.join(dir, filename)
    arg = ""
    if args.arguments:
        arg = args.arguments
    match language:

        case "python":
            command = f"{PYTHON_PATH} {full_path} {arg}"
            os.system(command)
            exit(0)
           
        case "cpp":
            save_as = filename.split('.')[0]
            command = f"{CPP_PATH} {full_path} -o {save_as} && ./{save_as} {arg}"
            os.system(command)
            exit(0)
           
        case "js":
            command = f"{NODE_PATH} {full_path} {arg}"
            os.system(command)
            exit(0)


        case "rust":
            command = f"{RUST_PATH} run {full_path} -- {arg}"
            os.system(command)
            exit(0)
        
        
    exit(3)
        
        
    
        
        
if __name__ == "__main__":
    main()