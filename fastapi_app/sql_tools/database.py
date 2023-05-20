import os
import json
import pymongo
import numpy as np

SECRET_STRING = "mongodb+srv://test:test431279@test.byytc4h.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(SECRET_STRING)
db = client["mts"]


def _serialize_data_from_db(data):
    "serialises data from db for json, converts objectids to strings"
    data = json.loads(json.dumps(data, default=str))
    return data


def get_collection(collection_name):
    return db[collection_name]


def save_entries_from_collection_to_jsonfile(col_name, jsonfile_name):
    col = get_collection(col_name)
    entries = col.find()
    with open(jsonfile_name, "w") as writer:
        for entry in entries:
            entry = _serialize_data_from_db(entry)
            writer.write(json.dumps(entry, indent=4))
            writer.write("\n")


def get_entries_from_collection(col_name):
    col = get_collection(col_name)
    entries = col.find()
    entries = [_serialize_data_from_db(entry) for entry in entries]
    return entries


def get_one_entry_from_collection(col_name, field_to_search, value):
    col = get_collection(col_name)
    query = {field_to_search: value}
    entry = col.find_one(query)
    entry = _serialize_data_from_db(entry)
    return entry


def create_entry_in_collection(col_name, entry):
    col = get_collection(col_name)
    col.insert_one(entry)


def create_user(user):
    col = get_collection("users")
    data = _serialize_data_from_db(user)
    col.insert_one(data)
    return True


def edit_user(user):
    col = get_collection("users")
    update_entry(col, user, field_to_search="login")
    return True


def update_entry(collection, new_dict, field_to_search='key'):
    """Updates a document in a MongoDB, using the specified field"""
    # Find the document to update
    query = {field_to_search: new_dict[field_to_search]}
    old_doc = collection.find_one(query)

    # Update the document with the new fields and values
    if old_doc is not None:
        new_doc = {**old_doc, **new_dict}
        collection.replace_one(query, new_doc)


def add_entry_from_json(collection, json_file):
    """Creates a new document in a MongoDB, using the specified field"""
    with open(json_file, "r") as reader:
        new_data = json.load(reader)
    collection.insert_one(new_data)


if __name__ == "__main__":
    pass
    # save_entries_from_collection_to_jsonfile("users", "users.json")

    # collection = get_collection("users")
    # update_entry(collection, {"login": "user44466", "username": "john"}, field_to_search="login")
    # res = get_entries_from_collection("users")
    # print(res)
