
# MessagePack関連のユーティリティ。

import msgpack

def load(filename):
    with open(filename, "rb") as file:
        return msgpack.unpackb(file.read(), encoding="utf-8")

def dump(filename, data):
    with open(filename, "wb") as file:
        file.write(msgpack.packb(data))
