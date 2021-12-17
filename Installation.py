import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

# Example
if __name__ == '__main__':
    install('configparser')
    install('matplotlib')
    install('numpy')
    install('opencv-python')
    install('PyAudio')
    install('PyQt5')
    install('pygrabber')
    install('Sphinx')
    install('sphinx-rtd-theme')
    install('scikit-learn')
    install('sphinx-panels')
    install('pip-review')
    install('pipwin')
    install('pyinstaller')
    install('TextGrid')
    install('xmltodict')