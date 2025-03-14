# All other workflows

<!-- NOTE: the raw strings for commas are required to ensure correct line breaks-->

```{csv-table} All other workflows deviating from 'standardized usage'
:header: Workflow,Description,Topics,Reporting,Stars,Watchers
:class: sphinx-datatable
:width: 135%
:widths: auto

{% for repo in input -%}
    [{{ repo["full_name"] }}](<https://github.com/{{ repo["full_name"] }}>){% raw %},{% endraw %}
    "{{ repo["description"] }}"{% raw %},{% endraw %}
    {%- for t in repo["topics"] -%}{bdg-secondary}`{{ t }}` {% endfor %}{% raw %},{% endraw %}
    {bdg-muted}`last update {{ repo["last_update"] }}`
    {%- for qc in ["formatting", "linting"] -%}
        {%- if repo[qc] == None -%}
            {bdg-success}`{{qc}}: passed`
        {%- else -%}
            {bdg-danger}`{{qc}}: failed`
        {%- endif -%}
    {% endfor %}{% raw %},{% endraw %}
    {{ repo["stargazers_count"] }}{% raw %},{% endraw %}
    {{ repo["subscribers_count"] }}
{% endfor %}
```
