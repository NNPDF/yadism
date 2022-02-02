MODULE=machinery
OUTPUT=_runcards
IGNORE=Makefile ${MODULE} README.md ${OUTPUT}
FOLDERS=$(filter-out ${IGNORE},$(wildcard *))

all:
	@for exp in ${FOLDERS}; do \
		echo $$exp; \
		python3 -m ${MODULE} $$exp/*; \
		done

clean:
	rm -rf ${OUTPUT}
