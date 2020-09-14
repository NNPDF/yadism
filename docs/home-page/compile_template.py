import sys
import pathlib

from jinja2 import Environment, FileSystemLoader

# ==========
# globals
# ==========


here = pathlib.Path(__file__).parent.absolute()
env = Environment(loader=FileSystemLoader(str(here)))

majors = []
majors.append(dict(num=0, minors=[1, 2, 3]))
majors.append(dict(num=1, minors=[0, 1]))


# ==========
# dump
# ==========

data = dict(majors=majors)
template = env.get_template(sys.argv[1])
stream = template.stream(data)
stream.dump(str(here / sys.argv[2]))
