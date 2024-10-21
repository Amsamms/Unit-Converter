import streamlit as st
from pint import UnitRegistry
import pint.errors
import pandas as pd

# Create a unit registry
ureg = UnitRegistry()

# Create some extra units to be in the registry
ureg.define('cubic_meter = 1e3 * liter = cu_meter')
ureg.define('square_meter = 10.76391042 * square_feet')
ureg.define('square_centimeter = 0.001076391042 * square_feet')
ureg.define('mm_H2O = 0.1 * cmH2O')
ureg.define('kilo_pascal = 1e3 * pascal')
ureg.define('mega_pascal = 1e6 * pascal')

# Get all units
all_units = sorted(list(ureg._units.keys()))
# Initialize all variables to None
selected_unit_1 = None
selected_unit_2 = None
selected_unit_3 = None
quantity_value_1 = None
quantity_value_2 = None
quantity_value_3 = None
operation_12 = None
operation_23 = None

st.markdown("""
    <div style="border: 2px solid blue; padding: 10px; border-radius: 5px;">
        <h1 style="text-align: center;">\U0001F310 Universal Unit Converter \U0001F310</h1>
    </div>
    <br/><br/>
""", unsafe_allow_html=True)

st.sidebar.title("Instructions")

st.sidebar.markdown("""
1. **Select the number of units** you want to convert. You can choose up to 3 units.

2. For each unit, **select the unit type** and **enter the quantity**. 

3. If you are converting more than one unit, **select the operation** (multiply or divide) that should be performed between the units.

4. After entering your inputs, the app will **perform the calculation** and display the result in the unit you selected. 

5. The app will also show **alternative combinations** of units that are dimensionally equivalent to the units you selected.

6. You can select one of these combinations to **see the quantity in a different unit**.

Remember, the operations are performed from left to right. So if you have 3 units, and you choose to multiply then divide, the app will first multiply the first two units, then divide by the third unit.

---

**Example:**

If you want to convert mass flow rate from `120` `kg/hour` to `pound/second`, here's how to do it:

- Set the number of units to `2`.
- For the first unit, select `kilogram` and enter the quantity of `120`.
- Set the operation with the next unit to `divide`.
- For the second unit, select `hour` or `hr` and enter `1` as the quantity.
- In the possible combinations, select `pound/sec`.
- The result would be displayed down as `0.07348742072829254 pound/second`
""")
st.sidebar.markdown('---')

# User selects the number of units
st.markdown("## Number of Units Selection")
num_units = st.slider("Select the number of units:", 1, 3, key='num_units')
st.markdown('---')

if num_units >= 1:
    st.markdown("### Unit 1")
    col1, col2 = st.columns(2)
    with col1:
        selected_unit_1 = st.selectbox("Select the first unit type:", all_units, key='unit_1', index=all_units.index('second'))
    with col2:
        quantity_value_1 = st.number_input("Enter the quantity for the first unit", min_value=0.0, value=1.0, key='unit_1_value')
    st.markdown('---')

if num_units >= 2:
    st.markdown("### Unit 2")
    col3, col4, col5 = st.columns([2, 1, 2])
    with col3:
        selected_unit_2 = st.selectbox("Select the second unit type:", all_units, key='unit_2', index=all_units.index('second'))
    with col4:
        operation_12 = st.radio('Operation:', ('multiply', 'divide'), key='12')
    with col5:
        quantity_value_2 = st.number_input("Enter the quantity for the second unit", min_value=0.0, value=1.0, key='unit_2_value')
    st.markdown('---')

if num_units == 3:
    st.markdown("### Unit 3")
    col6, col7, col8 = st.columns([2, 1, 2])
    with col6:
        selected_unit_3 = st.selectbox("Select the third unit type:", all_units, key='unit_3', index=all_units.index('second'))
    with col7:
        operation_23 = st.radio('Operation:', ('multiply', 'divide'), key='23')
    with col8:
        quantity_value_3 = st.number_input("Enter the quantity for the third unit", min_value=0.0, value=1.0, key='unit_3_value')
    st.markdown('---')

# Perform calculation and display dimensionality
try:
    # Create quantities with both value and unit
    quantity_1 = ureg.Quantity(quantity_value_1, selected_unit_1) if selected_unit_1 is not None else None
    quantity_2 = ureg.Quantity(quantity_value_2, selected_unit_2) if selected_unit_2 is not None else None
    quantity_3 = ureg.Quantity(quantity_value_3, selected_unit_3) if selected_unit_3 is not None else None

    if quantity_1 is not None and quantity_2 is not None and quantity_3 is not None:
        if operation_12 == 'multiply' and operation_23 == 'multiply':
            final_quantity = quantity_1 * quantity_2 * quantity_3
        elif operation_12 == 'divide' and operation_23 == 'divide':
            final_quantity = quantity_1 / quantity_2 / quantity_3
        elif operation_12 == 'divide' and operation_23 == 'multiply':
            final_quantity = quantity_1 / quantity_2 * quantity_3
        elif operation_12 == 'multiply' and operation_23 == 'divide':
            final_quantity = quantity_1 * quantity_2 / quantity_3
    elif quantity_1 is not None and quantity_2 is not None:
        if operation_12 == 'multiply':
            final_quantity = quantity_1 * quantity_2
        elif operation_12 == 'divide':
            final_quantity = quantity_1 / quantity_2
    elif quantity_1 is not None:
        final_quantity = quantity_1

