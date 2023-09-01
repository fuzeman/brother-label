#!/usr/bin/env python

# Python standard library
from __future__ import print_function
import logging

# external dependencies
import click

# imports from this very package
from .backends import available_backends
from .devices import BrotherDeviceManager


logger = logging.getLogger('brother_label')


printer_help = "The identifier for the printer. This could be a string like tcp://192.168.1.21:9100 for a networked printer or usb://0x04f9:0x2015/000M6Z401370 for a printer connected via USB."
@click.group()
@click.option('-b', '--backend', type=click.Choice(available_backends), envvar='BROTHER_LABEL_BACKEND')
@click.option('-m', '--device', type=click.Choice(BrotherDeviceManager().keys()), envvar='BROTHER_LABEL_DEVICE')
@click.option('-p', '--target', metavar='TARGET', envvar='BROTHER_LABEL_TARGET', help=printer_help)
@click.option('--debug', is_flag=True)
@click.version_option()
@click.pass_context
def cli(ctx, *args, **kwargs):
    """ Command line interface for the brother_label Python package. """

    backend = kwargs.get('backend', None)
    device = kwargs.get('device', None)
    target = kwargs.get('target', None)
    debug = kwargs.get('debug')

    # Store the general CLI options in the context meta dictionary.
    # The name corresponds to the second half of the respective envvar:
    ctx.meta['DEVICE'] = device
    ctx.meta['BACKEND'] = backend
    ctx.meta['TARGET'] = target

    logging.basicConfig(level='DEBUG' if debug else 'INFO')

@cli.command('discover')
@click.pass_context
def discover_cmd(ctx):
    """ find connected label printers """
    from .engine import BrotherLabel
    
    brother = BrotherLabel(
        ctx.meta.get('DEVICE'),
        backend=ctx.meta.get('BACKEND', 'pyusb'),
        strict=True
    )
    
    print('Available Devices:')
    print()

    for ad in brother.discover():
        print(ad['identifier'])

@cli.group()
@click.pass_context
def info(ctx, *args, **kwargs):
    """ list available labels, models etc. """

@info.command('devices')
@click.pass_context
def devices_cmd(ctx, *args, **kwargs):
    """
    List the choices for --model
    """
    print('Supported Devices:')
    print()

    for model in BrotherDeviceManager().keys():
        print("" + model)

@info.command('labels')
@click.pass_context
def labels_cmd(ctx, *args, **kwargs):
    """
    List the choices for --label
    """
    from .labels import FormFactor

    fmt = "{name:36s} {dots_printable:24s} {identifiers:26s}"

    print("Supported Labels:")
    print()
    print(fmt.format(
        name="\tName",
        dots_printable="Printable (dots)",
        identifiers="Identifiers"
    ))
    print("=" * 128)

    for device in BrotherDeviceManager().values():
        print("" + device.identifier)

        for label in device.labels:
            if label.form_factor in (FormFactor.DIE_CUT, FormFactor.ROUND_DIE_CUT):
                dp_fmt = "{0:4d} x {1:4d}"
            elif label.form_factor in (FormFactor.ENDLESS, FormFactor.PTOUCH_ENDLESS):
                dp_fmt = "{0:4d}"
            else:
                dp_fmt = " - unknown - "

            print(fmt.format(
                name=f"\t{label.name}",
                dots_printable=dp_fmt.format(*label.dots_printable),
                identifiers=', '.join(label.identifiers)
            ))
        
        print()

@info.command('env')
@click.pass_context
def env_cmd(ctx, *args, **kwargs):
    """
    print debug info about running environment
    """
    import sys, platform, os, shutil
    from pkg_resources import get_distribution, working_set
    print("\n##################\n")
    print("Information about the running environment of brother_label.")
    print("(Please provide this information when reporting any issue.)\n")
    # computer
    print("About the computer:")
    for attr in ('platform', 'processor', 'release', 'system', 'machine', 'architecture'):
        print('  * '+attr.title()+':', getattr(platform, attr)())
    # Python
    print("About the installed Python version:")
    py_version = str(sys.version).replace('\n', ' ')
    print("  *", py_version)
    # brother_label
    print("About the brother_label package:")
    pkg = get_distribution('brother_label')
    print("  * package location:", pkg.location)
    print("  * package version: ", pkg.version)
    try:
        cli_loc = shutil.which('brother_label')
    except:
        cli_loc = 'unknown'
    print("  * brother_label CLI path:", cli_loc)
    # brother_label's requirements
    print("About the requirements of brother_label:")
    fmt = "  {req:14s} | {spec:10s} | {ins_vers:17s}"
    print(fmt.format(req='requirement', spec='requested', ins_vers='installed version'))
    print(fmt.format(req='-' * 14, spec='-'*10, ins_vers='-'*17))
    requirements = list(pkg.requires())
    requirements.sort(key=lambda x: x.project_name)
    for req in requirements:
        proj = req.project_name
        req_pkg = get_distribution(proj)
        spec = ' '.join(req.specs[0]) if req.specs else 'any'
        print(fmt.format(req=proj, spec=spec, ins_vers=req_pkg.version))
    print("\n##################\n")

