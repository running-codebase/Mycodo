# coding=utf-8
import copy

from flask_babel import lazy_gettext

from mycodo.inputs.base_input import AbstractInput
from mycodo.utils.constraints_pass import constraints_pass_positive_value

# todo: This does not yet include temperature compensation
# todo or calibration

# Measurements
measurements_dict = {
    0: {
        'measurement': 'electrical_conductivity',
        'unit': 'uS_cm'
    }
}


# Input information
INPUT_INFORMATION = {
    'input_name_unique': 'ANYLEAF_EC',
    'input_manufacturer': 'AnyLeaf',
    'input_name': 'AnyLeaf EC',
    'input_library': 'anyleaf',
    'measurements_name': 'Electrical Conductivity',
    'measurements_dict': measurements_dict,
    'url_manufacturer': 'https://www.anyleaf.org/ec-module',
    'url_datasheet': 'https://www.anyleaf.org/static/ec-module-datasheet.pdf',

    'options_enabled': [
        'uart_location',
        'period',
    ],

    'dependencies_module': [
        ('apt', 'libjpeg-dev', 'libjpeg-dev'),
        ('apt', 'zlib1g-dev', 'zlib1g-dev'),
        ('pip-pypi', 'PIL', 'Pillow==8.1.2'),
        ('apt', 'python3-scipy', 'python3-scipy'),
        ('pip-pypi', 'usb.core', 'pyusb==1.1.1'),
        ('pip-pypi', 'adafruit_extended_bus', 'Adafruit-extended-bus==1.0.1'),
        ('pip-pypi', 'anyleaf', 'anyleaf==0.1.8.1')
    ],

    'interfaces': ['UART'],
    'uart_location': '/dev/serial0',
    'uart_baud_rate': 9600,

    'custom_options': [
        {
            'id': 'K',
            'type': 'float',
            'default_value': 1.0,
            'name': "{}".format(lazy_gettext('K')),  # todo: What should this be?
            'phrase': 'Conductivity constant K',
        }
    ],
    'custom_actions_message': """""",
    'custom_actions': [
    ]
}


class InputModule(AbstractInput):
    """A sensor support class that monitors AnyLeaf sensor conductivity (EC)"""

    def __init__(self, input_dev, testing=False):
        super(InputModule, self).__init__(input_dev, testing=testing, name=__name__)

        self.sensor = None

        if not testing:
            self.initialize_input()

    def initialize_input(self):
        from anyleaf import EcSensor

        if self.get_custom_option("K"):
            k = self.get_custom_option("K")
        else:
            k = 1.0

        self.sensor = EcSensor(K=k)

    def get_measurement(self):
        """ Gets the measurement """
        self.return_dict = copy.deepcopy(measurements_dict)

        if not self.sensor:
            self.logger.error("Input not set up")
            return

        # todo: Adjust this line once you've added temperature compensation.
        # self.value_set(0, self.sensor.read(OnBoard()))
        self.value_set(0, self.sensor.read())

        return self.return_dict
