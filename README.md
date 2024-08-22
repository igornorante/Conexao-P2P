Cliente de Chat em Arquitetura Cliente-Servidor

Este projeto implementa um cliente de chat para comunicação em uma arquitetura cliente-servidor, permitindo que os usuários se conectem a um servidor central, visualizem outros usuários online e estabeleçam conexões P2P para troca de mensagens.
Funcionalidades

    Conexão com o Servidor: O cliente se conecta a um servidor central utilizando um socket TCP, enviando um nome de usuário e configurando uma porta aleatória para conexões P2P.

    Listagem de Usuários Online: Comando /list para solicitar ao servidor uma lista dos usuários atualmente conectados, que é processada e exibida no cliente.

    Conexão P2P: O cliente pode iniciar um chat P2P com outro usuário através do comando /chat, estabelecendo uma conexão direta para troca de mensagens. A conexão é encerrada com o comando /bye.

    Keep Alive: O cliente envia periodicamente mensagens "KEEP" ao servidor para manter a conexão ativa.

    Encerramento: A conexão com o servidor é finalizada com o comando /exit.

Estrutura de Implementação

    Inicialização e Conexão: O cliente importa as bibliotecas necessárias, define o IP e a porta do servidor, cria um socket TCP e se conecta ao servidor. Um socket UDP também é criado para receber conexões P2P.

    Multithreading: O cliente utiliza threads para lidar com o recebimento de mensagens de outros clientes e para enviar mensagens "keep alive" ao servidor, garantindo a operação contínua sem interrupções.

    Tratamento de Erros: Implementa tratamento básico de erros, incluindo desconexões inesperadas e nomes de usuário inválidos.

Como Funciona

    Inicie o Cliente: O cliente solicita o nome de usuário, gera uma porta aleatória e se conecta ao servidor central.
    Lista de Usuários Online: Utilize o comando /list para visualizar outros usuários conectados.
    Inicie um Chat P2P: Com o comando /chat, estabeleça uma conexão direta com outro usuário.
    Keep Alive: O cliente envia mensagens "KEEP" automaticamente para o servidor, mantendo a conexão ativa.
    Encerramento: Feche o cliente com o comando /exit.

Observações

    Esta implementação assume que o servidor está configurado para processar as mensagens "USER", "LIST", "ADDR" e "KEEP".
    O arquivo cliente.txt contém todos os detalhes da implementação, incluindo a configuração inicial, funcionalidades principais e estrutura de threads.
