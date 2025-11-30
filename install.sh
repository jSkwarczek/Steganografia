if [ -z "$(command -v python3)" ]
then
    echo "python3 is not installed!"
    exit 1
fi

python3 -m venv .venv

if [ $? -ne 0 ]
then
    echo "error: failed to create python venv"
    exit 1
fi

source .venv/bin/activate

if [ $? -ne 0 ]
then
    echo "error: failed to activate python venv"
    exit 1
fi

pip install -U pip setuptools

if [ $? -ne 0 ]
then
    echo "error: failed to update pip and setuptools"
    exit 1
fi

pip install -r requirements.txt

if [ $? -ne 0 ]
then
    echo "error: failed to install dependencies"
    exit 1
fi

mkdocs build

if [ $? -ne 0 ]
then
    echo "error: failed to build documentation, 'help' will not be available in GUI"
    exit 1
fi

echo "Environment was successfully set up. You can activate it with 'source .venv/bin/activate'"
