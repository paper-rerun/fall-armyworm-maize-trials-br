# Fall armyworm control trials in Brazilian maize

2,075 trial results on the control of fall armyworm (*Spodoptera frugiperda*, "lagarta-do-cartucho") in maize, taken from the tables of 20 open-access Embrapa publications (2000 to 2023). Each row is one number exactly as printed: a treatment, its dose, where and when it was tested, what was measured and the value, with the page and table it came from.

Fall armyworm is the main pest of maize in Brazil, and much of the country's field and lab evidence on how to control it is published in Portuguese technical bulletins that are hard to find and are not machine-readable. This dataset makes 20 of them searchable and reusable.

Part of [Paper Rerun](https://paper-rerun.github.io). The work was done by AI agents on a home computer and reviewed by a human before publication.

## What is in it

| | |
|---|---|
| Publications | 20 (Alice and Infoteca-e, Embrapa's open repositories) |
| Records | 2,075 |
| Treatments | chemical 760, untreated or reference controls 622, biological 405 (baculovirus, *Bacillus thuringiensis*, *Beauveria*, *Telenomus*, *Trichogramma*, predators), Bt maize 156, botanical (neem) and other 122, cultural 10 |
| Measures | larval mortality, larvae per plant, leaf damage score, yield, parasitism, infested plants, development time, weight and others |

Files:
- `data/fall_armyworm_maize_trials.csv`: the dataset, one record per printed value. Columns are described in `method/schema.json`.
- `data/sources.csv`: the 20 publications, with authors, reference, record link and licence notice.
- `qa/diff.csv` and `qa/adjudication.csv`: every disagreement between the two independent transcriptions and how it was settled against the PDF.
- `method/`: the schema, the comparison script and the merge script.

The `origin` column says where each record came from: `A` (first transcription, confirmed by the second), `B` (found only by the second transcription, confirmed against the PDF) or `corrected` (first transcription with a field fixed after adjudication).

## How it was made

1. **Collection.** An agent searched Embrapa's open repositories for publications with quantitative trial tables on this topic and downloaded 20 of them.
2. **First transcription.** One agent per publication transcribed every table cell on the topic into a fixed schema, copying numbers exactly as printed (decimal comma to point, nothing computed or inferred).
3. **Second, blind transcription.** A different agent per publication transcribed the same documents from the PDF alone, without access to the first transcription, and accounted for every data cell of every table.
4. **Comparison and adjudication.** A script paired the two transcriptions and listed every disagreement and every value present in only one of them. Each one was settled by checking the PDF, with the page as evidence.

This is the double-entry-plus-arbitration practice used in data curation. We started with a single transcription and a checker who could see it; that checker reported no errors, which turned out to be misleading, so we added the blind step.

## How accurate it is

- **Numbers:** the two independent transcriptions agreed on every one of the 1,953 values and significance letters they both read. No value or letter error was found.
- **Coverage:** the first transcription alone missed 120 records, including a whole table printed sideways, and left the dose empty in 88 records where it was stated on another page. On its own it was 90% complete and correct per record; the blind transcription alone, 97.9%. Every one of those gaps is closed in this dataset.
- **Known limits:** values shown only in charts without printed numbers were not read. Coefficients of variation and other ANOVA statistics were left out. `variable_standardized` is still `other` for most records: the vocabulary will be widened in the next version (parasitism, infested plants, weight, development time, survival).

## Licence and citation

- The dataset (the CSV files, schema and scripts) is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the original publications listed in `data/sources.csv` as well as this dataset.
- The numbers are facts taken from the publications, with full citation on every row. The publications themselves are not redistributed. Embrapa's repositories show a CC BY-NC-ND 4.0 notice; one publication (figueiredo2015) carries a publisher copyright notice, so only its numbers and short citations are used.
- Notes quote the source text only in short fragments, with the page.

Errors or missing trials: please [open an issue](https://github.com/paper-rerun/fall-armyworm-maize-trials-br/issues).

## How this dataset was made

This dataset was built by AI agents (Claude, by Anthropic) on a home computer and reviewed by a human before publication. No value was estimated or typed by hand: each one was transcribed from the source PDF twice, independently, and every disagreement was checked against the page. The method and scripts are in `method/`, so the same can be done for other crops, pests and literatures. How the wider project works: https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contact: Filipe Tessaro, via issues on this repository.
