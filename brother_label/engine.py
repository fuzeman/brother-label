import logging, time

from .backends import backend_factory, guess_backend
from .backends.network import BrotherQLBackendNetwork
from .reader import interpret_response
from .converter import BrotherLabelConverter
from .devices import BrotherDeviceManager

logger = logging.getLogger(__name__)

class BrotherLabel(object):
    def __init__(self, device=None, target=None, backend=None, strict=False):
        self.target = target
        self.strict = strict

        self.converter = BrotherLabelConverter()
        self.devices = BrotherDeviceManager()

        # Device
        if device and isinstance(device, str):
            self.device = self.devices[device]
        elif device:
            self.device = device

        # Backend
        if not backend and target:
            backend = guess_backend(target) or 'linux_kernel'

        if backend:
            backend = backend_factory(backend)

            self.list_available_devices = backend['list_available_devices']
            self.backend = backend['backend_class']
        else:
            self.list_available_devices = None
            self.backend = None

    def convert(self, type, images, device=None, **kwargs):
        if device and isinstance(device, str):
            device = self.devices[device]

        return self.converter.convert(device or self.device, type, images, **kwargs)

    def discover(self):
        if not self.backend:
            raise LookupError('No backend available')
        
        return self.list_available_devices()
    
    def print(self, type, images, target=None, backend=None, blocking=True,  **kwargs):
        instructions = self.convert(type, images, **kwargs)

        self.send(
            instructions,
            blocking=blocking,
            target=target,
            backend=backend
        )

    def send(self, instructions, target=None, backend=None, blocking=True):
        """
        Send instruction bytes to a printer.

        :param bytes instructions: The instructions to be sent to the printer.
        :param str printer_identifier: Identifier for the printer.
        :param str backend_identifier: Can enforce the use of a specific backend.
        :param bool blocking: Indicates whether the function call should block while waiting for the completion of the printing.
        """

        backend = backend_factory(backend)['backend_class'] if backend else self.backend

        if not backend:
            raise LookupError('No backend available')

        printer = backend(target or self.target)

        status = {
          'instructions_sent': True, # The instructions were sent to the printer.
          'outcome': 'unknown', # String description of the outcome of the sending operation like: 'unknown', 'sent', 'printed', 'error'
          'printer_state': None, # If the selected backend supports reading back the printer state, this key will contain it.
          'did_print': False, # If True, a print was produced. It defaults to False if the outcome is uncertain (due to a backend without read-back capability).
          'ready_for_next_job': False, # If True, the printer is ready to receive the next instructions. It defaults to False if the state is unknown.
        }

        start = time.time()
        logger.info('Sending instructions to the printer. Total: %d bytes.', len(instructions))
        printer.write(instructions)
        status['outcome'] = 'sent'

        if not blocking:
            return status

        if backend == BrotherQLBackendNetwork:
            """ No need to wait for completion. The network backend doesn't support readback. """
            return status

        while time.time() - start < 10:
            data = printer.read()
            if not data:
                time.sleep(0.005)
                continue
            try:
                result = interpret_response(data)
            except ValueError:
                logger.error("TIME %.3f - Couln't understand response: %s", time.time()-start, data)
                continue
            status['printer_state'] = result
            logger.debug('TIME %.3f - result: %s', time.time()-start, result)
            if result['errors']:
                logger.error('Errors occured: %s', result['errors'])
                status['outcome'] = 'error'
                break
            if result['status_type'] == 'Printing completed':
                status['did_print'] = True
                status['outcome'] = 'printed'
            if result['status_type'] == 'Phase change' and result['phase_type'] == 'Waiting to receive':
                status['ready_for_next_job'] = True
            if status['did_print'] and status['ready_for_next_job']:
                break

        if not status['did_print']:
            logger.warning("'printing completed' status not received.")
        if not status['ready_for_next_job']:
            logger.warning("'waiting to receive' status not received.")
        if (not status['did_print']) or (not status['ready_for_next_job']):
            logger.warning('Printing potentially not successful?')
        if status['did_print'] and status['ready_for_next_job']:
            logger.info("Printing was successful. Waiting for the next job.")

        return status
