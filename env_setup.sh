#!/usr/bin/env bash

################################################################
# @ VERSION 0.0.1
# 
# This script is for project configuration.
#
# You should run this script everytime before working on the project.
#   source env_setup.sh
# 
# SUPPORTED TERMINALS:
#   * git bash (Windows)
#   * WSL2-Ubuntu (Windows)
#   * terminal (MacOS / Linux)
################################################################

CS348_PROJECT="CS 348 Project"
CS348_PROJECT_SCRIPT_VERSION="0.0.1"
CS348_PROJECT_PYTHON_EXEC=python3
CS348_PROJECT_API_PORT=6608
CS348_PROJECT_ADMINER_PORT=8080
_CS348_PROJECT_INITIAL_DIR=$(pwd)

# validate configurable os
if [[ "${OSTYPE}" == "linux-gnu"* ]]; then
    _CS348_PROJECT_OS="${OSTYPE}"
    _CS348_PROJECT_VERIFIED_OS="True"
elif [[ "${OSTYPE}" == "darwin"* ]]; then
    _CS348_PROJECT_OS="MacOS"
    _CS348_PROJECT_VERIFIED_OS="True"
elif [[ "${OSTYPE}" == "cygwin" ]]; then
    # POSIX compatibility layer and Linux environment emulation for Windows
    _CS348_PROJECT_OS="cygwin"
    _CS348_PROJECT_VERIFIED_OS="False"
elif [[ "${OSTYPE}" == "msys" ]]; then
    # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
    _CS348_PROJECT_OS="Windows"
    _CS348_PROJECT_VERIFIED_OS="True"
elif [[ "${OSTYPE}" == "win32" ]]; then
    _CS348_PROJECT_OS="${OSTYPE}"
    _CS348_PROJECT_VERIFIED_OS="False"
elif [[ "${OSTYPE}" == "freebsd"* ]]; then
    _CS348_PROJECT_OS="${OSTYPE}"
    _CS348_PROJECT_VERIFIED_OS="False"
else
    _CS348_PROJECT_OS="${OSTYPE}"
    _CS348_PROJECT_VERIFIED_OS="False"
fi

# continue with script configuration data
if [[ ${_CS348_PROJECT_OS} == MacOS ]]; then
    CS348_PROJECT_ROOT=${0:a:h}
else
    CS348_PROJECT_ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
fi
# IF Project root path contains 'space', it will cause error
if [[ "${CS348_PROJECT_ROOT}" =~ ( ) ]]; then
    echo -e "\e[33m[WARNING] Project root path contains 'space' which is not allowed: ${CS348_PROJECT_ROOT}.\e[0m"
    echo -e "Please move the project to different location and try again - run 'pwd' command to check if current directory contains 'space'"
    return 1 2> /dev/null; exit 1
fi

# Helper function
is_sourced() {
    if [ -n "$ZSH_VERSION" ]; then 
        case $ZSH_EVAL_CONTEXT in *:file:*) return 0;; esac
    else # Add additional POSIX-compatible shell names here, if needed.
        case ${0##*/} in dash|-dash|bash|-bash|ksh|-ksh|sh|-sh) return 0;; esac
    fi
    return 1  # NOT sourced.
}

(return 0 2>/dev/null) && sourced=1 || sourced=0
if [[ ${sourced} -eq 0 ]]; then
    echo -e "Script is not sourced, please run \"source env_setup.sh\" instead."
    echo -e "For more information, please check \"source env_setup.sh --help\" for more usages."
    return 1 2> /dev/null; exit 1
fi

usage() {
    echo -e "To start working on CS 348 Project, goto project's directory and run \"\e[3m\e[35msource env_setup.sh\e[0m\""
    echo -e ""
    echo -e "\e[1mUsage:\e[0m"
    echo -e "  \e[35msource env_setup.sh \e[3m\e[33m<option>\e[0m"
    echo -e ""
    echo -e "\e[1mOptions:\e[0m"
    echo -e "  \e[3m\e[33m-h\e[0m, \e[3m\e[33m--help\e[0m\t\tShow help."
    echo -e "  \e[3m\e[33m-i\e[0m, \e[3m\e[33m--instruction\e[0m\tShow instructions."
}

