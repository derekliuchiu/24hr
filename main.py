from selScraper import check_price
from texter import texter

def main():

    auto_mall = check_price("AutoMall")
    milpitas = check_price("Milpitas")
    if auto_mall:
        texter("AutoMall", True)
    if milpitas:
        texter("Milpitas", True)
    else:
        if auto_mall == None:
            texter("AutoMall", False)
        if milpitas == None:
            texter("Milpitas", False)
    print("ran")
if __name__ == "__main__":
    main()
