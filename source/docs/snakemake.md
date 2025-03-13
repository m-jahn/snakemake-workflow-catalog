
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

To do: Add a short description of how to create workflows.
Link to the template.
