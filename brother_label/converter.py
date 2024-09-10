#!/usr/bin/env python

from __future__ import division, unicode_literals
from builtins import str

import logging

from PIL import Image
import PIL.ImageOps, PIL.ImageChops

from . import BrotherQLUnsupportedCmd
from .labels import FormFactor
from .raster import BrotherLabelRaster

logger = logging.getLogger(__name__)

class BrotherLabelConverter(object):
    def convert(self, device, type, images,  **kwargs):
        r"""Converts one or more images to a raster instruction file.

        :param device:
            An instance of the BrotherDevice class
        :type device: :py:class:`brother_label.devices.BrotherDevice`
        :param str type:
            Type of label the printout should be on.
        :param images:
            The images to be converted. They can be filenames or instances of Pillow's Image.
        :type images: list(PIL.Image.Image) or list(str) images
        :param \**kwargs:
            See below

        :Keyword Arguments:
            * **autocut** --
              Enable cutting after printing the labels.
            * **autocut_every** --
              Specify autocut every n-th labels.
            * **autocut_end** --
              Enable cutting after the last label is printed.
            * **halfcut** --
              Enable half-cutting of labels.
            * **dither** (``bool``) --
              Instead of applying a threshold to the pixel values, approximate grey tones with dithering.
            * **compress**
            * **red**
            * **rotate**
            * **dpi_600**
            * **hq**
            * **threshold**
        """
        if not device:
            raise LookupError('No device available')
        
        label = device.labels_by_id[type]
        raster = BrotherLabelRaster(device)

        right_margin_dots = label.offset_r + device.additional_offset_r
        device_pixel_width = raster.get_pixel_width()

        autocut = kwargs.get('autocut', True)
        autocut_every = kwargs.get('autocut_every', 1)
        autocut_end = kwargs.get('autocut_end', True)
        halfcut = kwargs.get('halfcut', True)
        dither = kwargs.get('dither', False)
        compress = kwargs.get('compress', True)
        red = kwargs.get('red', False)
        rotate = kwargs.get('rotate', 'auto')
        if rotate != 'auto': rotate = int(rotate)
        dpi_600 = kwargs.get('dpi_600', False)
        hq = kwargs.get('hq', True)
        threshold = kwargs.get('threshold', 70)
        threshold = 100.0 - threshold
        threshold = min(255, max(0, int(threshold/100.0 * 255)))

        if red and not device.two_color:
            raise BrotherQLUnsupportedCmd('Printing in red is not supported with the selected model.')

        try:
            raster.add_switch_mode()
        except BrotherQLUnsupportedCmd:
            pass
        raster.add_invalidate()
        raster.add_initialize()
        try:
            raster.add_switch_mode()
        except BrotherQLUnsupportedCmd:
            pass

        for x, image in enumerate(images):
            if isinstance(image, Image.Image):
                im = image
            else:
                try:
                    im = Image.open(image)
                except:
                    raise NotImplementedError("The image argument needs to be an Image() instance, the filename to an image, or a file handle.")

            if im.mode.endswith('A'):
                # place in front of white background and get red of transparency
                bg = Image.new("RGB", im.size, (255,255,255))
                bg.paste(im, im.split()[-1])
                im = bg
            elif im.mode == "P":
                # Convert GIF ("P") to RGB
                im = im.convert("RGB" if red else "L")
            elif im.mode == "L" and red:
                # Convert greyscale to RGB if printing on black/red tape
                im = im.convert("RGB")

            if dpi_600:
                dots_expected = [el*2 for el in label.dots_printable]
            else:
                dots_expected = label.dots_printable

            if label.form_factor in (FormFactor.ENDLESS, FormFactor.PTOUCH_ENDLESS):
                if rotate not in ('auto', 0):
                    im = im.rotate(rotate, expand=True)
                if dpi_600:
                    im = im.resize((im.size[0]//2, im.size[1]))
                if im.size[0] != label.dots_printable[0]:
                    hsize = int((label.dots_printable[0] / im.size[0]) * im.size[1])
                    im = im.resize((label.dots_printable[0], hsize), Image.NEAREST)
                    logger.warning('Need to resize the image...')
                if im.size[0] < device_pixel_width:
                    new_im = Image.new(im.mode, (device_pixel_width, im.size[1]), (255,)*len(im.mode))
                    new_im.paste(im, (device_pixel_width-im.size[0]-right_margin_dots, 0))
                    im = new_im
            elif label.form_factor in (FormFactor.DIE_CUT, FormFactor.ROUND_DIE_CUT):
                if rotate == 'auto':
                    if im.size[0] == dots_expected[1] and im.size[1] == dots_expected[0]:
                        im = im.rotate(90, expand=True)
                elif rotate != 0:
                    im = im.rotate(rotate, expand=True)
                if im.size[0] != dots_expected[0] or im.size[1] != dots_expected[1]:
                    raise ValueError("Bad image dimensions: %s. Expecting: %s." % (im.size, dots_expected))
                if dpi_600:
                    im = im.resize((im.size[0]//2, im.size[1]))
                new_im = Image.new(im.mode, (device_pixel_width, dots_expected[1]), (255,)*len(im.mode))
                new_im.paste(im, (device_pixel_width-im.size[0]-right_margin_dots, 0))
                im = new_im

            if red:
                filter_h = lambda h: 255 if (h <  40 or h > 210) else 0
                filter_s = lambda s: 255 if s > 100 else 0
                filter_v = lambda v: 255 if v >  80 else 0
                red_im = self.hsv_filter(im, filter_h, filter_s, filter_v)
                red_im = red_im.convert("L")
                red_im = PIL.ImageOps.invert(red_im)
                red_im = red_im.point(lambda x: 0 if x < threshold else 255, mode="1")

                filter_h = lambda h: 255
                filter_s = lambda s: 255
                filter_v = lambda v: 255 if v <  80 else 0
                black_im = self.hsv_filter(im, filter_h, filter_s, filter_v)
                black_im = black_im.convert("L")
                black_im = PIL.ImageOps.invert(black_im)
                black_im = black_im.point(lambda x: 0 if x < threshold else 255, mode="1")
                black_im = PIL.ImageChops.subtract(black_im, red_im)
            else:
                im = im.convert("L")
                im = PIL.ImageOps.invert(im)

                if dither:
                    im = im.convert("1", dither=Image.FLOYDSTEINBERG)
                else:
                    im = im.point(lambda x: 0 if x < threshold else 255, mode="1")

            raster.add_status_information()
            tape_size = label.tape_size
            if label.form_factor in (FormFactor.DIE_CUT, FormFactor.ROUND_DIE_CUT):
                raster.mtype = 0x0B
                raster.mwidth = tape_size[0]
                raster.mlength = tape_size[1]
            elif label.form_factor in (FormFactor.ENDLESS, ):
                raster.mtype = 0x0A
                raster.mwidth = tape_size[0]
                raster.mlength = 0
            elif label.form_factor in (FormFactor.PTOUCH_ENDLESS, ):
                raster.mtype = 0x00
                raster.mwidth = tape_size[0]
                raster.mlength = 0
            raster.pquality = int(hq)
            raster.add_media_and_quality(im.size[1])
            try:
                if autocut:
                    raster.add_autocut(True)
                    raster.add_cut_every(autocut_every)
            except BrotherQLUnsupportedCmd:
                pass
            try:
                raster.dpi_600 = dpi_600
                raster.autocut_end = autocut_end
                raster.halfcut = halfcut
                raster.two_color_printing = True if red else False
                raster.add_expanded_mode()
            except BrotherQLUnsupportedCmd:
                pass
            raster.add_margins(label.feed_margin)
            try:
                if compress: raster.add_compression(True)
            except BrotherQLUnsupportedCmd:
                pass
            if red:
                raster.add_raster_data(black_im, red_im)
            else:
                raster.add_raster_data(im)

            raster.add_print(
                last_page=x >= len(images) - 1
            )

        return raster.data

    def hsv_filter(self, im, filter_h, filter_s, filter_v, default_col=(255,255,255)):
        """ https://stackoverflow.com/a/22237709/183995 """

        hsv_im = im.convert('HSV')
        H, S, V = 0, 1, 2
        hsv = hsv_im.split()
        mask_h = hsv[H].point(filter_h)
        mask_s = hsv[S].point(filter_s)
        mask_v = hsv[V].point(filter_v)

        Mdat = []
        for h, s, v in zip(mask_h.getdata(), mask_s.getdata(), mask_v.getdata()):
            Mdat.append(255 if (h and s and v) else 0)

        mask = mask_h
        mask.putdata(Mdat)

        filtered_im = Image.new("RGB", im.size, color=default_col)
        filtered_im.paste(im, None, mask)
        return filtered_im
