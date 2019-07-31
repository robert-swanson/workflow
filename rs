if [ "$1" == "" ]
then
    echo "script name expected for removal"
else
    mv ~/scripts/$1 ~/workflow/trash && rm ~/workflow/scripts/*/$1
fi
