#!/usr/bin/env bash


VP_ENV_DIR='.virtualenv'
VP_REQ_FILE='requirements.txt'
VP_SUBSHELL=0
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

# Enter virtual environment.
enter () {
    # In virtual environment already?
    # VIRTUAL_ENV created when 'activate' is sourced.
    if [ -z "${VIRTUAL_ENV}" ]; then
        # shellcheck disable=SC1090
        echo "${VP_ENV_DIR}/bin/activate"
        source "${VP_ENV_DIR}/bin/activate"
        # shellcheck disable=SC2046
        PS1="[(${VP_ENV_DIR}) \\u@\\h $(basename $(pwd))]> "
        VP_SUBSHELL=1
    fi

    return 0
}

# Create virtual environment.
create () {
    # Check if virtualenv is installed.
    if ! command -v virtualenv >/dev/null 2>&1; then
        echo "Installing virtualenv package.."
        pip install virtualenv
    fi

    if [ -d "${VP_ENV_DIR}" ] || [ -L "${VP_ENV_DIR}" ]; then
        echo "${VP_ENV_DIR} exists."
        return 0
    fi

    args=("${VP_ENV_DIR}")

    echo "Creating .virtualenv ..."
    virtualenv "${args[@]}"
    
    enter
    
    echo "Installing requrements .. "
    pip install -r $VP_REQ_FILE
    
    echo "Deactivating .. "
    sleep 1
    exit
    # exit
    return 0
}

# Delete virtual environment.
delete () {
    if [ -n "${VIRTUAL_ENV}" ]; then
        echo "Please exit out of virtual environment subshell with 'exit' before deleting it."
        return 1
    fi

    if [ -d "${VP_ENV_DIR}" ] && [ ! -L "${VP_ENV_DIR}" ]; then
        rm -rf "${VP_ENV_DIR}"
        echo "Deleted virtual environment folder: ${VP_ENV_DIR}"
    else
        echo "No ${VP_ENV_DIR} to delete."
    fi

    return 0
}

# Handle command line.
CMD=${1:-h}

case "${CMD}" in
    -\?|-h|--help|\?|h|help )
        echo "wrong usage "
        # echo "Usage:"
        # echo -e "\\tvp <command>"
        # echo "Commands:"
        # echo -e "\\t-?, -h, --help"
        # echo -e "\\t?, h, help\\t\\tDisplay this help message."
        # echo -e "\\tcreate [args]\\t\\tCreate virtual environment."
        # echo -e "\\tdelete\\t\\t\\tDelete virtual environment."
        # echo -e "\\tenter\\t\\t\\tEnter virtual environment to start working."
        # echo -e "\\tinstall [pkg]\\t\\tInstall package and update requirements.txt file."
        # echo -e "\\tuninstall [pkg]\\t\\tUninstall package and update requirements.txt file."
        # echo
        # echo "Notes:"
        # echo "To exit out of virtual environment subshell type: exit"
        # echo "Any arguments for the create command are passed to virtualenv."
        # echo "Any commands not on the list (other than create) are passed to pip."
    ;;
    create|delete|enter )
        shift

        ${CMD} "${@}"

        if [ "${VP_SUBSHELL}" -eq 1 ]; then
            bash
        fi
    ;;
    * )
        # pip "${@}"
    # ;;
esac
