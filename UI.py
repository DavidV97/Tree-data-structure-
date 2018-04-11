from Manager import Manager


def start():
    exit = True

    while exit:

        menu()
        option = get_option()
        exit = execute_menu(option)


def menu():
    print("____________Menu principal____________\n")
    print("1. Agregar datos en una estructura\n")
    print("2. Eliminar datos en una estructura\n")
    print("3. Mostrar datos de una estructura\n")
    print("0. Salir\n")
    print("______________________________________\n")


def get_option():

    option = input("Digite una opcion: ")

    return option


def execute_menu(option):
    exit = True
    operation = ""

    if option == "1":
        operation = "Add"
        add_delete_show_menu(operation)
        option = get_option()
        execute_add_delete_show(option, operation)

    elif option == "2":

        operation = "Delete"
        add_delete_show_menu(operation)
        option = get_option()
        execute_add_delete_show(option, operation)

    elif option == "3":

        operation = "Show"
        add_delete_show_menu(operation)
        option = get_option()
        execute_add_delete_show(option, operation)

    elif option == "0":

        exit = False
        print("Gracias...")

    else:
        print("*Opcion invalida*")

    return exit


def add_delete_show_menu(operation):
    operation = get_ES_name(operation)

    print("____________" + operation + " datos____________\n")
    print("1. En un arbol B\n")
    print("2. En un arbol AVL\n")
    print("3. En un arbol B+\n")
    print("4. En un arbol Rojo-Negro\n")
    print("0. <-\n")
    print("______________________________________")


def get_ES_name(operation):
    if operation == "Add":
        return "Agregar"
    elif operation == "Delete":
        return "Eliminar"
    else:
        return "Mostrar"


def execute_add_delete_show(option, operation):
    strcuk_type = ""

    if option == "1":
        strcuk_type = "B"
        execute_operation(operation, strcuk_type)

    elif option == "2":
        strcuk_type = "AVL"
        execute_operation(operation, strcuk_type)

    elif option == "3":
        """
        strcuk_type = "B+"
        execute_operation(operation, strcuk_type)
        """
        pass

    elif option == "4":
        strcuk_type = "Rojo-Negro"
        execute_operation(operation, strcuk_type)

    elif option == "0":
        pass

    else:
        print("Opcion invalida")


def execute_operation(operation, struck_type):
    num = 0

    if operation == "Add" or operation == "Delete":

        num = get_input()

        if operation == "Add":
            print(str(Manager.add_item(num, struck_type)))
        else:
            print(str(Manager.delete_item(num, struck_type)))
    else:
        print(str(Manager.show_item(struck_type)))


def get_input():

    success = True

    while success:
        try:
            option = int(input("Digite el numero: "))
            success = False

        except ValueError:
            print("El numero debe ser entero")

    return option


if __name__ == "__main__":
    start()