@cli.command('create', short_help='create a label')
@click.argument('images', nargs=-1, type=click.File('rb'), metavar='IMAGE [IMAGE] ...')
@click.argument('out', nargs=1, type=click.File('wb'), metavar='OUT')
@click.option('-t', '--type', envvar='BROTHER_QL_LABEL', help='The label (size, type - die-cut or endless). Run `brother_label info labels` for a full list including ideal pixel dimensions.')
@click.option('-r', '--rotate', type=click.Choice(('auto', '0', '90', '180', '270')), default='auto', help='Rotate the image (counterclock-wise) by this amount of degrees.')
@click.option('-t', '--threshold', type=float, default=70.0, help='The threshold value (in percent) to discriminate between black and white pixels.')
@click.option('-d', '--dither', is_flag=True, help='Enable dithering when converting the image to b/w. If set, --threshold is meaningless.')
@click.option('--red', is_flag=True, help='Create a label to be printed on black/red/white tape (only with QL-8xx series on DK-22251 labels). You must use this option when printing on black/red tape, even when not printing red.')
@click.option('--600dpi', 'dpi_600', is_flag=True, help='Print with 600x300 dpi available on some models. Provide your image as 600x600 dpi; perpendicular to the feeding the image will be resized to 300dpi.')
@click.option('--lq', is_flag=True, help='Print with low quality (faster). Default is high quality.')
@click.option('--no-compress', is_flag=True, help='Disable compression.')
@click.option('--no-cut', is_flag=True, help="Don't cut the tape after printing the label.")
@click.pass_context
def create_cmd(ctx, no_compress, no_cut, *args, **kwargs):
    """ Create a label of the provided IMAGE. """
    from .engine import BrotherLabel

    brother = BrotherLabel(
        ctx.meta.get('DEVICE'),
        strict=True
    )
    instructions = brother.convert(
        compress=not no_compress,
        cut=not no_cut,
        **kwargs
    )
    kwargs['out'].write(instructions)

@cli.command('print', short_help='print a label')
@click.argument('images', nargs=-1, type=click.File('rb'), metavar='IMAGE [IMAGE] ...')
@click.option('-t', '--type', envvar='BROTHER_QL_LABEL', help='The label (size, type - die-cut or endless). Run `brother_label info labels` for a full list including ideal pixel dimensions.')
@click.option('-r', '--rotate', type=click.Choice(('auto', '0', '90', '180', '270')), default='auto', help='Rotate the image (counterclock-wise) by this amount of degrees.')
@click.option('-t', '--threshold', type=float, default=70.0, help='The threshold value (in percent) to discriminate between black and white pixels.')
@click.option('-d', '--dither', is_flag=True, help='Enable dithering when converting the image to b/w. If set, --threshold is meaningless.')
@click.option('--red', is_flag=True, help='Create a label to be printed on black/red/white tape (only with QL-8xx series on DK-22251 labels). You must use this option when printing on black/red tape, even when not printing red.')
@click.option('--600dpi', 'dpi_600', is_flag=True, help='Print with 600x300 dpi available on some models. Provide your image as 600x600 dpi; perpendicular to the feeding the image will be resized to 300dpi.')
@click.option('--lq', is_flag=True, help='Print with low quality (faster). Default is high quality.')
@click.option('--no-compress', is_flag=True, help='Disable compression.')
@click.option('--no-cut', is_flag=True, help="Don't cut the tape after printing the label.")
@click.pass_context
def print_cmd(ctx, no_compress, no_cut, *args, **kwargs):
    """Print a label of the provided IMAGE. """
    from .engine import BrotherLabel
    
    brother = BrotherLabel(
        ctx.meta.get('DEVICE'),
        backend=ctx.meta.get('BACKEND', 'pyusb'),
        target=ctx.meta.get('TARGET'),
        strict=True
    )

    brother.print(
        blocking=True,
        compress=not no_compress,
        cut=not no_cut,
        **kwargs
    )

@cli.command('analyze', help='interpret a binary file containing raster instructions for the Brother QL-Series printers')
@click.argument('instructions', type=click.File('rb'))
@click.option('-f', '--filename-format', help="Filename format string. Default is: label{counter:04d}.png.")
@click.pass_context
def analyze_cmd(ctx, *args, **kwargs):
    from .reader import BrotherQLReader
    br = BrotherQLReader(kwargs.get('instructions'))
    if kwargs.get('filename_format'): br.filename_fmt = kwargs.get('filename_format')
    br.analyse()

@cli.command('send', short_help='send an instruction file to the printer')
@click.argument('instructions', type=click.File('rb'))
@click.pass_context
def send_cmd(ctx, *args, **kwargs):
    from .engine import BrotherLabel
    
    brother = BrotherLabel(
        ctx.meta.get('DEVICE'),
        backend=ctx.meta.get('BACKEND', 'pyusb'),
        target=ctx.meta.get('TARGET'),
        strict=True
    )

    brother.send(
        kwargs['instructions'].read(),
        blocking=True
    )

if __name__ == '__main__':
    cli()
