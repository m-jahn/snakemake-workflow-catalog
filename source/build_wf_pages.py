import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from pathlib import Path


def check_readme(readme):
    clean_readme = []
    readme_split = readme.split("\n")
    code_block = False
    for i, j in zip(readme_split, range(0, len(readme_split))):
        if i.startswith("```"):
            code_block = not code_block
        if i.startswith("# ") and not code_block:
            clean_readme += [i.replace("# ", "## ")]
        else:
            clean_readme += [i]
    return "\n".join(clean_readme)


def check_deployment(depl):
    result = {}
    for i in depl.keys():
        if depl[i]:
            result[i.replace("singularity", "apptainer")] = True
    return result


def check_qc_output(qc_item):
    if qc_item is None:
        return None
    else:
        result = qc_item.split("\n")
        if len(result) > 20:
            return "\n".join(result[:20]) + "\n\n... (truncated)"
        else:
            return "\n".join(result)


def build_wf_pages():
    # import jinja templates
    env = Environment(
        loader=FileSystemLoader("_templates"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("workflow_page.md")

    # import workflow data
    with open("../data.js", "r") as f:
        next(f)
        repos = {}
        for repo in json.loads(f.read()):
            if repo["standardized"]:
                repos[repo["full_name"]] = repo

    # render markdown template with jinja2 for each repo
    for current_repo in repos:
        repo = repos[current_repo]
        wf_data = {}
        wf_data["full_name"] = current_repo
        md_filename = f"{current_repo.replace('/', ' ')}.md"
        # prepare title, description, reporting, qc stats, etc.
        wf_data["description"] = repo["description"]
        wf_data["topics"] = repo["topics"]
        wf_data["linting"] = check_qc_output(repo["linting"])
        wf_data["formatting"] = check_qc_output(repo["formatting"])
        wf_data["release"] = repo["latest_release"]
        last_update = datetime.fromtimestamp(repo["updated_at"])
        wf_data["last_update"] = datetime.strftime(last_update, "%Y-%m-%d")
        # add deployment options
        wf_data["deployment"] = check_deployment(repo["software_stack_deployment"])
        # add configuration from readme; adjust header level if necessary
        wf_data["config_from_readme"] = check_readme(repo["config_readme"])
        # render and export
        md_rendered = template.render(wf=wf_data)
        output_dir = Path("docs/workflows")
        output_path = output_dir / md_filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_rendered)

    # closing statement
    print("Workflow pages rendered successfully.")
    return None
