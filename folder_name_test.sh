INVALID_FOLDER_NAMES=$(ls -d ./*/*[[:upper:]]* 2> /dev/null)
if [[ $INVALID_FOLDER_NAMES ]]; then
    for INVALID_FOLDER_NAME in $INVALID_FOLDER_NAMES
    do 
        echo "::error file=$INVALID_FOLDER_NAME::Folder names must be lowercase"
    done
    exit 1
else
    echo "Folder name check success!"
    exit 0
fi

