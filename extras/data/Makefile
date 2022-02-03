PY=python3

PACKAGE=machinery
OUTPUT=_runcards
IGNORE=Makefile ${PACKAGE} README.md ${OUTPUT}
FOLDERS=$(filter-out ${IGNORE},$(wildcard *))

all:
	@for exp in ${FOLDERS}; do \
		echo $$exp; \
		${PY} -m ${PACKAGE} generate $$exp/*; \
		done

benchmark:
	@${PY} -m ${PACKAGE} benchmark ${OUTPUT}/*

clean:
	rm -rf ${OUTPUT}
