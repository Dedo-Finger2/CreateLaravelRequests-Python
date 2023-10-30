import os
from jinja2 import FileSystemLoader, Environment
from typing import Dict, List


def load_template(template_dir: str, template_name: str):
    file_loader = FileSystemLoader(template_dir)
    env = Environment(loader=file_loader)

    return env.get_template(template_name)


def create_request_file(template, requests_dir, model_name, action):
    request_model_name = f'{action.capitalize()}{model_name[:-4]}Request.php'
    request_path = os.path.join(requests_dir, request_model_name)

    template_variables = {
        'NomeArquivo': request_model_name[:-4],
        'Permissao': 'true',
        'NomeModel': model_name[:-4],
        'Acao': action
    }

    output = template.render(template_variables)

    with open(request_path, 'w') as request_file:
        request_file.write(output)


def update_controller_imports(controller_path, controller_name):
    with open(controller_path, 'r') as file:
        controller_content = file.readlines()

    with open(controller_path, 'w') as file:
        for line in controller_content:
            if 'use Illuminate\\Http\\Request' in line:
                line = line.replace('use Illuminate\\Http\\Request',
                                    f'use App\\Http\\Requests\\Store{controller_name[:-14]}Request;'
                                    f'\nuse App\\Http\\Requests\\Update{controller_name[:-14]}Request')
            if 'store(Request' in line:
                line = line.replace('store(Request', f'store(Store{controller_name[:-14]}Request')
            if 'update(Request' in line:
                line = line.replace('update(Request', f'update(Update{controller_name[:-14]}Request')
            file.write(line)


def main():
    template_dir = "C:\\Users\\anton\\Documents\\PyCharmProjects\\CreateLaravelRequests"
    models_dir = "C:\\laragon\\www\\Sistema-TCC-2023\\app\\Models"
    controllers_dir = "C:\\laragon\\www\\Sistema-TCC-2023\\app\\Http\\Controllers"
    requests_dir = "C:\\laragon\\www\\Sistema-TCC-2023\\app\\Http\\Requests"

    template = load_template(template_dir, 'template.txt')

    all_models = os.listdir(models_dir)
    all_controllers = os.listdir(controllers_dir)

    for model in all_models:
        if model != "User.php":
            create_request_file(template, requests_dir, model, 'store')
            create_request_file(template, requests_dir, model, 'update')

    for controller in all_controllers:
        if controller != "Controller.php" and controller != "TestingController.php":
            update_controller_imports(os.path.join(controllers_dir, controller), controller)


main()
