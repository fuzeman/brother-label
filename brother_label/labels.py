from enum import IntEnum, StrEnum
import attrs
import re

from .core import ElementManager

MEDIA_ENDLESS_PATTERN = re.compile(r"^(?P<width>\d+)(?P<color>red)?$")
MEDIA_RECT_PATTERN = re.compile(r"^(?P<width>\d+)x(?P<height>\d+)$")
MEDIA_ROUND_PATTERN = re.compile(r"^d(?P<diameter>\d+)$")

class Media(StrEnum):
    ENDLESS_6       = "6"
    ENDLESS_9       = "9"
    ENDLESS_12      = "12"
    ENDLESS_18      = "18"
    ENDLESS_24      = "24"
    ENDLESS_29      = "29"
    ENDLESS_36      = "36"
    ENDLESS_38      = "38"
    ENDLESS_50      = "50"
    ENDLESS_54      = "54"
    ENDLESS_62      = "62"
    ENDLESS_62_RED  = "62red"
    ENDLESS_102     = "102"
    ENDLESS_103     = "103"
    ENDLESS_104     = "104"

    RECT_17x54      = "17x54"
    RECT_17x87      = "17x87"
    RECT_23x23      = "23x23"
    RECT_29x42      = "29x42"
    RECT_29x90      = "29x90"
    RECT_39x48      = "39x48"
    RECT_39x90      = "39x90"
    RECT_52x29      = "52x29"
    RECT_54x29      = "54x29"
    RECT_60x86      = "60x86"
    RECT_62x29      = "62x29"
    RECT_62x100     = "62x100"
    RECT_102x51     = "102x51"
    RECT_102x152    = "102x152"
    RECT_103x164    = "103x164"

    ROUND_12        = "d12"
    ROUND_24        = "d24"
    ROUND_58        = "d58"

    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj.description = cls.describe(value)
        return obj

    @classmethod
    def describe(cls, value):
        # Endless
        match = MEDIA_ENDLESS_PATTERN.match(value)
        if match:
            out = '{0}mm endless'.format(match.group('width'))

            if match.group('color') == 'red':
                out += ' (black/red/white)'

            return out

        # Rectangle
        match = MEDIA_RECT_PATTERN.match(value)
        if match:
            return '{0}mm x {1}mm die-cut'.format(match.group('width'), match.group('height'))

        # Round
        match = MEDIA_ROUND_PATTERN.match(value)
        if match:
            return '{0}mm round die-cut'.format(match.group('diameter'))

        return 'unknown media ({0})'.format(value)


class FormFactor(IntEnum):
    """
    Enumeration representing the form factor of a label.
    The labels for the Brother QL series are supplied either as die-cut (pre-sized), or for more flexibility the
    continuous label tapes offer the ability to vary the label length.
    """
    #: rectangular die-cut labels
    DIE_CUT = 1
    #: endless (continouse) labels
    ENDLESS = 2
    #: round die-cut labels
    ROUND_DIE_CUT = 3
    #: endless P-touch labels
    PTOUCH_ENDLESS = 4

class Color(IntEnum):
    """
    Enumeration representing the colors to be printed on a label. Most labels only support printing black on white.
    Some newer ones can also print in black and red on white.
    """
    #: The label can be printed in black & white.
    BLACK_WHITE = 0
    #: The label can be printed in black, white & red.
    BLACK_RED_WHITE = 1

@attrs.define
class Label(object):
    """
    This class represents a label. All specifics of a certain label
    and what the rasterizer needs to take care of depending on the
    label choosen, should be contained in this class.
    """
    #: The media type of the given label, must be unique per device. Eg. `Media.ENDLESS_29`.
    media: Media
    #: Additional media aliases for the given label.
    aliases: [str]
    #: The tape size of a single label (width, lenght) in mm. For endless labels, the length is 0 by definition.
    tape_size: (int, int)
    #: The type of label
    form_factor: FormFactor
    #: The total area (width, length) of the label in dots (@300dpi).
    dots_total: (int, int)
    #: The printable area (width, length) of the label in dots (@300dpi).
    dots_printable: (int, int)
    #: The required offset from the right side of the label in dots to obtain a centered printout.
    offset_r: int
    #: An additional amount of feeding when printing the label.
    #: This is non-zero for some smaller label sizes and for endless labels.
    feed_margin: int = 0
    #: Some labels allow printing in red, most don't.
    color: Color = Color.BLACK_WHITE

    def works_with_model(self, model): # type: bool
        """
        Method to determine if certain label can be printed by the specified printer model.
        """
        if self.restricted_to_models and model not in models: return False
        else: return True

    @property
    def identifiers(self): # type: [str]
        return [self.media] + self.aliases

    @property
    def name(self): # type: str
        return self.media.description
    