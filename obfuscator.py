import base64, random, string, zlib


def random_gen(N):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(N))


fn = input("file name > ")
size = int(input("c size  >"))

"""
    string obfuscation method
        :base64.b64decode(b'd2l0YWo=').decode()
"""
with open(fn, "r") as f:
    data = f.readlines()


num = 0
for n in data:

    if n == '\n' or n == "\n":
        data.remove(n)
    elif n.startswith("#"):
        data.pop(num)


    num += 1

"""
    :string conv
"""
num = 0
is_string = False
is_multi_string = False
multi_string_count = 0
saving_string = ""
to_replace = []
for e in data:
    for f in e:
        if f == "\"":
            is_string = not is_string

        if is_string:
            saving_string += f
    if not saving_string == "":
        saving_string.replace("\"", "").strip()
        saving_string = saving_string[1:]
        to_replace.append(saving_string)
        saving_string = ""
    num += 1
num = 0
for g in data:
    for g_ in to_replace:
        if g_ in g:
            lane = g.find(g_) - 1
            if not lane == 0:
                length = len(g_) + 2
                encoded_string = base64.b64encode(g_.encode())
                to_save = f"{g[:lane]}base64.b64decode({encoded_string}).decode(){g[lane + length:]}"

                data[num] = to_save

    num += 1

"""
    : random - 3
    : x 16
    : base64
    : compyle <string>
"""



code = {}
for b in data:
    code[random_gen(size if not size == 0 else 24)]=base64.b64encode(zlib.compress(b.encode('utf-8'))).decode('utf-8')


print(code)
with open(f"{fn.split('.')[0]}-obf.py", "w") as out:
    out.write("import base64,zlib;")
    to_write = f""
    to_exec = f""
    num = 1
    for x in code:
        print(f"{num} {len(code)}")
        to_write += f"{x}=b'{code[x]}';"
        if not num == len(code):
            to_exec += f"zlib.decompress(base64.b64decode({x}))+"
        else:
            to_exec += f"zlib.decompress(base64.b64decode({x}))"
        num += 1
    to_write += f"exec({to_exec})"
    encoded = zlib.compress(base64.b64encode(to_write.encode()))
    print(encoded)
    out.write(f"exec(base64.b64decode(zlib.decompress({encoded})))")
    #out.write(to_write)


print()


