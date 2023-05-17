class UsbCable:
    def __init__(self) -> None:
        self.isPlugged = False

    def plubUsb(self):
        self.isPlugged = True


class UsbPort:
    def __init__(self) -> None:
        self.portAvailable = True

    def plub(self, usb):
        if self.portAvailable:
            usb.plubUsb()
            self.portAvailable = False


# Plug directly into usb ports
usbCable = UsbCable()
usbPort1 = UsbPort()
usbPort1.plub(usbCable)

# not compatible with usb cable
class MicroUsbCable:
    def __init__(self) -> None:
        self.isPlugged = False

    def plubMicroUsb(self):
        self.isPlugged = True


class MicroToUsbAdapter(UsbCable):
    def __init__(self, microUsbCable):
        self.microUsbCable = microUsbCable
        self.microUsbCable.plubMicroUsb()


microToUsbAdpater = MicroToUsbAdapter(MicroUsbCable)
usbPort2 = UsbPort()
usbPort2.plub(microToUsbAdpater)
