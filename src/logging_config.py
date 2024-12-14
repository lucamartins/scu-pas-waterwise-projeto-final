import logging
from colorama import Fore, Style, init

init(autoreset=True)

class ColorfulFormatter(logging.Formatter):
    """
    Formatter customizado para adicionar cores às mensagens de log.
    """
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"

def get_custom_logger(name: str) -> logging.Logger:
    """
    Cria e configura um logger customizado com cores.
    :param name: Nome do logger.
    :return: Logger configurado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Ajuste o nível conforme necessário

    # Cria um handler para exibir logs no console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Define o formato das mensagens
    formatter = ColorfulFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Adiciona o handler ao logger
    logger.addHandler(console_handler)

    return logger