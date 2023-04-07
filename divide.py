def main():
    print("Let's implement division. Type two numbers for x and y")
    
    x = int(input("x > "))
    y = int(input("y > "))
    
    print("%d / %d = %0.3f" % (x, y, divide(x, y)))
    
    
    
# TODO: divide() 함수 정의
def divide (a, b):
    if b==0:
        print("Error: cannot divide by zero.")
        return()
    else:
        return a / b


if __name__ == "__main__":
    main()