instruction () {
    echo -e "\e[36mCS 348 PROJECT DEVELOP ENVIRONMENT FEATURES\e[0m"
    echo -e "  \e[33mroot\e[0m\t\t\t\tMove to ${CS348_PROJECT_ROOT}."
    echo -e "  \e[33mapi-server\e[0m\t\t\tProvides useful commands for the developer. \e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
    echo -e ""
    echo -e "\e[36mGENERAL INSTRUCTIONS\e[0m"
    echo -e "  The project has 2 core docker containers: db (a.k.a. database), and app (a.k.a. flask-api-server)."
    echo -e "  The server can be easily run by \"api-server up\" command (Booting takes 30-60 seconds)."
    echo -e "  Once server is running, you can check the database using GUI using \"api-server open db\" or through CLI using \"api-server connect db\"."
    echo -e "  Ther server is called \e[33mdb\e[0m. The username for db is \e[33mgroup8\e[0m and the password is \e[33mPassword0!\e[0m, finally the database is \e[33mcs348_project\e[0m."
    echo -e "  In order to use \"flask seed all\" command, connect to api container through \"api-server connect api\" command, then cd into src, then type \"flask seed all\""
    echo -e "  finally, to close the server, enter \"api-server down\". For more detailed information, please check \"api-server --help\""
    echo -e ""
    echo -e "\e[36mREMARK\e[0m"
    echo -e "  * the data/ folder is mounted with db container - it contains mysql data, so if you want to reset the data, simply remove this folder and rebuild."
    echo -e "  * the api/ folder is mounted with app container - since flask is in debugging mode, if you edit the code and save, the change will be reflected immediately."
    echo -e "  * do not upload data/ folder to GitHub (it's your local database)."
    echo -e "  * if you need to use flask migration commands, use \"api-server connect api\" feature."
    echo -e ""
    echo -e "If you have any questions, please contact John Yoon <j53yoon@uwaterloo.ca>."
}

