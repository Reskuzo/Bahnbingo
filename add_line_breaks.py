
with open(r'./tasks.txt', "r", encoding="utf-8") as tasks_file:
    new_lines = []
    for line in tasks_file.readlines():
        text = line.split(";")[2][:-1]
        line = line.split(";")[0] + ";" + line.split(";")[1] + ";"
        result = ""
        for word in text.split(" "):
            if len(result) + len(word) > 18:
                line += result + "\\"
                result = word + " "
            else:
                result += word + " "
        line += result
        new_lines += [line + "\n"]

with open(r'./tasks.txt', "w", encoding="utf-8") as tasks_file:
    tasks_file.writelines(new_lines)
