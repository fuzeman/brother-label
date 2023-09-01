from attr import attrs, attrib
from typing import Tuple

from .core import ElementManager
from .labels import Color, FormFactor, Label

@attrs
class BrotherDevice(object):
    """
    This class represents a printer model. All specifics of a certain model
    and the opcodes it supports should be contained in this class.
    """
    #: A string identifier given to each model implemented. Eg. 'QL-500'.
    identifier = attrib(type=str)
    #: Minimum and maximum number of rows or 'dots' that can be printed.
    #: Together with the dpi this gives the minimum and maximum length
    #: for continuous tape printing.
    min_max_length_dots = attrib(type=Tuple[int, int])
    #: The minimum and maximum amount of feeding a label
    min_max_feed = attrib(type=Tuple[int, int], default=(35, 1500))
    number_bytes_per_row = attrib(type=int, default=90)
    #: The required additional offset from the right side
    additional_offset_r = attrib(type=int, default=0)
    #: Support for the 'mode setting' opcode
    mode_setting = attrib(type=bool, default=True)
    #: Model has a cutting blade to automatically cut labels
    cutting = attrib(type=bool, default=True)
    #: Model has support for the 'expanded mode' opcode.
    #: (So far, all models that have cutting support do).
    expanded_mode = attrib(type=bool, default=True)
    #: Model has support for compressing the transmitted raster data.
    #: Some models with only USB connectivity don't support compression.
    compression = attrib(type=bool, default=True)
    #: Support for two color printing (black/red/white)
    #: available only on some newer models.
    two_color = attrib(type=bool, default=False)
    #: Number of NULL bytes needed for the invalidate command.
    num_invalidate_bytes = attrib(type=int, default=200)

    def __attrs_post_init__(self) -> None:
        self.labels_by_id = {}

        for label in self.labels:
            for identifier in label.identifiers:
                self.labels_by_id[identifier] = label

    @property
    def labels(self):
        return []

    @property
    def name(self):
        return self.identifier


