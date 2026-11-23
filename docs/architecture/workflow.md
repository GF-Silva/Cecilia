# Workflow

How the workflow of doing something work.
Notice that they are for me to follow this architecture, so can be classified as internal and i do not provide a english version.

Todo o desenvolvimento aqui apresentado deve seguir essa estrutura de planejamento e metodologia para preparar o que será feito corretamente. Lembrando que seguimos algo como a metodologia de desenvolvimento *Incremental* ou *Iterativa*

## Planejamento

### Contextualização

Nessa etapa contextualizamos o problema, de modo a definir o que será ou não feito.

1. **Dor:** Qual a dor que queremos resolver? Nessa etapa Define-se a dor que queremos resolver
2. **Afetados:** Quem precisa que essa dor seja resolvida? O que eles precisam? Nessa etapa pensamos nos afetados
3. **Escopo**: O que o sistema fará para resolver a dor para os afetados? O que ele não fará? Nessa etapa pensamos em como podemos resolver a dor deles
4. **Requisitos:** Quais são os requisitos para essa ação? Nessa etapa Define-se os requisitos para a ação ser um sucesso
5. **Ações:** Quais ações gerais serão feitas internamente? Nessa etapa traduzimos e agrupamos os requisitos em ações.

### Definição de regras por ação

Nessa etapa pegamos as ações feitas e definimos as regras que ela deve seguir.

1. **Usuários da ação:** Define-se quem poderá usufruir da ação. Nessa etapa, pense para quem a ação será exposta.
2. **Regras gerais da ação:** Define-se o que os usuários da ação terão que seguir. Nessa etapa, pense em todas as regras que a ação exposta deve ter para garantir o functionamento, quais validações deverão ser feitas e como serão feitas.
3. **Separação das regras imutáveis:** Agrupamos as regras que não devem mutar nessa ação. Todos devem seguir as regras aqui feitas.
4. **Separação das regras específicas:** Agrupamos as regras que dependem do contexto. Apenas alguns devem seguir essas regras, dependendo de seu contexto

### Definição de responsabilidades

1. **Definição dos agentes:** Dados os envolvidos, regras e ação, define-se quais partes do sistema tem envolvimento com essa ação específica. Aqui, pense em quem será chamado e qual domínio tem que ser respeitado para essa ação acontecer.
2. **Agrupamento das tarefas dos agents:** As regras e ações são separadas por agente responsável. Aqui, é decidido a quem cada pertence cada item especificado.

### Finalização

1. **Revisão:** Revisar o que foi feito, buscar melhorias e criticar as ideias
2. **Planejar a ordem**: Com tudo pronto, é decidida a ordem com que as ações serão feitas
