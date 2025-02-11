def main():
    print("Let's implement addition. Type two numbers for x and y.")

    x = int(input("x > "))
    y = int(input("y > "))
    
    print("%d + %d = %d" % (x, y, add(x, y)))    
    #몰라몰라몰라ㅋㅋ
def add(x,y):
    return x+y
    
if __name__ == "__main__":
    main()

