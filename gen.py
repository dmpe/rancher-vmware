import os
import pandas as pd

from jinja2 import Environment, PackageLoader, select_autoescape

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, "templates")
outpit_dir = os.path.join(root, "output")
filename_homepage = os.path.join(outpit_dir, "index.html")
filename_events = os.path.join(outpit_dir, "events.html")

env = Environment(loader=PackageLoader("homepage"))
template_homepage = env.get_template("index.html")
template_events = env.get_template("events.html")

print(template_homepage)
print(template_events)

data = pd.read_csv(
    outpit_dir + "/" + "all_hostnames.csv",
    sep=";",
    header=0,
    parse_dates=[1],
    infer_datetime_format=True,
)

csv_file=data.to_dict(orient="records")

with open(filename_homepage, "w") as fl, open(filename_events, "w") as fe:
    fl.write(template_homepage.render(hostList=csv_file))
    fe.write(template_events.render(eventsList=csv_file))
    fe.close()
    fl.close()
