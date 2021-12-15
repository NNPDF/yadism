IGNORE=Makefile parse README.md _runcards
FOLDERS=$(filter-out ${IGNORE},$(wildcard *))

all:
	for exp in ${FOLDERS}; do \
		echo $$exp; \
		python3 -m parse $$exp/*; \
	done
