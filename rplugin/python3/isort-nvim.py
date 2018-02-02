from subprocess import PIPE, Popen

import neovim

ISORT_COMMAND = 'isort'


@neovim.plugin
class IsortNvim:

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('Isort', nargs='*', range='%', complete='file')
    def isort_command(self, args, range):
        current_buffer = self.nvim.current.buffer[range[0] - 1:range[1]]
        text = '\n'.join(current_buffer)
        output = self._isort(text)
        lines = output.split('\n')[:-1]
        self.nvim.current.buffer[:] = lines

    def error(self, msg):
        self.nvim.err_write('[isort] {}\n'.format(msg))

    def _isort(self, text, *args):
        isort_command = self.nvim.vars.get('isort_command', ISORT_COMMAND)
        isort_args = [isort_command] + list(args) + ['-']
        with Popen(isort_args, stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
            output, error = proc.communicate(input=text.encode())
            return output.decode()