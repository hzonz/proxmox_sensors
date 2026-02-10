# 🔌 Passo 3: Instalação da Integração no Home Assistant

Para visualizar os dados (incluindo temperaturas, sensores de hardware, discos, PBS, VMs e CTs), usaremos a integração **Proxmox Extended Sensors**.

[Guia Visual de Instalação](#-Guia-Visual-de-Instalação)

---

## 1. Instalação via HACS

Por ser uma integração personalizada, primeiro precisamos adicioná-la ao HACS:

1. Vá para **HACS → Integrações**  
2. Clique nos **três pontos** (canto superior direito)  
3. Selecione **Repositórios personalizados**  
4. Adicione este repositório: `https://github.com/Javisen/proxmox_sensors/`
5. Em **Categoria**, selecione `Integração`  
6. Instale e **reinicie o Home Assistant**

---

## 2. Configuração da Integração

Após a reinicialização:

1. Vá para **Configurações → Dispositivos e Serviços**  
2. Clique em **Adicionar integração**  
3. Pesquise por **Proxmox Extended Sensors**

---

## 3. Dados de Conexão

O formulário é simples, mas há detalhes importantes:

### 🔹 Host
- **Na rede local:** apenas o IP → `192.168.1.50`  
*(Não adicione porta ou http/https)*  
- **Externamente:** seu domínio → `proxmox.meudominio.com`  
*(A integração detecta automaticamente http/https)*

### 🔹 Tipo de servidor
- **PVE** → Proxmox Virtual Environment  
- **PBS** → Proxmox Backup Server  

### 🔹 Método de autenticação
- **Login tradicional** (somente PVE)  
- **Token da API** (obrigatório para PBS)

---

## 🔐 Opção A: Login com Usuário (sem Token)

Válido apenas para **PVE**.

Campos:

- **Usuário:** `usuario@realm`  
Exemplos:  
- `homeassistant@pve`  
- `root@pam`  
- **Senha:** a senha do usuário  
- **Nome do Nó:** nome do nó (como aparece no Proxmox)

---

## 🔐 Opção B: Login com Token (recomendado e obrigatório para PBS)

Campos:

- **Usuário:** `usuario@realm`  
- **token_id:** apenas o nome do token → `ha-token`  
*(Não coloque `usuario@pve!token`)*  
- **Token_secret:** o Secret gerado pelo Proxmox  

---

## ✅ Seleção de Entidades (somente no PVE)

Após a conexão, a integração escaneará seu servidor e você poderá escolher o que monitorar:

- **VMs**  
- **CTs**  
- **Discos físicos**  
- **Armazenamentos**

> [!TIP]  
> Selecione apenas o que você precisa para manter o Home Assistant limpo e rápido.

---

## 🧭 Guia Visual de Instalação

**Abaixo você encontrará um guia visual completo do processo de configuração, incluindo métodos de login, seleção de recursos e etapas de configuração.**

<details>
  <summary>🪪 Captura de tela: Conexão do Servidor</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Não use "http://" ou "https://". Já cuidamos disso para você.
</details>

<details>
  <summary>🪪 Captura de tela: Login via Usuário e Senha (somente PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Certifique-se de usar o realm `pam` ou `pve` conforme a configuração do seu usuário.
</details>

<details> 
  <summary>🪪 Captura de tela: Login via Usuário e Token (PVE e PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **No campo Token_id, insira apenas o nome do token**
</details>

<details>
  <summary>⚙️ Captura de tela: Seleção de Recursos</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Login Proxmox" width="600">
  </p>
  *Nota: Selecione os CTs, VMs e Armazenamentos que deseja adicionar, bem como as opções*
</details>

---

## ⚠️ Nota importante para PBS em ambientes compartilhados (Tuxis, Hetzner, etc.)

Se você usa um PBS **gerenciado** ou **multi‑tenant**, como o Tuxis Free PBS:

- Você não verá sensores de hardware  
- Você não verá temperaturas  
- Você não verá discos físicos  
- Você não verá métricas do nó  

Isso é normal porque:

- Você não tem acesso ao hardware real  
- O provedor oculta a infraestrutura  
- Você não tem permissões de root  
- Você não pode acessar o sistema de arquivos real  

**Resultado:**  
A integração mostrará apenas sensores vazios ou nenhum dado.  
Em versões futuras, tentaremos exibir métricas personalizadas do datastore.