set_features () {
    alias root="cd '${CS348_PROJECT_ROOT}'; echo -e \"\e[35mMOVING TO ${CS348_PROJECT_ROOT}.\e[0m\""
    
    api-server () {
        __CS348_SERVER_INITITAL_DIR=$(pwd)
        cd ${CS348_PROJECT_ROOT}
        if [[ ${#} -eq 0 ]]; then
            echo -e "\e[31mINVALID ARGUMENT: at least 1 argument expected.\e[0m"
            echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
            cd ${__CS348_SERVER_INITITAL_DIR}
            return 1
        else
            if [[ ${1} == "-h" || ${1} == "--help" ]]; then
                echo -e "\e[1mPurpose:\e[0m"
                echo -e "  Allows developers to control docker features with easy commands."
                echo -e ""
                echo -e "\e[1mFeatures:\e[0m"
                echo -e " \e[3m\e[33m api-server [-h|--help]\e[0m\t\tShow this help."
                echo -e " \e[3m\e[33m api-server [up|start]\e[0m\t\tBuild a new image and start up the server on background (recommended)."
                echo -e " \e[3m\e[33m api-server [up|start] here\e[0m\t\tBuild a new image and start up the server on this terminal."
                echo -e " \e[3m\e[33m api-server [down|stop]\e[0m\t\tStop the running servers."
                echo -e " \e[3m\e[33m api-server [ls|show] [images|containers]\e[0m\t\tShow all the images or containers built."
                echo -e " \e[3m\e[33m api-server [rm|remove|delete] [images|containers|all]\e[0m\t\tdelete all the images and/or containers built."
                echo -e " \e[3m\e[33m api-server [ps|process|processess]\e[0m\t\tShow every running containers."
                echo -e " \e[3m\e[33m api-server connect [api|app|flask]\e[0m\t\tOpen bash terminal within the api container."
                echo -e " \e[3m\e[33m api-server connect [db|database|mysql]\e[0m\t\tOpen bash terminal within the db container."
                echo -e " \e[3m\e[33m api-server log [api|app|flask]\e[0m\t\tShow the terminal log of the api container."
                echo -e " \e[3m\e[33m api-server log [db|database|mysql]\e[0m\t\tShow the terminal log of the db container."
                echo -e " \e[3m\e[33m api-server open [api|app|flask]\e[0m\t\tOpen the browser directed to http://localhost:${CS348_PROJECT_API_PORT}/."
                echo -e " \e[3m\e[33m api-server open [db|database|mysql]\e[0m\t\tOpen the browser directed to http://localhost:${CS348_PROJECT_ADMINER_PORT}/."
                echo -e ""                
                echo -e "\e[35m\e[1m\e[3mYou will require python3 installed in your terminal to use \"api-server open <option>\".\e[0m"
                cd ${__CS348_SERVER_INITITAL_DIR}
                return 0
            elif [[ ${1} == "up" || ${1} == "start" ]]; then
                if [[ ${#} -eq 1 ]]; then
                    docker-compose up --build -d
                    cd ${__CS348_SERVER_INITITAL_DIR}
                    return 0
                else
                    if [[ ${2} == "here" ]]; then
                        docker-compose up --build
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    else
                        echo -e "\e[31mINVALID ARGUMENT: ${2}\e[0m"
                        echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 1
                    fi
                fi
            elif [[ ${1} == "ls" || ${1} == "show" ]]; then
                if [[ ${#} -eq 1 ]]; then
                    echo -e "\e[31mINVALID ARGUMENT: More argument is expected for ${1}\e[0m"
                    echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                    cd ${__CS348_SERVER_INITITAL_DIR}
                    return 1
                else
                    if [[ ${2} == "images" ]]; then
                        docker-compose images
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    elif [[ ${2} == "containers" ]]; then
                        docker container ls
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    else
                        echo -e "\e[31mINVALID ARGUMENT: ${2}\e[0m"
                        echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 1
                    fi
                fi
            elif [[ ${1} == "rm" || ${1} == "delete" || ${1} == "remove" ]]; then
                if [[ ${#} -eq 1 ]]; then
                    echo -e "\e[31mINVALID ARGUMENT: More argument is expected for ${1}\e[0m"
                    echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                    cd ${__CS348_SERVER_INITITAL_DIR}
                    return 1
                else
                    if [[ ${2} == "images" ]]; then
                        __CS348_RM_TEST=$(docker image ls -q)
                        if [[ ${__CS348_RM_TEST} == "" ]]; then
                            echo -e "\e[33mThere are no images.\e[0m"
                            cd ${__CS348_SERVER_INITITAL_DIR}
                            return 0
                        else
                            docker image rm -f $(docker image ls -q)
                            cd ${__CS348_SERVER_INITITAL_DIR}
                            return 0
                        fi
                    elif [[ ${2} == "containers" ]]; then
                        __CS348_RM_TEST=$(docker container ls -aq)
                        if [[ ${__CS348_RM_TEST} == "" ]]; then
                            echo -e "\e[33mThere are no containers.\e[0m"
                            cd ${__CS348_SERVER_INITITAL_DIR}
                            return 0
                        else
                            docker container rm -f $(docker container ls -aq)
                            cd ${__CS348_SERVER_INITITAL_DIR}
                            return 0
                        fi
                    elif [[ ${2} == "all" ]]; then
                        __CS348_RM_TEST=$(docker image ls -q)
                        if [[ ${__CS348_RM_TEST} == "" ]]; then
                            echo -e "\e[33mThere are no images.\e[0m"
                        else
                            docker image rm -f $(docker image ls -q)
                        fi

                        __CS348_RM_TEST=$(docker container ls -aq)
                        if [[ ${__CS348_RM_TEST} == "" ]]; then
                            echo -e "\e[33mThere are no containers.\e[0m"
                        else
                            docker container rm -f $(docker container ls -aq)
                        fi

                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    else
                        echo -e "\e[31mINVALID ARGUMENT: ${2}\e[0m"
                        echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 1
                    fi
                fi
            elif [[ ${1} == "ps" || ${1} == "process" || ${1} == "processess" ]]; then
                docker-compose ps
                cd ${__CS348_SERVER_INITITAL_DIR}
                return 0
            elif [[ ${1} == "down" || ${1} == "stop" ]]; then
                docker-compose down
                cd ${__CS348_SERVER_INITITAL_DIR}
                return 0
            elif [[ ${1} == "connect" ]]; then
                if [[ ${#} -eq 1 ]]; then
                    echo -e "\e[31mINVALID ARGUMENT: More argument is expected for ${1}\e[0m"
                    echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                    cd ${__CS348_SERVER_INITITAL_DIR}
                    return 1
                else
                    if [[ ${2} == "api" || ${2} == "app" || ${2} == "flask" ]]; then
                        docker-compose ps | grep "cs348-project-api-api-1" 1> /dev/null 2> /dev/null
                        if [[ ${?} -eq 0 ]]; then
                            docker exec -it cs348-project-api-api-1 bash
                        else
                            echo -e "\e[33mThe api container is currently not on service.\e[0m"
                        fi
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    elif [[ ${2} == "db" || ${2} == "database" || ${2} == "mysql" ]]; then
                        docker-compose ps | grep "cs348-project-api-db-1" 1> /dev/null 2> /dev/null
                        if [[ ${?} -eq 0 ]]; then
                            docker exec -it cs348-project-api-db-1 bash
                        else
                            echo -e "\e[33mThe db container is currently not on service.\e[0m"
                        fi
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    else
                        echo -e "\e[31mINVALID ARGUMENT: ${2}\e[0m"
                        echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 1
                    fi
                fi
            elif [[ ${1} == "open" ]]; then
                if [[ ${#} -eq 1 ]]; then
                    echo -e "\e[31mINVALID ARGUMENT: More argument is expected for ${1}\e[0m"
                    echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                    cd ${__CS348_SERVER_INITITAL_DIR}
                    return 1
                else
                    if [[ ${2} == "api" || ${2} == "app" || ${2} == "flask" ]]; then
                        ${CS348_PROJECT_PYTHON_EXEC} -m webbrowser http://localhost:${CS348_PROJECT_API_PORT}
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    elif [[ ${2} == "db" || ${2} == "database" || ${2} == "mysql" ]]; then
                        ${CS348_PROJECT_PYTHON_EXEC} -m webbrowser http://localhost:${CS348_PROJECT_ADMINER_PORT}
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    else
                        echo -e "\e[31mINVALID ARGUMENT: ${2}\e[0m"
                        echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 1
                    fi
                fi
            elif [[ ${1} == "log" || ${1} == "logs" ]]; then
                if [[ ${#} -eq 1 ]]; then
                    echo -e "\e[31mINVALID ARGUMENT: More argument is expected for ${1}\e[0m"
                    echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                    cd ${__CS348_SERVER_INITITAL_DIR}
                    return 1
                else
                    if [[ ${2} == "api" || ${2} == "app" || ${2} == "flask" ]]; then
                        docker logs cs348-project-api-api-1
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    elif [[ ${2} == "db" || ${2} == "database" || ${2} == "mysql" ]]; then
                        docker logs cs348-project-api-db-1
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 0
                    else
                        echo -e "\e[31mINVALID ARGUMENT: ${2}\e[0m"
                        echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                        cd ${__CS348_SERVER_INITITAL_DIR}
                        return 1
                    fi
                fi
            else
                echo -e "\e[31mINVALID ARGUMENT: ${1}\e[0m"
                echo -e "\e[33mPlease check \e[3m'api-server --help'\e[0m\e[33m for the usage."
                cd ${__CS348_SERVER_INITITAL_DIR}
                return 1
            fi
        fi
    }

    export -f api-server
}

# argument parsing
if [[ ${#} -eq 1 ]]; then
    if [[ ${1} == "-h" || ${1} == "--help" ]]; then
        usage
        return 0 2> /dev/null; exit 0
    elif [[ ${1} == "-i" || ${1} == "--instruction" ]]; then
        instruction
        return 0 2> /dev/null; exit 0
    fi
elif [[ ${#} -gt 1 ]]; then
    echo -e "\e[31mInvalid option value, please check \"source env_setup.sh --help\" for usage.\e[0m"
    return 1 2> /dev/null; exit 1
fi

# script description
echo -e "\e[36m${CS348_PROJECT} ENVIRONMENT SETUP ROUTINE\e[0m"

echo -e "\e[0m   VERSION: \t\e[32m${CS348_PROJECT_SCRIPT_VERSION}\e[0m"

echo -en "\e[0m   SOURCED: "
(return 0 2>/dev/null) && sourced=1 || sourced=0
if [[ ${sourced} -eq 0 ]]; then
    echo -e "\t\e[31mFalse\e[0m"
    echo -e "\e[31m[WARNING] Script is not sourced, please run \e[3m\"source env_setup.sh\"\e[0m\e[31m instead.\e[0m"
    echo -e "For more information, please check \e[3m\"source env_setup.sh --help\"\e[0m for more usages."
    return 1 2> /dev/null; exit 1
else
    echo -e "\t\e[32mTrue\e[0m"
fi

echo -en "\e[0m        OS: \t\e[0m"
if [[ ${_CS348_PROJECT_VERIFIED_OS} == True ]]; then
    echo -e "\e[32m${_CS348_PROJECT_OS} (VERIFIED)\e[0m"
else
    echo -e "\e[31m${_CS348_PROJECT_OS} (NOT VERIFIED)\e[0m"
    echo -e "\e[33m[WARNING] Not verified OS setup may cause unexpected error.\e[0m"
    echo -e "Would you like to continue anyway? [y/N]\e[0m"
    read _USER_ANSWER
    if [[ ${_USER_ANSWER} =~ (y|Y)((e|E)(s|S))? ]]; then
        echo -e "\e[32mProceeding the setup\e[0m"
    else
        echo -e "\e[31mAborting the setup\e[0m"
        return 1 2> /dev/null; exit 1
    fi
fi

echo -e "\e[0m     SHELL: \t\e[32m${SHELL}\e[0m"
echo -e "\e[0m      ROOT: \t\e[32m${CS348_PROJECT_ROOT}\e[0m"

echo -e ""
echo -en "\e[36mVERIFYING DOCKER ----------- \e[0m"
docker --version 1> /dev/null 2> /dev/null
if [[ ${?} -eq 0 ]]; then
    echo -e "\e[32mSuccess!\e[0m"
else
    echo -e "\e[32mdocker not found\e[0m"
    cd ${_CS348_PROJECT_INITIAL_DIR}
    return 1 2> /dev/null; exit 1
fi

echo -en "\e[36mVERIFYING DOCKER-COMPOSE --- \e[0m"
docker-compose --version 1> /dev/null 2> /dev/null
if [[ ${?} -eq 0 ]]; then
    echo -e "\e[32mSuccess!\e[0m"
else
    echo -e "\e[32mdocker-compose not found\e[0m"
    cd ${_CS348_PROJECT_INITIAL_DIR}
    return 1 2> /dev/null; exit 1
fi

set_features 1> /dev/null 2> /dev/null

echo -e ""

cd ${_CS348_PROJECT_INITIAL_DIR}
instruction
echo -e ""

return 0 2> /dev/null; exit 0
