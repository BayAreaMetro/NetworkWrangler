
These are the Tableau template files used to generate project diffs when the `--create_project_diffs` or 
`--create_project_diff` arguments are invoked via  [build_network_mtc.py](../scripts/build_network_mtc.py) 
or [build_network_mtc_blueprint.py](../scripts/build_network_mtc_blueprint.py).

In order to update them, I recommend the following process:

1) Build a network with project diffs for a project relevant to your updates.
2) Using the Tableau GUI, edit the generated project mapping tableau so that it's improved for that project.
3) Copy the generated version back over this template.
4) Use a text editor to remove the hardcoded directories that were set when you used the GUI by making them relative (e.g. [`directory='.'`](https://github.com/BayAreaMetro/NetworkWrangler/blob/8e5111ea27af9f63044d8339bdcd0bad2270dfdc/ProjectMapping/ProjectMapping_hwy.twb#L39C43-L39C56)).
5) Test your changes worked by building the network again with project diffs (maybe for a different project to make sure relative paths work).
6) If it works, yay! Commit it!
