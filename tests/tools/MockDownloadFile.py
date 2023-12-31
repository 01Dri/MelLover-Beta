
def create_file_test(path):
    full_path = f"{path}/teste.txt"
    with open(full_path, "w") as file:
        file.write("escrevi algo aqui")


