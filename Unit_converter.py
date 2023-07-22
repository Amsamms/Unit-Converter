import streamlit as st
from pint import UnitRegistry
import pint.errors

# Create a unit registry
ureg = UnitRegistry()

# creat cubic meter, use the below to define any unit to be in the registry
ureg.define('cubic_meter = 1e3 * liter = m^3 = cu_m = cu_meter')

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
        <h1 style="text-align: center;">🌐 Universal Unit Converter 🌐</h1>
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
#num_units = st.selectbox("Select the number of units:", [1, 2, 3], key='num_units')
st.markdown("## number of units selection")
num_units = st.slider("Select the number of units:", 1, 3, key='num_units')
st.markdown('---')

if num_units >= 1:
    st.markdown("## Unit 1")
    # First drop-down menu for unit type
    selected_unit_1 = st.selectbox("Select the first unit type:", all_units, key='unit_1', index=all_units.index('second'))
    # Input field for the quantity of the first unit
    quantity_value_1 = st.number_input("Enter the quantity for the first unit", min_value=0.0, value=1.0, key='unit_1_value')
    st.markdown('---')

if num_units >= 2:
    st.markdown("## Unit 2")
    # Operation radio button
    operation_12 = st.radio('Operation:', ('multiply', 'divide'), key='12')
    # Second drop-down menu for unit type
    selected_unit_2 = st.selectbox("Select the second unit type:", all_units,key='unit_2', index=all_units.index('second'))
    # Input field for the quantity of the second unit
    quantity_value_2 = st.number_input("Enter the quantity for the second unit", min_value=0.0, value=1.0, key='unit_2_value')
    st.markdown('---')

if num_units == 3:
    st.markdown("## Unit 3")
    # Operation radio button
    operation_23 = st.radio('Operation:', ('multiply', 'divide'),key='23')
    # Third drop-down menu for unit type
    selected_unit_3 = st.selectbox("Select the third unit type:", all_units, key='unit_3', index=all_units.index('second'))
    # Input field for the quantity of the third unit
    quantity_value_3 = st.number_input("Enter the quantity for the third unit", min_value=0.0, value=1.0, key='unit_3_value')
    st.markdown('---')
# Perform calculation and display dimensionality
try:
    # Create quantities with both value and unit
    quantity_1 = ureg.Quantity(quantity_value_1, selected_unit_1) if selected_unit_1 is not None else None
    quantity_2 = ureg.Quantity(quantity_value_2, selected_unit_2) if selected_unit_2 is not None else None
    quantity_3 = ureg.Quantity(quantity_value_3, selected_unit_3) if selected_unit_3 is not None else None

    if quantity_1 is not None and quantity_2 is not None and quantity_3 is not None:
        if operation_12 == 'multiply' and operation_23== 'multiply' :
            final_quantity = quantity_1 * quantity_2 * quantity_3
        elif operation_12 == 'divide' and operation_23 == 'divide' :
            final_quantity = quantity_1 / quantity_2 / quantity_3
        elif operation_12 == 'divide' and operation_23 == 'multiply' :
            final_quantity = quantity_1 / quantity_2 * quantity_3
        elif operation_12 == 'multiply' and operation_23 == 'divide' :
            final_quantity = quantity_1 * quantity_2 / quantity_3
    elif quantity_1 is not None and quantity_2 is not None:
        if operation_12 == 'multiply':
          final_quantity = quantity_1 * quantity_2
        elif operation_12 == 'divide':
          final_quantity = quantity_1 / quantity_2
    elif quantity_1 is not None :
        final_quantity = quantity_1
        
        
    #st.write(final_quantity)
    #st.write(final_quantity.magnitude)
    #st.write(final_quantity.units)
    #st.write(final_quantity.dimensionality)
               
except Exception as e:
    st.write("An error occurred in difining final_quantity:")
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
    st.markdown("## select a combatible unit to convert to ")
    selected_combination = st.selectbox("Select a combination:", possible_combinations, key='possible_combination')
    st.write(f'there are {len(possible_combinations)} selection available')
except Exception as L:
    st.write("An error occurred in finding alternative combinations:")
    st.write(str(L))
try:  
    # Convert the final quantity to the selected combination
    converted_quantity = final_quantity.to(selected_combination)
    st.markdown('---')  
    #st.write(f"the initial quantity of {final_quantity.magnitude} in {final_quantity.units} equal to {converted_quantity.magnitude} in {converted_quantity.units}.")
    # Write output
    st.markdown(
        f"The initial quantity of <span style='color:blue;font-weight:bold'>{final_quantity.magnitude}</span> in "
        f"<span style='color:blue;font-weight:bold'>{final_quantity.units}</span><br/>"
        f"is equal to:<br/>"
        f"<span style='color:red;font-weight:bold'>{converted_quantity.magnitude}</span> in "
        f"<span style='color:red;font-weight:bold'>{converted_quantity.units}</span>.",
        unsafe_allow_html=True,
    )
except Exception as o:
    st.write("An error occurred in conversion:")
    st.write(str(o))
    

