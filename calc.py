def add(a,b):
    return a+b
def multiply(a,b):
    return a*b
def main():
    print("This is calculator")
    
    print("Choose your operator as a number (1=add, 2=minus, 3=multiply, 4=divide)")
    opttype = int(input("> "))
    print("You chose ")
    if (opttype == 1):
        print("addition.")
    elif (opttype==2):
        print("minus")
    elif (opttype==3):
        print("multiply")
    else:
        print("divide")
if __name__ == "__main__":
    main()
