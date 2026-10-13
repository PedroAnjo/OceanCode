from .controllers.app_controller import ControladorAplicacao

def principal():
    ControladorAplicacao().executar()

if __name__ == '__main__':
    principal()
