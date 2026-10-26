# Ensaios de controle da lagarta-do-cartucho no milho no Brasil

English version: [README.md](README.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23630093.svg)](https://doi.org/10.5281/zenodo.23630093)

2.075 resultados de ensaios sobre o controle da lagarta-do-cartucho (*Spodoptera frugiperda*) no milho, tirados das tabelas de 20 publicações de acesso aberto da Embrapa (2000 a 2023). Cada linha é um número exatamente como foi impresso: um tratamento, a dose, onde e quando foi testado, o que foi medido e o valor, com a página e a tabela de onde saiu.

A lagarta-do-cartucho é a principal praga do milho no Brasil, e boa parte dos dados de campo e de laboratório do país sobre como controlá-la está em boletins técnicos em português, difíceis de achar e que não podem ser lidos por máquina. Este dataset torna 20 deles pesquisáveis e reutilizáveis.

Faz parte do [Paper Rerun](https://paper-rerun.github.io). O trabalho foi feito por agentes de IA num computador doméstico e revisado por uma pessoa antes da publicação.

## O que tem

| | |
|---|---|
| Publicações | 20 (Alice e Infoteca-e, os repositórios abertos da Embrapa) |
| Registros | 2.075 |
| Tratamentos | químicos 760, testemunhas sem tratamento ou de referência 622, biológicos 405 (baculovírus, *Bacillus thuringiensis*, *Beauveria*, *Telenomus*, *Trichogramma*, predadores), milho Bt 156, botânicos (nim) e outros 122, culturais 10 |
| Medidas | mortalidade de lagartas, lagartas por planta, nota de dano foliar, produtividade, parasitismo, plantas infestadas, tempo de desenvolvimento, peso e outras |

Arquivos:
- `data/fall_armyworm_maize_trials.csv`: o dataset, um registro por valor impresso. As colunas estão descritas em `method/schema.json`.
- `data/sources.csv`: as 20 publicações, com autores, referência, link do registro e aviso de licença.
- `qa/diff.csv` e `qa/adjudication.csv`: cada divergência entre as duas transcrições independentes e como ela foi resolvida conferindo o PDF.
- `method/`: o schema, o script de comparação e o script de junção.

A coluna `origin` diz de onde veio cada registro: `A` (primeira transcrição, confirmada pela segunda), `B` (encontrado só pela segunda transcrição, confirmado no PDF) ou `corrected` (primeira transcrição com um campo corrigido depois da arbitragem).

### Principais colunas

O arquivo está em UTF-8, com vírgula separando as colunas. Local, safra, estádio da cultura e método de aplicação estão em `location`, `season_or_year`, `crop_stage` e `application_method`, no próprio registro.

- `doc_id`: identificador da publicação de origem. Liga o registro a `data/sources.csv` e é também o nome do PDF, sem a extensão.
- `page`: página do PDF contada a partir de 1 (a primeira página do arquivo é 1), e não o número impresso na página. O rótulo da tabela está em `table_or_figure`, como impresso ("Tabela 3", "TABLE 2"), ou `text` quando o número está no corpo do texto.
- `treatment`: nome do tratamento exatamente como aparece na linha ou no cabeçalho da tabela, no idioma do documento.
- `treatment_type`: classe do tratamento. `chemical` é inseticida sintético; `biological`, organismo vivo ou produto microbiano (Bt pulverizado, baculovírus, fungos, parasitoides, predadores); `Bt`, híbrido ou evento de milho Bt; `cultural`, prática de cultivo (época de semeadura, dessecação, consórcio, push-pull, adubação com silício); `control`, testemunha sem tratamento ou isolinha não Bt usada como testemunha; `other`, nim e outros extratos vegetais, só feromônio ou combinações que não cabem numa classe.
- `dose_and_unit`: dose com a unidade, como escrita ("0,2 L/ha", "15 parasitoides/m2"). Vazia quando não se aplica (híbrido Bt, testemunha) ou quando o documento não informa.
- `variable`: variável medida, exatamente como no cabeçalho ou na legenda, com o momento da avaliação quando ele faz parte do cabeçalho ("Mortalidade (%) 72 h", "Nota de dano 14 DAA").
- `variable_standardized`: a mesma variável numa lista fechada. `efficacy_pct` é a eficiência de controle impressa pelos autores (Abbott, Henderson-Tilton ou similar); `mortality_pct`, mortalidade observada ou corrigida; `damage_score`, nota de dano foliar (Davis 0-9, 0-5); `larvae_per_plant`, lagartas por planta ou por unidade amostral; `yield_kg_ha`, produtividade de grãos em kg/ha; `other`, todo o resto.
- `value_as_printed`: o número exatamente como impresso, sem a letra de significância ("87,5").
- `value`: o mesmo número com ponto decimal (87.5), pronto para cálculo. Em relação a `value_as_printed`, só muda a vírgula pelo ponto e sai o separador de milhar. Nada foi calculado, convertido ou arredondado.
- `unit`: unidade como impressa ou informada na legenda ("%", "kg/ha", "lagartas/planta", "nota (0-5)").
- `statistic`: o que o número é: `mean` (média, o padrão quando o documento não diz outra coisa), `median`, `total`, `single_value` (uma observação), `percentage_of_total` ou `other`.
- `significance_letter`: letra(s) do teste de médias exatamente como impressas ("a", "bc", "Ab1"). Vazia quando não há.

## Como foi feito

1. **Coleta.** Um agente buscou nos repositórios abertos da Embrapa publicações com tabelas de ensaios quantitativos sobre o tema e baixou 20 delas.
2. **Primeira transcrição.** Um agente por publicação transcreveu cada célula de tabela sobre o tema num schema fixo, copiando os números exatamente como impressos (vírgula decimal trocada por ponto, nada calculado ou deduzido).
3. **Segunda transcrição, às cegas.** Outro agente por publicação transcreveu os mesmos documentos só a partir do PDF, sem acesso à primeira transcrição, e prestou contas de cada célula de dados de cada tabela.
4. **Comparação e arbitragem.** Um script pareou as duas transcrições e listou cada divergência e cada valor presente em só uma delas. Cada caso foi resolvido conferindo o PDF, com a página como evidência.

É a prática de dupla digitação com arbitragem usada em curadoria de dados. Começamos com uma transcrição só e um revisor que podia vê-la. Esse revisor não apontou nenhum erro, o que se mostrou enganoso, e por isso acrescentamos a etapa às cegas.

## Qual a precisão

- **Números:** as duas transcrições independentes concordaram em todos os 1.953 valores e letras de significância que ambas leram. Não foi encontrado nenhum erro de valor ou de letra.
- **Cobertura:** sozinha, a primeira transcrição deixou de fora 120 registros, inclusive uma tabela inteira impressa de lado na página, e deixou a dose vazia em 88 registros em que ela aparecia em outra página. Por registro, ela estava 90% completa e correta; a transcrição às cegas, sozinha, 97,9%. Todas essas lacunas estão fechadas neste dataset.
- **Limites conhecidos:** valores mostrados só em gráficos, sem número impresso, não foram lidos. Coeficientes de variação e outras estatísticas da ANOVA ficaram de fora. `variable_standardized` ainda é `other` na maioria dos registros: o vocabulário vai ser ampliado na próxima versão (parasitismo, plantas infestadas, peso, tempo de desenvolvimento, sobrevivência).

## Licença e citação

- O dataset (os arquivos CSV, o schema e os scripts) é publicado sob a licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Por favor, cite as publicações originais listadas em `data/sources.csv` e também este dataset.
- Os números são fatos tirados das publicações, com a citação completa em cada linha. As publicações em si não são redistribuídas. Os repositórios da Embrapa exibem um aviso CC BY-NC-ND 4.0; uma publicação (figueiredo2015) traz um aviso de copyright da editora, então dela só são usados os números e citações curtas.
- As notas citam o texto original só em trechos curtos, com a página.

Erros ou ensaios que faltam: por favor, [abra uma issue](https://github.com/paper-rerun/fall-armyworm-maize-trials-br/issues).

## Como este dataset foi feito

Este dataset foi montado por agentes de IA (Claude, da Anthropic) num computador doméstico e revisado por uma pessoa antes da publicação. Nenhum valor foi estimado ou digitado à mão: cada um foi transcrito do PDF original duas vezes, de forma independente, e cada divergência foi conferida na página. O método e os scripts estão em `method/`, então o mesmo pode ser feito para outras culturas, pragas e literaturas. Como funciona o projeto como um todo (em inglês): https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contato: Filipe Tessaro, pelas issues deste repositório.
