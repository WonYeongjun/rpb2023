def add(a,b):
    return a+b
def multiply(a,b):
    return a*b
def minus(a,b):
    return a-b
def divide(a,b):
    return a/b   

def main():
    print("This is calculator")
    
    print("Choose your operator as a number (1=add, 2=minus, 3=multiply, 4=divide)")
    opttype = int(input("> "))
    x=int(input("x > "))
    y = int(input("y > "))
    print("You chose ")
    if (opttype == 1):
        print("addition.")
        z=add(x,y)
        print("%d+%d=%d" % (x,y,z))
    elif (opttype==2):
        print("minus")
        z=minus(x,y)
        print("%d-%d=%d" % (x,y,z))
    elif (opttype==3):
        print("multiply")
        z=multiply(x,y)
        print("%d*%d=%d" % (x,y,z))
    else:
        print("divide")
        z=divide(x,y)
        print("%d/%d=%d" % (x,y,z))
    

if __name__ == "__main__":
    main()
