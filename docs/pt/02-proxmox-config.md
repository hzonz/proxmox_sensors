# 🔐 Passo 2: Configuração de Usuários e Permissões

**Para que o Home Assistant se comunique com o Proxmox de forma segura, é recomendável não usar o usuário root. Criaremos um usuário dedicado e atribuiremos as permissões necessárias para que a integração funcione a 100%.**

> ⚠️ **IMPORTANTE:**  
> Devido às funções avançadas da integração (controle de VMs/CTs, backups individuais e em massa, ações PBS…), é necessário atribuir **permissões de administrador** tanto no PVE quanto no PBS.

---

## 1. Diferença entre PVE e PBS

### **Proxmox VE (PVE)**
- Você pode usar **Usuário/Senha** ou **Token da API**.  
- O usuário deve ter a função **PVEAdmin**.

### **Proxmox Backup Server (PBS)**
- É **obrigatório** usar um **Token da API**.  
- O usuário deve ter a função **Administrator** (o PBS não possui uma função intermediária válida).

---

## 2. Criação do Usuário

1. Vá para **Datacenter → Permissions → Users**  
2. Clique em **Add**  
3. Configure:  
   - **User:** `homeassistant`  
   - **Realm:** `pve`  
   - **Password:** apenas se você for usar login por senha no PVE  
4. Salve as alterações

---

## 3. Atribuição da Função Correta

1. Vá para **Datacenter → Permissions**  
2. Clique em **Add → User Permission**  
3. Configure os seguintes campos:

### ✔ Para PVE:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

### ✔ Para PBS:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

> 💡 **Por que `/` é necessário:**  
> A integração precisa de acesso global para ler nós, VMs, CTs, discos, datastores e tarefas.

---

## 4. Geração do Token da API (Obrigatório para PBS)

1. Vá para **Datacenter → Permissions → API Tokens**  
2. Clique em **Add**  
3. Configure:  
   - **User:** `homeassistant@pve`  
   - **Token ID:** `ha-token`  
   - **Privilege Separation:** **desmarcado**  
   - **Expire:** **Never**  
4. Ao criar o token, o Proxmox exibirá:  
   - **Token ID**  
   - **Secret** (exibido apenas uma vez)

> [!WARNING]
> **Copie o "Secret" agora e guarde-o em um local seguro.** Depois que você fechar esta janela, o Proxmox nunca mais o mostrará novamente por motivos de segurança.

> [!TIP]
> ### 💡 Esqueceu de copiar o Secret?
> Não se preocupe. Embora o Proxmox não o mostre novamente por motivos de segurança, você não precisa excluir o token e começar do zero:
> 
> 1. Na lista **API Tokens**, selecione o token que você já criou.
> 2. Clique no botão **Regenerate**.
> 3. O sistema invalidará imediatamente a chave antiga e fornecerá um **novo Secret**.
> 
> *Lembre-se de que, se você regenerar o Secret, deverá atualizá-lo na configuração do Home Assistant para que a integração possa se reconectar.*