class BrotherDeviceQL(BrotherDevice):
    @property
    def labels(self):
        return super().labels + [
            # Continuous
            Label(["12", "DK-22214"],                           ( 12,   0), FormFactor.ENDLESS,       ( 142,    0), ( 106,    0),  29 , feed_margin=35),
            Label(["18"],                                       ( 18,   0), FormFactor.ENDLESS,       ( 256,    0), ( 234,    0), 171 , feed_margin=14),
            Label(["29", "DK-22210"],                           ( 29,   0), FormFactor.ENDLESS,       ( 342,    0), ( 306,    0),   6 , feed_margin=35),
            Label(["38", "DK-22225"],                           ( 38,   0), FormFactor.ENDLESS,       ( 449,    0), ( 413,    0),  12 , feed_margin=35),
            Label(["50", "DK-22223"],                           ( 50,   0), FormFactor.ENDLESS,       ( 590,    0), ( 554,    0),  12 , feed_margin=35),
            Label(["54", "DK-N55224"],                          ( 54,   0), FormFactor.ENDLESS,       ( 636,    0), ( 590,    0),   0 , feed_margin=35),
            Label(["62", "DK-22205", "DK-44205", "DK-44605"],   ( 62,   0), FormFactor.ENDLESS,       ( 732,    0), ( 696,    0),  12 , feed_margin=35),
            Label(["62red", "DK-22251"],                        ( 62,   0), FormFactor.ENDLESS,       ( 732,    0), ( 696,    0),  12 , feed_margin=35, color=Color.BLACK_RED_WHITE),
            
            # Die-Cut
            Label(["17x54", "DK-11204"],                        ( 17,  54), FormFactor.DIE_CUT,       ( 201,  636), ( 165,  566),   0 ),
            Label(["17x87", "DK-11203"],                        ( 17,  87), FormFactor.DIE_CUT,       ( 201, 1026), ( 165,  956),   0 ),
            Label(["23x23", "DK-11221"],                        ( 23,  23), FormFactor.DIE_CUT,       ( 272,  272), ( 202,  202),  42 ),
            Label(["29x42"],                                    ( 29,  42), FormFactor.DIE_CUT,       ( 342,  495), ( 306,  425),   6 ),
            Label(["29x90", "DK-11201"],                        ( 29,  90), FormFactor.DIE_CUT,       ( 342, 1061), ( 306,  991),   6 ),
            Label(["39x90", "DK-11208"],                        ( 38,  90), FormFactor.DIE_CUT,       ( 449, 1061), ( 413,  991),  12 ),
            Label(["39x48"],                                    ( 39,  48), FormFactor.DIE_CUT,       ( 461,  565), ( 425,  495),   6 ),
            Label(["52x29"],                                    ( 52,  29), FormFactor.DIE_CUT,       ( 614,  341), ( 578,  271),   0 ),
            Label(["54x29"],                                    ( 54,  29), FormFactor.DIE_CUT,       ( 630,  341), ( 598,  271),  60 ),
            Label(["60x86", "DK-11234", "DK-12343PK"],          ( 60,  87), FormFactor.DIE_CUT,       ( 708, 1024), ( 672,  954),  18 ),
            Label(["62x29", "DK-11209"],                        ( 62,  29), FormFactor.DIE_CUT,       ( 732,  341), ( 696,  271),  12 ),
            Label(["62x100", "DK-11202"],                       ( 62, 100), FormFactor.DIE_CUT,       ( 732, 1179), ( 696, 1109),  12 ),

            # Round Die-Cut
            Label(["d12", "DK-11219"],                          ( 12,  12), FormFactor.ROUND_DIE_CUT, ( 142,  142), (  94,   94), 113 , feed_margin=35),
            Label(["d24", "DK-11218"],                          ( 24,  24), FormFactor.ROUND_DIE_CUT, ( 284,  284), ( 236,  236),  42 ),
            Label(["d58", "DK-11207"],                          ( 58,  58), FormFactor.ROUND_DIE_CUT, ( 688,  688), ( 618,  618),  51 ),
        ]

class BrotherDeviceQL10(BrotherDeviceQL):
    @property
    def labels(self):
        return super().labels + [
            # Continuous
            Label(["102", "DK-22243"],                          (102,   0), FormFactor.ENDLESS,       (1200,    0), (1164,    0),  12 , feed_margin=35),
            Label(["104"],                                      (104,   0), FormFactor.ENDLESS,       (1227,    0), (1200,    0),  -8 , feed_margin=35),
            
            # Die-Cut
            Label(["102x51", "DK-11240"],                       (102,  51), FormFactor.DIE_CUT,       (1200,  596), (1164,  526),  12),
            Label(["102x152", "DK-11241"],                      (102, 153), FormFactor.DIE_CUT,       (1200, 1804), (1164, 1660),  12),
        ]

class BrotherDeviceQL11(BrotherDeviceQL10):
    @property
    def labels(self):
        return super().labels + [
            # Continuous
            Label(["103", "DK-22246"],                          (104,   0), FormFactor.ENDLESS,       (1224,    0), (1200,    0),  12 , feed_margin=35),
            
            # Die-Cut
            Label(["103x164", "DK-11247"],                      (104, 164), FormFactor.DIE_CUT,       (1224, 1941), (1200, 1822),  12),
        ]

class BrotherDevicePT(BrotherDevice):
    @property
    def labels(self):
        return super().labels + [
            # Continuous
            Label(["12", "pt12"],                               ( 12,   0), FormFactor.PTOUCH_ENDLESS,( 170,    0), ( 150,    0),   213, feed_margin=14),
            Label(["18", "pt18"],                               ( 18,   0), FormFactor.PTOUCH_ENDLESS,( 256,    0), ( 234,    0),   171, feed_margin=14),
            Label(["24", "pt24"],                               ( 24,   0), FormFactor.PTOUCH_ENDLESS,( 128,    0), ( 128,    0),   0, feed_margin=14),
            Label(["36", "pt36"],                               ( 36,   0), FormFactor.PTOUCH_ENDLESS,( 512,    0), ( 454,    0),   61, feed_margin=14),
        ]

