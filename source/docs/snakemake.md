
# Snakemake

```{toctree}
:hidden:
```

## What is 'snakemake'?

The Snakemake workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language. They can be seamlessly scaled to server, cluster, grid and cloud environments, without the need to modify the workflow definition. Finally, Snakemake workflows can entail a description of required software, which will be automatically deployed to any execution environment.

## Basic usage

Snakemake usage is [extensively documented here](https://snakemake.readthedocs.io/en/stable/).

Snakemake is organized in `rules`, which define specific input and output files. 
Files are processed using code which is for example directly deployed with the `shell` directive, or with external `python` and `R` scripts, or even directly rendered `markdown` based notebooks.

To get a first impression:

```bash
rule select_by_country:
    input:
        "data/worldcitiespop.csv"
    output:
        "by-country/{country}.csv"
    shell:
        "xsv search -s Country '{wildcards.country}' "
        "{input} > {output}"
```

In this code chunk, the input table `data/worldcitiespop.csv` is searched by the keyword `country`, which is used as a wildcard to construct new file names for the output. The result is that all lines from the original table are split by Country and saved as separare files in a new output directory.

## Create your own workflows

The best starting point to create your own workflows is the [Snakemake workflow template](https://github.com/snakemake-workflows/snakemake-workflow-template).

The template comes with a pre-configured structure that is compatible with the Snakemake catalog ['standardized usage'](<about/adding_workflows>). Just fork or clone the template, start addiong rules and push your workflow to Github. The structure of 'standardized' workflows is like this:

```
├── config/
│   └── config.yaml
│   └── README.md
├── workflow/
│   ├── Snakefile
│   ├── rules/
│   ├── scripts/
│   └── envs/
├── .snakemake-workflow-catalog.yml
└── README.md
```

:::{note}
The template is currently not fully functional as it contains no actual `Snakefile` and test cases. This will be changed in the near future.
:::

