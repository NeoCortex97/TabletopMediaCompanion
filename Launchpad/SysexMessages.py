from Launchpad.SysexFields import MagicField, FunctionField, LayoutField
from MidiCs.Field import ManufacturerField


# Layout                        34, <Layout>
# Led Color palette             10, <LED> <Colour>
# Column Color palette          12, <Column>, <Colour>
# row color palette             13, <Row>, <Colour>
# All leds palette              14, <Colour>
# Flash palette                 35, 0, <LED> <Colour>
# Pulse palette                 40, 0 <LED> <Colour>
# Led Color RGB                 11, <LED>, <Red> <Green> <Blue>
# Initialize fader              43, <Number> <Type> <Colour> <Value>
# Scroll text                   20, <Colour> <Loop> <Text>
# Stop scrolling (empty string) 20
# Scrolling finished            21

# Version Inquiry
# (240, 0, 32, 41, 0, , 247)

# Force bootloader
# (240, 0, 32, 41, 0, 113, 0, 105, 247)


LAYOUT_MESSAGE_TEMPLATE = [ManufacturerField, MagicField, FunctionField, LayoutField]
