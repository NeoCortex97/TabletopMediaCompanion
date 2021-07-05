from Launchpad.SysexFields import MagicField, FunctionField, LayoutField
from MidiCs.Field import ManufacturerField
from functools import partial


# Layout                        34, <Layout>
# Led Color palette             10, <LED> <Color>
# Column Color palette          12, <Column>, <Color>
# row color palette             13, <Row>, <Colour>
# All leds palette              14, <Color>
# Flash palette                 35, 0, <LED> <Color>
# Pulse palette                 40, 0 <LED> <Color>
# Led Color RGB                 11, <LED>, <Red> <Green> <Blue>
# Initialize fader              43, <Number> <Type> <Color> <Value>
# Scroll text                   20, <Color> <Loop> <Text>
# Stop scrolling (empty string) 20
# Scrolling finished            21

# Version Inquiry
# (240, 0, 32, 41, 0, , 247)

# Force bootloader
# (240, 0, 32, 41, 0, 113, 0, 105, 247)


LAYOUT_MESSAGE_TEMPLATE = [ManufacturerField, MagicField, partial(FunctionField, content='CHANGE_LAYOUT'), LayoutField]
LED_COLOR_BY_PALETTE_TEMPLATE = [ManufacturerField, MagicField, partial(FunctionField, content='LED_PALETTE'), ]
