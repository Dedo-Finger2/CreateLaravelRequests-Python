# Código de criação de requests do Laravel.
# padrão de nome para validação de inserção: Store{Model}Request
# padrão de nome para validação de atualização: Update{Model}Request

import os
from jinja2 import FileSystemLoader, Environment

# Pega o caminho do template
template_dir: str = "C:\\Users\\anton\\Documents\\PyCharmProjects\\CreateLaravelRequests"
file_loader = FileSystemLoader(template_dir)
env = Environment(loader=file_loader)

# Guarda o arquivo do template
template = env.get_template('template.txt')

# Troca os valores das variáveis dentro do arquivo
template_variables = {
    'NomeArquivo': None,
    'Permissao': 'true',
    'NomeModel': None,
    'Acao': None
}

# Diretório dos Models
models_dir: str = "C:\\laragon\\www\\Sistema-TCC-2023\\app\\Models"

# Listar todos os Models
all_models = os.listdir(models_dir)
models_name = []

# Para cada Model
for model in all_models:
    # Guardar apenas o nome do Model numa lista
    if model == "User.php":
        continue
    models_name.append(model)

# Diretório dos Controllers
controllers_dir: str = "C:\\laragon\\www\\Sistema-TCC-2023\\app\\Http\\Controllers"
# Listar todos os Controllers
all_controllers = os.listdir(controllers_dir)
controllers_name = []
for controller in all_controllers:
    if controller == "Controller.php" or controller == "TestingController.php":
        continue
    controllers_name.append(controller)

# Diretório de Requesets
requests_dir: str = "C:\\laragon\\www\\Sistema-TCC-2023\\app\\Http\\Requests"

# Para cada Model
for model in models_name:
    # Criar arquivo de validação de inserção
    store_request_model_name = "Store"+model[:-4]+"Request.php"
    store_request_path = os.path.join(requests_dir, store_request_model_name)

    # Configura as variávies
    template_variables['Acao'] = 'insercao'
    template_variables['NomeArquivo'] = store_request_model_name[:-4]
    template_variables['NomeModel'] = model[:-4]

    # Renderiza os valores nas variáveis
    store_output = template.render(template_variables)

    # Cria novo arquivo de store
    with open(store_request_path, 'w') as store_request_file:
        # Jogar arquivo dentro da pasta de Requests
        store_request_file.write(store_output)

    # Criar arquivo de validação de atualização
    update_request_model_name = "Update" + model[:-4] + "Request.php"
    update_request_path = os.path.join(requests_dir, update_request_model_name)

    # Configura as variávies
    template_variables['Acao'] = 'atualizacao'
    template_variables['NomeArquivo'] = update_request_model_name[:-4]

    # Renderiza os valores nas variáveis
    update_output = template.render(template_variables)

    # Cria novo arquivo de update
    with open(update_request_path, 'w') as update_request_file:
        # Jogar arquivo dentro da pasta de Requests
        update_request_file.write(update_output)

# Para cada Controller
for controller in controllers_name:
    # Pegar arquivo
    controller_path = os.path.join(controllers_dir, controller)

    # Pegar conteúdo do arquivo
    with open(controller_path, 'r') as file:
        controller_content = file.readlines()

    with open(controller_path, 'w') as file:
        # Para cada linha do conteúdo
        for line in controller_content:
            # Adiciona a importação dos arquivos substituindo o request padrão
            if 'use Illuminate\\Http\\Request' in line:
                line = line.replace('use Illuminate\\Http\\Request', f'use App\\Http\\Requests\\Store{controller[:-14]}Request;\nuse App\\Http\\Requests\\Update{controller[:-14]}Request')
            # Substituir 'store(Request' por 'store(Store{Model}Request'
            if 'store(Request' in line:
                line = line.replace('store(Request', f'store(Store{controller[:-14]}Request')
            # Substituir 'update(Request' por 'update(Update{Model}Request'
            if 'update(Request' in line:
                line = line.replace('update(Request', f'update(Update{controller[:-14]}Request')
            file.write(line)