class BrotherDevicePTE(BrotherDevice):
    @property
    def labels(self):
        return super().labels + [
            # Continuous
            Label(["6", "pte6"],                                (  6,   0), FormFactor.PTOUCH_ENDLESS,(  42,    0), (  32,    0),  48, feed_margin=14),
            Label(["9", "pte9"],                                (  9,   0), FormFactor.PTOUCH_ENDLESS,(  64,    0), (  50,    0),  39, feed_margin=14),
            Label(["12", "pte12"],                              ( 12,   0), FormFactor.PTOUCH_ENDLESS,(  84,    0), (  70,    0),  29, feed_margin=14),
            Label(["18", "pte18"],                              ( 18,   0), FormFactor.PTOUCH_ENDLESS,( 128,    0), ( 112,    0),   8, feed_margin=14),
            Label(["24", "pte24"],                              ( 24,   0), FormFactor.PTOUCH_ENDLESS,( 170,    0), ( 128,    0),   0, feed_margin=14),
        ]

class BrotherDeviceManager(ElementManager):
    def __init__(self):
        super().__init__((
            # QL Series
            BrotherDeviceQL('QL-500',    (295, 11811), compression=False, mode_setting=False, expanded_mode=False, cutting=False),
            BrotherDeviceQL('QL-550',    (295, 11811), compression=False, mode_setting=False),
            BrotherDeviceQL('QL-560',    (295, 11811), compression=False, mode_setting=False),
            BrotherDeviceQL('QL-570',    (150, 11811), compression=False, mode_setting=False),
            BrotherDeviceQL('QL-580N',   (150, 11811)),
            BrotherDeviceQL('QL-600',    (150, 11811)),
            BrotherDeviceQL('QL-650TD',  (295, 11811)),
            BrotherDeviceQL('QL-700',    (150, 11811), compression=False, mode_setting=False),
            BrotherDeviceQL('QL-710W',   (150, 11811)),
            BrotherDeviceQL('QL-720NW',  (150, 11811)),
            BrotherDeviceQL('QL-800',    (150, 11811), two_color=True, compression=False, num_invalidate_bytes=400),
            BrotherDeviceQL('QL-810W',   (150, 11811), two_color=True, num_invalidate_bytes=400),
            BrotherDeviceQL('QL-820NWB', (150, 11811), two_color=True, num_invalidate_bytes=400),

            # QL 10 Series
            BrotherDeviceQL10('QL-1050',   (295, 35433), number_bytes_per_row=162, additional_offset_r=44),
            BrotherDeviceQL10('QL-1060N',  (295, 35433), number_bytes_per_row=162, additional_offset_r=44),
            
            # QL 11 Series
            BrotherDeviceQL11('QL-1100',   (301, 35434), number_bytes_per_row=162, additional_offset_r=44),
            BrotherDeviceQL11('QL-1100NWB',(301, 35434), number_bytes_per_row=162, additional_offset_r=44),
            BrotherDeviceQL11('QL-1115NWB',(301, 35434), number_bytes_per_row=162, additional_offset_r=44),
            
            # PT Series
            BrotherDevicePT('PT-P750W',  (31, 14172), number_bytes_per_row=16),
            BrotherDevicePT('PT-P900W',  (57, 28346), number_bytes_per_row=70),
            BrotherDevicePT('PT-P950NW', (57, 28346), number_bytes_per_row=70),

            # PTE Series
            BrotherDevicePTE('PT-E550W',  (31, 14172), number_bytes_per_row=16),
        ))
