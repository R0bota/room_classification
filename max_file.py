def col(n):
    if n % 2 == 0:
        n = n / 2
    else:
        n = 3 * n + 1

    if n == 1:
        print("DONE")
        return
    print(n)
    col(n)

col(1234556564332110)