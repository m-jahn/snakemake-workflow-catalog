## Adding workflows

Workflows are **automatically added** to the Workflow Catalog. This is done by regularly searching Github repositories for matching workflow structures. The catalog includes workflows based on the following criteria.

### Generic workflows

- The workflow is contained in a public Github repository.
- The repository has a `README.md` file, containing the words "snakemake" and "workflow" (case insensitive).
- The repository contains a workflow definition named either `Snakefile` or `workflow/Snakefile`.
- If the repository contains a folder `rules` or `workflow/rules`, that folder must at least contain one file ending on `.smk`.
- The repository is small enough to be cloned into a [Github Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions) job (very large files should be handled via [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files), so that they can be stripped out during cloning).
- The repository is not blacklisted here.

### _Standardized Usage_ workflows

In order to additionally appear in the "standardized usage" area, repositories additionally have to:

- have their main workflow definition named `workflow/Snakefile` (unlike for [plain inclusion](#generic-workflows), which also allows just `Snakefile` in the root of the repository),
- provide configuration instructions under `config/README.md`
- contain a `YAML` file `.snakemake-workflow-catalog.yml` in their root directory, which configures the usage instructions displayed by this workflow catalog.

Typical content of the `.snakemake-workflow-catalog.yml` file:

```yaml
usage:
  mandatory-flags:
    desc: # describe your flags here in a few sentences
    flags: # put your flags here
  software-stack-deployment:
    conda: true # whether pipeline works with '--sdm conda'
    apptainer: true # whether pipeline works with '--sdm apptainer/singularity'
    apptainer+conda: true # whether pipeline works with '--sdm conda apptainer/singularity'
    report: true # whether creation of reports using 'snakemake --report report.zip' is supported
```

:::{note}
Definition of mandatory flags can happen through a list of strings (`['--a', '--b']`), or a single string (`'--a --b'`).
:::

:::{note}
The content of the `.snakemake-workflow-catalog.yml` file is subject to change. Flags might change in the near future, but current versions will always stay compatible with the catalog.
:::

Once included in the standardized usage area you can link directly to the workflow page using the URL `https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/<owner>/<repo>`. Do not forget to replace the `<owner>` and `<repo>` tags at the end of the URL.

### Workflow pages

Each standardized workflow has its own page, which is linked on the summary tables or the 'top workflows' tiles.
Workflow pages are **enhanced by information automatically parsed** from their Github repositories. Right now this includes:

1. **Tube Maps**: A graphical representation of the workflow rulegraph, build using [snakevision](https://github.com/OpenOmics/snakevision).
   Tube maps will automatically show up on your workflow page if the following command can be run for your workflow: `snakemake -s <snakefile> -c 1 -d .test --forceall --rulegraph`.
   This means, you need to have a working test case defined in the `.test` sub-dir.

2. **Workflow Configuration**: These are simply the configuration instructions from `config/README.md`.

3. **Workflow Parameters**: If the repo contains a `workflow/schemas/config.schema.yaml` OR `config/schemas/config.schema.yaml` file, the parameters defined in this file will be parsed and displayed as a table on the workflow page.
   The default fields that are recognized in the schema are `type`, `description`, `default` and `required`.
   Config options can be arbitrarily nested in the schema using the `properties` field of an object.

All these features are implemented in the [snakemake-workflow-template](https://github.com/snakemake-workflows/snakemake-workflow-template). If you want to create a standard-compliant workflow (page), the template is the ideal starting point.

### Release handling

If your workflow provides Github releases, the catalog will always just scrape the latest non-preview release. Hence, in order to update your workflow's records here, you need to release a new version on Github.
