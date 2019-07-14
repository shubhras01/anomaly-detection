from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity
ureg.define('dog_year = 52 * day = dy')