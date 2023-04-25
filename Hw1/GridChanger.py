from Environment import Environment


def change(env: Environment, row: int, col: int, node: str, file_name: str):
    """
        Change the Grid and save
    :param env: Environment object
    :param row: Row index
    :param col: Column index
    :param node: New node
    :param file_name: File name
    :return: Nothing
    """
    env.grid[row][col] = node.upper()

    file_name = file_name[:-4]

    env.save(file_name)


if __name__ == "__main__":
    file_name = input("File Name: ")

    env = Environment(file_name)

    while True:
        row = int(input("Row:"))
        col = int(input("Col:"))

        if row == -1 or col == -1:
            break

        node = input("Node:")

        change(env, row, col, node, file_name)
