# ❓ FAQ — Perguntas Frequentes

Aqui estão as dúvidas e problemas mais comuns ao usar a integração **Proxmox Extended Sensors**, juntamente com soluções rápidas.

---

## 🔐 Não consigo iniciar sessão na integração (PVE ou PBS)

### ✔ 1. Não insira `http://` ou `https://`
Digite apenas o domínio ou o IP, por exemplo:

192.168.1.10  
pve.meu-dominio.com

---

### ✔ 2. Não insira a porta
A integração detecta automaticamente a porta correta.

---

### ✔ 3. Verifique as permissões do usuário ou do Token API
O usuário deve ter:

- PVE: `PVEAdmin`  
- PBS: `Administrator`

As permissões devem ser atribuídas na raiz `/`.

---

### ✔ 4. Certifique-se de que o Token está ativo
Em Proxmox → Datacenter → Permissions → API Tokens  
Deve aparecer **Enabled: Yes**.

---

## 🔑 Aparece “Permission denied” mesmo com o Token correto

Isso geralmente ocorre porque:

### ✔ 1. O Token não tem permissões na raiz `/`
As permissões devem ser atribuídas em `/ (root)`  
Não em um nó específico.

### ✔ 2. O Token pertence a um usuário sem permissões
O usuário deve ter o papel `PVEAdmin` ou `Administrator`.

---

## 🌐 A integração não detecta meu PBS da Tuxis

Isso é normal.

Servidores PBS gerenciados pela Tuxis **não expõem métricas internas** via API:

- espaço do datastore  
- uso do disco  
- estatísticas RRD  
- hardware do nó  
- temperatura  
- SMART  
- CPU/RAM  

Isso não é um erro da integração.  
A Tuxis bloqueia esses endpoints por design.

A integração detecta automaticamente um PBS Tuxis e oculta sensores indisponíveis.

---

## 📦 Não vejo sensores de espaço do datastore no PBS

### ✔ Se o seu PBS é da Tuxis → esses dados não estão disponíveis
A Tuxis bloqueia o endpoint que retorna o estado do datastore.

Sem esse endpoint, não é possível obter:

- espaço total  
- espaço livre  
- porcentagem de uso  
- deduplicação  
- chunks  
- GC  

---

## 🌡️ Sensores de temperatura não aparecem no PVE

### ✔ 1. `lm-sensors` deve estar instalado no nó  
### ✔ 2. Você deve executar `sensors-detect`  
### ✔ 3. Você deve carregar os módulos recomendados  
Exemplo:

modprobe coretemp  
modprobe nct6775  

### ✔ 4. Você deve criar um serviço systemd  
Para que os sensores funcionem após reiniciar.

---

## 🖥️ Sensores NVMe/SSD/HDD não aparecem

### ✔ 1. O disco deve suportar leitura de temperatura  
Alguns modelos OEM não expõem sensores.

### ✔ 2. NVMe virtualizado em VMs não possui sensores  
Somente hardware físico fornece esses dados.

### ✔ 3. PBS da Tuxis não expõe sensores de disco  
Limitação do provedor.

---

## 🧠 Minhas VMs ou containers não aparecem

### ✔ 1. Verifique as permissões do usuário  
Ele deve ter o papel `PVEAdmin`.

### ✔ 2. Em clusters  
Você deve se conectar ao **nó principal**, não a um nó secundário.

---

## 🔄 A integração demora para atualizar os valores

Isso é normal.

A integração usa um coordenador interno para:

- evitar sobrecarga da API  
- reduzir carga no nó  
- melhorar desempenho  

O intervalo padrão é de 10 segundos (configurável).

---

## 🧩 Posso usar vários servidores PVE e PBS?

Sim.  
A integração permite várias instâncias, cada uma com seu próprio Token.

---

## 🔒 Tokens API são seguros?

Sim.

A integração:

- não armazena senhas  
- usa apenas Tokens  
- não executa comandos no servidor  
- não altera a configuração do Proxmox  
- não abre portas adicionais  

---

## 🧹 Como remover sensores antigos?

O Home Assistant remove automaticamente entidades órfãs.

Para forçar a limpeza:

1. Remova a integração  
2. Reinicie o Home Assistant  
3. Adicione a integração novamente  

---

## 🛠️ Onde posso reportar erros?

Abra um issue no GitHub com:

- versão do HA  
- versão do Proxmox  
- logs relevantes  
- passos para reproduzir  
- tipo de servidor (PVE, PBS, Tuxis, etc.)  

---

# 🧾 Checklist antes de abrir um Issue

Esta lista resolve 90% dos problemas:

### ✔ 1. Você consegue acessar o Proxmox pelo navegador?  
Se não, a integração também não conseguirá.

### ✔ 2. Está usando apenas domínio/IP?  
Nada de `http://`, `https://` ou portas.

### ✔ 3. O Token API está ativo?  
Deve mostrar **Enabled: Yes**.

### ✔ 4. O usuário tem permissões na raiz `/`?  
As permissões devem ser atribuídas em `/ (root)`.

### ✔ 5. `lm-sensors` está instalado e configurado?  
Sem isso, sensores de hardware não aparecerão.

### ✔ 6. Seu PBS é da Tuxis?  
Nesse caso, métricas internas não estão disponíveis.

### ✔ 7. Você reiniciou o Home Assistant após alterar permissões?  
O HA mantém permissões antigas em cache.

### ✔ 8. Há erros nos logs do HA?  
Verifique a seção “Integrações”.

### ✔ 9. Você testou no modo anônimo?  
O frontend do HA mantém cache por muito tempo.

---

# 🚫 Limitações Conhecidas

Essas limitações não são erros da integração, mas restrições do Proxmox ou do provedor.

---

### 🔒 1. PBS da Tuxis

PBS da Tuxis não expõe:

- espaço do datastore  
- uso do disco  
- deduplicação  
- chunks  
- estatísticas RRD  
- hardware do nó  
- temperatura  
- SMART  
- CPU/RAM  

A integração oculta automaticamente esses sensores.

---

### 🧊 2. Sensores de hardware em máquinas virtuais

VMs não expõem sensores reais:

- temperaturas  
- ventoinhas  
- voltagens  
- SMART  

Somente hardware físico fornece esses dados.

---

### 📦 3. NVMe/SSD sem sensores

Alguns modelos OEM ou controladoras RAID não expõem temperatura ou SMART.

---

### 🔐 4. Tokens sem permissões em `/`

Se as permissões forem atribuídas a um nó em vez da raiz, o Proxmox bloqueia a API.

---

### 🕒 5. Intervalos de atualização

A integração usa um intervalo mínimo para evitar sobrecarga da API.  
É normal que os valores demorem alguns segundos para atualizar.

---

### 🧩 6. Clusters Proxmox

Você deve se conectar ao **nó principal** do cluster.  
Nós secundários não expõem a API completa.

---

### 🌐 7. Certificados SSL autoassinados

A integração os aceita automaticamente, mas alguns navegadores podem exibir avisos.
