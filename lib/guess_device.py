import platform

def guess_device():
    # returns the system type win/mac/rpi/None
    device = platform.uname()

    system = device[0]
    name = device[1]
    chip_type = device[4]
    processor = device[5]

    if system.lower() == "windows":
        return 'win'
    elif 'mac' in system.lower():
        return 'mac'
    elif system.lower() == "linux":
        if name.lower() == 'raspberrypi' or 'armv' in chip_type.lower():
            return 'rpi'
        return None
    return None

if __name__ == "__main__":
    print(guess_device())