PY=python3

PACKAGE=machinery
OUTPUT=_runcards
IGNORE=Makefile ${PACKAGE} README.md ${OUTPUT} banana.yaml benchmark.db
FOLDERS=$(filter-out ${IGNORE},$(wildcard *))

all:
	@for exp in ${FOLDERS}; do \
		echo $$exp; \
		${PY} -m ${PACKAGE} generate $$exp/*; \
		done

benchmark:
	@rm -f benchmark.db
	@${PY} -m ${PACKAGE} benchmark ${OUTPUT}/* -lo

clean:
	rm -rf ${OUTPUT}
