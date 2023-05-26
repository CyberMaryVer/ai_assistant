import os

KEY_PATH = "fastapi_app/chatbot/fake_keys"


def check_key(key, key_path=KEY_PATH):
    keys = os.listdir(key_path)
    keys = [k for k in keys if not k.endswith(".py")]
    return key in keys


def use_key(key, key_path=KEY_PATH):
    if check_key(key, key_path):
        with open(os.path.join(key_path, key), "r") as reader:
            count = reader.read()
            if int(count) == 0:
                return {"error": "Key is out of uses"}
            count = int(count) - 1
        with open(os.path.join(key_path, key), "w") as writer:
            writer.write(str(count))
        return {"success": "Key is used", "uses_left": count}
    else:
        return {"error": "Key is not found"}


if __name__ == "__main__":
    r = use_key(key='5', key_path="./../fake_keys")
    print(r)
    r = use_key(key='11111test', key_path="./../fake_keys")
    print(r)
