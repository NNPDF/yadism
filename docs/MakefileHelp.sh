#!/bin/bash
#
# Author: Diogo Alexsander Cavilha <diogocavilha@gmail.com>
# Date:   02.21.2018
#
# MAKEFILE HELP
#
# Shows a Makefile help.

_makefile_help_generator() {
    local pattern

    pattern='(?<=@# ).*'

    echo ""
    cat Makefile | grep -oP "$pattern" | awk -F' - ' '{print sprintf(" %-18s - %s", $1, $2);}'
    echo ""
}

_makefile_help_generator