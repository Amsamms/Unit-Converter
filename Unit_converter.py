import streamlit as st
from pint import UnitRegistry, UndefinedUnitError

# Create a unit registry
ureg = UnitRegistry()

# Get all units
all_units = sorted(list(ureg._units.keys()))

# Define the form
st.title("Unit Converter")
value = st.number_input("Enter the value to convert", value=1.0)
from_unit = st.selectbox("Select the current unit", options=all_units)
to_unit = st.selectbox("Select the unit to convert to", options=all_units)

# Perform the conversion when the Convert button is pressed
if st.button("Convert"):
    # Create a quantity with the given value and unit
    quantity = value * ureg.parse_expression(from_unit)
    
    try:
        # Try to perform the conversion
        converted_quantity = quantity.to(ureg.parse_expression(to_unit))
        st.write(f"{value} {from_unit} is equivalent to {converted_quantity.magnitude:.2f} {to_unit}")
    except Exception as e:
        st.write(f"Could not perform conversion: {e}")
        
        # Find and recommend compatible units
        from_unit_dimensionality = ureg.parse_expression(from_unit).dimensionality
        compatible_units = []
        for unit in all_units:
            try:
                if ureg.parse_expression(unit).dimensionality == from_unit_dimensionality:
                    compatible_units.append(unit)
            except UndefinedUnitError:
                continue
        
        st.markdown(f"### Here are some units that are compatible with {from_unit}:")
        columns = st.columns(4)
        for i, unit in enumerate(compatible_units):
            columns[i % 4].markdown(f"`{unit}`")
