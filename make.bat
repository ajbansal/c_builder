cd %~dp0
echo off
path="C:\Anaconda3";"C:\Anaconda3\Scripts";%path%
echo %path%

if %1%==test (
    python setup.py test
)

if %1%==upload_test (
    rmdir dist /s /q
    python setup.py sdist
    echo "YOU ARE UPLOADING TO MAIN PYPI REPO"
    echo "Checklist"
    echo "1. Have you done the readme?"
    set /p proceed=Do you want to proceed [yes/no]?
    if %proceed%==yes (
        twine upload --repository pypitest dist/*
    )
)

if %1%==upload_main (
    rmdir dist /s /q
    python setup.py sdist
    echo "YOU ARE UPLOADING TO MAIN PYPI REPO"
    echo "Checklist"
    echo "1. Have you done the readme?"
    set /p proceed=Do you want to proceed [yes/no]?
    if %proceed%==yes (
        twine upload --repository pypi dist/*
    )
)

