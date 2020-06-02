class PowerInfo(object):
    def __init__(self, current_ampere: float, voltage_volts: float, power_watts: float):
        self._current = current_ampere
        self._voltage = voltage_volts
        self._power = power_watts

    @property
    def power(self) -> float:
        return self._power

    @property
    def voltage(self) -> float:
        return self._voltage

    @property
    def current(self) -> float:
        return self._current

    def __str__(self):
        return f"POWER = {self._power} W, VOLTAGE = {self._voltage} V, CURRENT = {self._current} A"
