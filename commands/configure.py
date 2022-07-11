import click
from choices.output_format import output_format_choices
from options.britive_options import britive_options
from helpers.build_britive import build_britive


@click.group()
def configure():
    """
    Configures the PyBritive CLI.
    """


@configure.command()
@build_britive
@britive_options(names='configure_tenant,configure_alias,format,configure_prompt')
def tenant(ctx, configure_tenant, configure_alias, output_format, configure_prompt):
    """
    Configures tenant level settings for the PyBritive CLI.

    If CLI options/flags are not provided an interactive data entry process will collect any needed data.
    """
    tenant_name = configure_tenant
    no_prompt = configure_prompt
    alias = configure_alias
    output_format = output_format

    if not no_prompt:
        if not tenant_name:
            tenant_name = click.prompt(
                'The name of the tenant: [tenant].britive-app.com',
                type=str
            )
        if not alias:
            alias = click.prompt(
                'Optional alias for the above tenant. This alias would be used with the `--tenant` flag',
                default=tenant_name,
                type=str
            )
        if not output_format:
            output_format = click.prompt(
                'Output format (csv|json|table|yaml): ',
                default='json',
                type=output_format_choices
            )

    if not tenant_name  or len(tenant_name.strip()) == 0:
        raise click.ClickException('Tenant Name not provided.')
    if not alias:
        alias = tenant_name
    if not output_format or output_format not in output_format_choices.choices:
        ctx.obj.britive.print(f'Invalid output format {output_format} provided. Defaulting to "json".')
        output_format = 'json'

    ctx.obj.britive.configure_tenant(
        tenant=tenant_name,
        alias=alias,
        output_format=output_format
    )


@configure.command(name='global')  # have to specify the name since global is a reserved word
@build_britive
@britive_options(names='configure_tenant,format,configure_prompt')
def global_command(ctx, configure_tenant, output_format, configure_prompt):
    """
    Configures global level settings for the PyBritive CLI.

    If CLI options/flags are not provided an interactive data entry process will collect any needed data.
    """
    default_tenant_name = configure_tenant
    no_prompt = configure_prompt
    output_format = output_format

    if not no_prompt:
        if not default_tenant_name:
            default_tenant_name = click.prompt(
                'The default tenant name',
                type=str
            )
        if not output_format:
            output_format = click.prompt(
                'Output format (csv|json|table|yaml): ',
                default='json',
                type=output_format_choices
            )
        if not output_format or output_format not in output_format_choices.choices:
            ctx.obj.britive.print(f'Invalid output format {output_format} provided. Defaulting to "json".')
            output_format = 'json'

    ctx.obj.britive.configure_global(
        default_tenant_name=default_tenant_name,
        output_format=output_format
    )


@configure.command(name='import')  # have to specify the name since import is a reserved word
@build_britive
@britive_options(names='silent')
def import_command(ctx, silent):  # silent is handled by @build_britive
    """
    Import an existing configuration from the Node.js/NPM version of the Britive CLI.
    """
    ctx.obj.britive.import_existing_npm_config()
