# PROTEUS — Persistent Research Organism (prototype 0.1)

**Português:** protótipo local, executável e mensurável de agente persistente de aprendizado incremental. **Não** é AGI, não realiza autoaperfeiçoamento geral nem possui acesso irrestrito ao computador.

## Requisitos
Python 3.11+ (biblioteca padrão; `pytest` é opcional para testes). Não requer GPU, credenciais, serviços externos ou modelos baixados.

## Instalação
No diretório raiz do projeto:

```bash
python -m pip install -e .
python -m proteus init
python -m proteus train --episodes 300
python -m proteus evaluate --episodes 50
python -m proteus status
python -m proteus explore --cycles 3 --episodes 60
python -m proteus research --seeds 3 --episodes 100
python -m proteus evolve --episodes 80
python -m proteus run --cycles 2 --episodes-per-cycle 50
python -m proteus serve --port 8765
```

Use `python -m proteus run --cycles 0` para repetição contínua de ciclos até `Ctrl+C` ou `python -m proteus stop` em outro terminal. Depois execute `python -m proteus resume` para apagar o sinal de parada.

Os dados ficam em `data/` por padrão. Execute `python -m proteus --home /caminho/isolado train --episodes 200` para escolher outro diretório. A opção global `--home` deve vir **antes** do subcomando.

## Testes

```bash
python -m pytest -q
python -m compileall -q src
```

## Funcionamento real
O ciclo de aprendizado usa Q-learning tabular + experience replay opcional + modelo empírico de transições. Treina no GridWorld em tempo de execução e persiste em SQLite e JSON verificado por SHA-256. Métricas de avaliação não atualizam o modelo. Há também experiências pareadas para comparar com e sem replay.

A pasta `cognition/` inclui modelos tabulares e auxiliares simples; não inclui um Transformer nem um modelo de linguagem. `tools/` fornece manipulação restrita de arquivos, validador estático de Python e calculadora aritmética. O executor de shell e a rede são propositalmente bloqueados. Os módulos de evolução operam sobre candidatos de **hiperparâmetros** e não alteram livremente o código-fonte.

O "sandbox" de arquivos limita caminhos e quota, mas **não é isolamento de sistema operacional**. Para executar código gerado de verdade, seria necessário adicionar um contêiner/VM com isolamento de processos, usuários, rede e volumes, além de aprovação explícita.

## Estrutura
`src/proteus/core` (orquestração), `memory` (SQLite), `learning` (Q-learning/replay), `cognition` (modelos preditivos), `environments` (ambientes de teste), `research` (ablação e estatísticas), `evolution` (busca limitada), `evaluation` (métricas), `safety`, `infrastructure`, `tools`, `interface`. Consulte `docs/architecture.md` e `docs/learning_protocol.md`.

## Limitações conhecidas
- Não existe aprendizado neural profundo online no protótipo; é um baseline tabular.
- O GridWorld pode ser parcialmente observável quando existem obstáculos; a observação não inclui o mapa completo.
- A continuidade preserva tabela Q, modelo de transições, episódios, eventos e experiências, mas **não** restaura o estado exato do RNG/replay entre reinícios.
- Os módulos físicos, multiagentes, puzzles e programação são experimentos auxiliares simples, ainda não integrados ao ciclo principal.
- Na avaliação, novos mapas obstaculizados podem reduzir a taxa de sucesso. Isso é uma limitação mensurável, não algo escondido.
- O desenho de módulos prevê crescimento gradual sem garantir inteligência geral, descoberta científica nem melhorias indefinidas.

Licença: código demonstrativo para estudo e experimentação; revise políticas e direitos aplicáveis antes de distribuir ou executar em ambientes sensíveis.
