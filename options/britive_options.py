import click
from options.tenant import option as tenant
from options.token import option as token
from options.output_format import option as output_format
from options.alias import option as alias
from options.blocktime import option as blocktime
from options.mode import option as mode
from options.maxpolltime import option as maxpolltime
from options.version import option as version
from options.configure_tenant import option as configure_tenant
from options.configure_alias import option as configure_alias
from options.configure_prompt import option as configure_prompt

options_map = {
    'tenant': tenant,
    'token': token,
    'format': output_format,
    'output_format': output_format,
    'alias': alias,
    'blocktime': blocktime,
    'mode': mode,
    'maxpolltime': maxpolltime,
    'version': version,
    'configure_tenant': configure_tenant,
    'configure_alias': configure_alias,
    'configure_prompt': configure_prompt
}


def britive_options(*args, **kwargs):
    def inner(f):
        names = [n.strip() for n in kwargs['names'].split(',')]
        names.reverse()
        for name in names:
            option = options_map.get(name)
            if not name:
                click.echo(f'Invalid option {name} provided.')
                exit()
            f = option(f)
        return f
    return inner

