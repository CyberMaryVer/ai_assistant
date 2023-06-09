import os


def add_examples(openapi_schema: dict, docs_dir):
    path_key = 'paths'
    code_key = 'x-codeSamples'
    lable_lang_mapping = {"Python": "Python",
                          "NodeJS": "JavaScript",
                          "React": "JavaScript",
                          "__info": "Markdown",
                          }

    for folder in os.listdir(docs_dir):
        base_path = os.path.join(docs_dir, folder)
        files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
        for f in files:
            parts = f.split('-')
            if len(parts) >= 2:
                route = '/' + '/'.join(parts[:-1]) + '/{user_id}'
                method = parts[-1].split('.')[0]
                print(f'[{path_key}][{route}][{method}][{code_key}]')

                if route in openapi_schema[path_key]:
                    print(f'Adding examples code to openapi {f}')
                    if code_key not in openapi_schema[path_key][route][method]:
                        openapi_schema[path_key][route][method].update({code_key: []})

                    openapi_schema[path_key][route][method][code_key].append({
                        'lang': lable_lang_mapping[folder],
                        'source': open(os.path.join(base_path, f), "r").read(),
                        'label': folder,
                    })
                else:
                    print(f'Example code wasn\'t added to {route} in openapi.\n'
                          f'Your Code key: {code_key}\n'
                          f'Openapi Path: {path_key}\n'
                          f'Openapi Route: {route}\n')
                    # print(f'Openapi Method: {openapi_schema["paths"].keys()}\n')
            else:
                print(f'Error in adding examples code to openapi {f}')

    return openapi_schema