except Exception as e:
    st.write("An error occurred in defining final_quantity:")
    st.write(str(e))

# preparing all possible combinations
try:
    if quantity_1 is not None and quantity_2 is not None and quantity_3 is not None:
        # Prepare a list of compatible units for the first unit
        compatible_units_1 = []
        for unit in all_units:
            try:
                if ureg.parse_expression(selected_unit_1).dimensionality == ureg.parse_expression(unit).dimensionality:
                    compatible_units_1.append(unit)
            except pint.errors.UndefinedUnitError:
                pass
        # Prepare a list of compatible units for the second unit
        compatible_units_2 = []
        for unit in all_units:
            try:
                if ureg.parse_expression(selected_unit_2).dimensionality == ureg.parse_expression(unit).dimensionality:
                    compatible_units_2.append(unit)
            except pint.errors.UndefinedUnitError:
                pass
        # Prepare a list of compatible units for the third unit
        compatible_units_3 = []
        for unit in all_units:
            try:
                if ureg.parse_expression(selected_unit_3).dimensionality == ureg.parse_expression(unit).dimensionality:
                    compatible_units_3.append(unit)
            except pint.errors.UndefinedUnitError:
                pass
        # Prepare a list of possible combinations for the final quantity
        if operation_12 == 'divide' and operation_23 == 'divide':
            possible_combinations = [f"{unit1}/{unit2}/{unit3}" for unit1 in compatible_units_1 for unit2 in compatible_units_2 for unit3 in compatible_units_3]
        if operation_12 == 'multiply' and operation_23 == 'multiply':
            possible_combinations = [f"{unit1}*{unit2}*{unit3}" for unit1 in compatible_units_1 for unit2 in compatible_units_2 for unit3 in compatible_units_3]
        if operation_12 == 'multiply' and operation_23 == 'divide':
            possible_combinations = [f"{unit1}*{unit2}/{unit3}" for unit1 in compatible_units_1 for unit2 in compatible_units_2 for unit3 in compatible_units_3]
        if operation_12 == 'divide' and operation_23 == 'multiply':
            possible_combinations = [f"{unit1}/{unit2}*{unit3}" for unit1 in compatible_units_1 for unit2 in compatible_units_2 for unit3 in compatible_units_3]
    elif quantity_1 is not None and quantity_2 is not None:
        # Prepare a list of compatible units for the first unit
        compatible_units_1 = []
        for unit in all_units:
            try:
                if ureg.parse_expression(selected_unit_1).dimensionality == ureg.parse_expression(unit).dimensionality:
                    compatible_units_1.append(unit)
            except pint.errors.UndefinedUnitError:
                pass
        # Prepare a list of compatible units for the second unit
        compatible_units_2 = []
        for unit in all_units:
            try:
                if ureg.parse_expression(selected_unit_2).dimensionality == ureg.parse_expression(unit).dimensionality:
                    compatible_units_2.append(unit)
            except pint.errors.UndefinedUnitError:
                pass
        # Prepare a list of possible combinations for the final quantity
        if operation_12 == 'divide':
            possible_combinations = [f"{unit1}/{unit2}" for unit1 in compatible_units_1 for unit2 in compatible_units_2]
        elif operation_12 == 'multiply':
            possible_combinations = [f"{unit1}*{unit2}" for unit1 in compatible_units_1 for unit2 in compatible_units_2]
    elif quantity_1 is not None:
        compatible_units_1 = []
        for unit in all_units:
            try:
                if ureg.parse_expression(selected_unit_1).dimensionality == ureg.parse_expression(unit).dimensionality:
                    compatible_units_1.append(unit)
            except pint.errors.UndefinedUnitError:
                pass
        possible_combinations = [f"{unit1}" for unit1 in compatible_units_1]
        possible_combinations = list(set(possible_combinations))
    st.markdown('---')
    st.markdown("## Select a Compatible Unit to Convert To ")
    selected_combination = st.selectbox("Select a combination:", possible_combinations, key='possible_combination')
    st.write(f'There are {len(possible_combinations)} selection(s) available')

    # Display initial and converted result below the columns
    if 'final_quantity' in locals() and 'selected_combination' in locals():
        converted_quantity = final_quantity.to(selected_combination)
        result_df = pd.DataFrame({
            "Description": ["Initial Quantity", "Converted Quantity"],
            "Value": [final_quantity.magnitude, converted_quantity.magnitude],
            "Unit of Measurement": [str(final_quantity.units), str(converted_quantity.units)]
        })
        st.markdown('---')
        st.write("### Conversion Result")
        st.dataframe(result_df)
except Exception as L:
    st.write("An error occurred in finding alternative combinations:")
    st.write(str(L))
