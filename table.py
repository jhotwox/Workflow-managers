def max_length(l: list, columns: int) -> list:
    # Llenar la lista con ceros, con la misma longitud de la lista de entrada es decir l[0]
    if columns == 0:
        res: list = [0 for i in range(len(l[0]))]
    else:
        res: list = [0 for i in range(columns)]
        
    for ob in l:
        for index, item in enumerate(ob):
            if len(item) > res[index]:
                res[index] = len(item)
    return res

# TODO:
# - Combinar con la función max_length
# - Cambiar comprobación de lista y tupla para que se puedan combinar
def convert_to_string(l: list | tuple) -> list:
    if not l:
        raise Exception("Error: The list is empty")
    if not all(isinstance(i, list) for i in l) and not all(isinstance(i, tuple) for i in l):
        raise Exception("Error: The list is not a list of lists or a list of tuples")
    
    res = []
    for ob in l:
        aux = []
        for i in ob:
            if not isinstance(i, str):
                try:
                    i = str(i)
                except Exception as e:
                    print("[-] convert_to_string Err:", e)
                    print("item:", i)
                    raise Exception("Error: The list contains elements that cannot be converted to string") from e
            aux.append(str(i))
        # print([type(i) for i in aux])
        res.append(aux)
    return res

def table(l: list, columns: int = 0, header: bool = False) -> None:
    list_converted = convert_to_string(l)
    max_len: list = max_length(list_converted, columns)
    
    def print_line():
        print("+" + "-" * (sum(max_len) + len(max_len)*3 - 1) + "+")
    
    print_line()
    for i, ob in enumerate(list_converted):
        print("|", end="")
        for index, item in enumerate(ob):
            print(f" {item}{' ' * (max_len[index] - len(item))} |", end="")
        print()
        if header and i == 0:
            print_line()
    print_line()

if __name__ == "__main__":
    test = [
        [1, 1, 'delectus aut autem', 0],
        [1, 2, 'quis ut nam facilis et officia qui', 1],
        [1, 3, 'fugiat veniam minus', 0],
        [1, 4, 'et porro tempora', 1],
        [1, 5, 'laboriosam mollitia et enim quasi adipisci quia provident illum', 0]
    ]
    todo1 = [
        (1, 1, 'delectus aut autem', 0),
        (1, 2, 'quis ut nam facilis et officia qui', 0),
        (1, 3, 'fugiat veniam minus', 0),
        (1, 5, 'laboriosam mollitia et enim quasi adipisci quia provident illum', 0),
        (1, 6, 'qui ullam ratione quibusdam voluptatem quia omnis', 0)
    ]
    # try:
    #     convert_to_string(test)
    # except Exception as e:
    #     print("Error:", e)
    # try:
    #     print(convert_to_string(test))
    # except Exception as e:
    #     print("Error:", e)
    try:
        todo1.insert(0, ["userId", "id", "title", "completed"])
        table(todo1)
    except Exception as e:
        print(e)