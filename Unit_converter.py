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

# Configure page
st.set_page_config(
    page_title="Universal Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI Design - Complete Makeover
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Modern clean background */
    .stApp {
        background: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main .block-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #e2e8f0;
        max-width: 1000px;
        margin-top: 2rem;
    }

    /* Modern header */
    .hero-section {
        text-align: center;
        padding: 3rem 0 2rem 0;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 16px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
    }

    .hero-content {
        position: relative;
        z-index: 1;
    }

    .hero-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.025em;
    }

    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0;
    }

    /* Card system */
    .conversion-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .conversion-card:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border-color: #c7d2fe;
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .card-subtitle {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0 0 1rem 0;
    }

    /* Mode selector */
    .mode-selector {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .mode-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
        position: relative;
    }

    .mode-card:hover {
        border-color: #6366f1;
        background: #f8faff;
    }

    .mode-card.active {
        border-color: #6366f1;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.25);
    }

    .mode-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }

    .mode-title {
        font-weight: 600;
        font-size: 1.1rem;
        margin: 0 0 0.5rem 0;
    }

    .mode-desc {
        font-size: 0.9rem;
        opacity: 0.8;
        margin: 0;
    }

    /* Input styling */
    .input-group {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 1rem;
        align-items: end;
    }

    .input-label {
        font-weight: 500;
        color: #374151;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }

    /* Operation flow */
    .operation-flow {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
        position: relative;
    }

    .flow-line {
        height: 2px;
        background: linear-gradient(90deg, #e2e8f0 0%, #6366f1 50%, #e2e8f0 100%);
        flex: 1;
    }

    .operation-pill {
        background: white;
        border: 2px solid #6366f1;
        border-radius: 50px;
        padding: 0.75rem 1.5rem;
        margin: 0 1rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
        min-width: 160px;
        text-align: center;
    }

    .operation-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #6366f1;
        text-transform: uppercase;
        letter-spacing: 0.025em;
        margin: 0 0 0.25rem 0;
    }

    /* Results section */
    .results-section {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid #c7d2fe;
    }

    .results-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 1.5rem 0;
    }

    .result-cards {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .result-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e2e8f0;
    }

    .result-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.025em;
        margin: 0 0 0.5rem 0;
    }

    .result-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 0.25rem 0;
    }

    .result-unit {
        font-size: 0.9rem;
        color: #6366f1;
        font-weight: 500;
        margin: 0;
    }

    /* Conversion factor */
    .conversion-factor {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid #c7d2fe;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        font-size: 0.9rem;
        color: #374151;
    }

    /* Modern form controls */
    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        font-family: 'Inter', sans-serif;
    }

    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        font-family: 'Inter', sans-serif;
    }

    .stRadio > div {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .stRadio > div > label {
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        margin: 0;
        flex: 1;
        text-align: center;
    }

    .stRadio > div > label:hover {
        border-color: #6366f1;
        background: #f8faff;
    }

    /* Mode selection radio buttons - make them minimal */
    .stRadio[data-testid="stRadio"] > div {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }

    .stRadio[data-testid="stRadio"] > div > label {
        font-size: 0.9rem;
        padding: 0.5rem;
        margin: 0;
        border: none;
        background: transparent;
        width: 100%;
    }

    .stRadio[data-testid="stRadio"] > div > label:hover {
        background: #f1f5f9;
        border-radius: 6px;
    }

    /* Hide default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stDeployButton {display: none;}

    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }

        .mode-selector {
            grid-template-columns: 1fr;
        }

        .input-group {
            grid-template-columns: 1fr;
        }

        .result-cards {
            grid-template-columns: 1fr;
        }

        .operation-flow {
            flex-direction: column;
            gap: 1rem;
        }

        .flow-line {
            display: none;
        }
    }
</style>
""", unsafe_allow_html=True)

# Modern hero section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">Universal Unit Converter</h1>
        <p class="hero-subtitle">Convert any measurement with precision and ease</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("📋 Step-by-Step Guide")

st.sidebar.markdown("""
### 🎯 **How to Use This Converter**

**Step 1: Choose Complexity**
Select how many units you need (1-3 units)

**Step 2: Configure Units**
- Pick your unit type from the dropdown
- Enter the quantity value
- Choose operations (×, ÷) between units

**Step 3: Select Output Format**
Pick your desired output unit combination

**Step 4: View Results**
See your conversion with precision!

---

### 💡 **Pro Tips**

✨ **Single Unit**: Perfect for basic conversions like meters to feet

🔗 **Two Units**: Great for rates like speed (distance/time) or density (mass/volume)

⚡ **Three Units**: Handle complex units like acceleration (distance/time²)

---

### 🚀 **Quick Example**

**Converting 120 kg/hour to pound/second:**

1. Set units to **2**
2. Unit 1: `kilogram` with value `120`
3. Operation: **divide** (÷)
4. Unit 2: `hour` with value `1`
5. Select output: `pound/second`
6. Result: `0.0735 pound/second`

---

### ⚠️ **Important Notes**

- Operations are performed **left to right**
- All calculations maintain **dimensional consistency**
- Choose compatible units for accurate results
""")

# Mode selection with modern cards
st.markdown('<h2 style="text-align: center; margin: 2rem 0 1rem 0; color: #1e293b; font-weight: 700;">Choose Conversion Type</h2>', unsafe_allow_html=True)

# Use radio buttons styled as cards to avoid the button reset issue
mode_options = [
    "🔢 Single Unit - Convert between different units of the same measurement",
    "⚡ Compound Units - Handle rates, ratios, and combined measurements",
    "🚀 Complex Units - Advanced conversions with multiple operations"
]

selected_mode = st.radio("", mode_options, key="conversion_mode")

# Map selection to number of units
if "Single Unit" in selected_mode:
    num_units = 1
elif "Compound Units" in selected_mode:
    num_units = 2
else:  # Complex Units
    num_units = 3

# Display mode cards with active state (visual feedback only)
st.markdown(f"""
<div class="mode-selector">
    <div class="mode-card {'active' if num_units == 1 else ''}">
        <span class="mode-icon">🔢</span>
        <h3 class="mode-title">Single Unit</h3>
        <p class="mode-desc">Convert between different units of the same measurement</p>
    </div>
    <div class="mode-card {'active' if num_units == 2 else ''}">
        <span class="mode-icon">⚡</span>
        <h3 class="mode-title">Compound Units</h3>
        <p class="mode-desc">Handle rates, ratios, and combined measurements</p>
    </div>
    <div class="mode-card {'active' if num_units == 3 else ''}">
        <span class="mode-icon">🚀</span>
        <h3 class="mode-title">Complex Units</h3>
        <p class="mode-desc">Advanced conversions with multiple operations</p>
    </div>
</div>
""", unsafe_allow_html=True)

if num_units >= 1:
    st.markdown("""
    <div class="conversion-card">
        <h3 class="card-title">📊 First Unit</h3>
        <p class="card-subtitle">Select your starting measurement unit and enter its value</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_unit_1 = st.selectbox("Unit Type", all_units, key='unit_1', index=all_units.index('second'))
    with col2:
        quantity_value_1 = st.number_input("Value", min_value=0.0, value=1.0, key='unit_1_value')

if num_units >= 2:
    st.markdown("""
    <div class="conversion-card">
        <h3 class="card-title">⚡ Second Unit</h3>
        <p class="card-subtitle">Add a second measurement for compound unit conversion</p>
    </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns([2, 1])
    with col3:
        selected_unit_2 = st.selectbox("Unit Type", all_units, key='unit_2', index=all_units.index('second'))
    with col4:
        quantity_value_2 = st.number_input("Value", min_value=0.0, value=1.0, key='unit_2_value')

    # Modern operation selection
    st.markdown("""
    <div class="operation-flow">
        <div class="flow-line"></div>
        <div class="operation-pill">
            <div class="operation-title">Operation</div>
        </div>
        <div class="flow-line"></div>
    </div>
    """, unsafe_allow_html=True)

    operation_12 = st.radio("Choose how to combine the units:", ('✖️ Multiply', '➗ Divide'), key='12')

if num_units == 3:
    st.markdown("""
    <div class="conversion-card">
        <h3 class="card-title">🚀 Third Unit</h3>
        <p class="card-subtitle">Add a third measurement for advanced unit conversions</p>
    </div>
    """, unsafe_allow_html=True)

    col5, col6 = st.columns([2, 1])
    with col5:
        selected_unit_3 = st.selectbox("Unit Type", all_units, key='unit_3', index=all_units.index('second'))
    with col6:
        quantity_value_3 = st.number_input("Value", min_value=0.0, value=1.0, key='unit_3_value')

    # Second operation selection
    st.markdown("""
    <div class="operation-flow">
        <div class="flow-line"></div>
        <div class="operation-pill">
            <div class="operation-title">Second Operation</div>
        </div>
        <div class="flow-line"></div>
    </div>
    """, unsafe_allow_html=True)

    operation_23 = st.radio("Choose the second operation:", ('✖️ Multiply', '➗ Divide'), key='23')

# Perform calculation and display dimensionality
try:
    # Create quantities with both value and unit
    quantity_1 = ureg.Quantity(quantity_value_1, selected_unit_1) if selected_unit_1 is not None else None
    quantity_2 = ureg.Quantity(quantity_value_2, selected_unit_2) if selected_unit_2 is not None else None
    quantity_3 = ureg.Quantity(quantity_value_3, selected_unit_3) if selected_unit_3 is not None else None

    # Convert operation text to simple operation names for logic
    op_12_simple = 'multiply' if operation_12 and 'Multiply' in operation_12 else 'divide'
    op_23_simple = 'multiply' if operation_23 and 'Multiply' in operation_23 else 'divide'

    if quantity_1 is not None and quantity_2 is not None and quantity_3 is not None:
        if op_12_simple == 'multiply' and op_23_simple == 'multiply':
            final_quantity = quantity_1 * quantity_2 * quantity_3
        elif op_12_simple == 'divide' and op_23_simple == 'divide':
            final_quantity = quantity_1 / quantity_2 / quantity_3
        elif op_12_simple == 'divide' and op_23_simple == 'multiply':
            final_quantity = quantity_1 / quantity_2 * quantity_3
        elif op_12_simple == 'multiply' and op_23_simple == 'divide':
            final_quantity = quantity_1 * quantity_2 / quantity_3
    elif quantity_1 is not None and quantity_2 is not None:
        if op_12_simple == 'multiply':
            final_quantity = quantity_1 * quantity_2
        elif op_12_simple == 'divide':
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
        if op_12_simple == 'divide' and op_23_simple == 'divide':
            possible_combinations = [f"{unit1}/{unit2}/{unit3}" for unit1 in compatible_units_1 for unit2 in compatible_units_2 for unit3 in compatible_units_3]
        if op_12_simple == 'multiply' and op_23_simple == 'multiply':
            possible_combinations = [f"{unit1}*{unit2}*{unit3}" for unit1 in compatible_units_1 for unit2 in compatible_units_2 for unit3 in compatible_units_3]
        if op_12_simple == 'multiply' and op_23_simple == 'divide':
            possible_combinations = [f"{unit1}*{unit2}/{unit3}" for unit1 in compatible_units_1 for unit2 in compatible_units_2 for unit3 in compatible_units_3]
        if op_12_simple == 'divide' and op_23_simple == 'multiply':
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
        if op_12_simple == 'divide':
            possible_combinations = [f"{unit1}/{unit2}" for unit1 in compatible_units_1 for unit2 in compatible_units_2]
        elif op_12_simple == 'multiply':
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

    st.markdown("""
    <div class="conversion-card">
        <h3 class="card-title">🎯 Choose Output Format</h3>
        <p class="card-subtitle">Select your desired output unit from dimensionally compatible options</p>
    </div>
    """, unsafe_allow_html=True)

    selected_combination = st.selectbox("Output Unit", possible_combinations, key='possible_combination')
    st.info(f"Found {len(possible_combinations)} compatible unit format(s)")

    # Modern results display
    if 'final_quantity' in locals() and 'selected_combination' in locals():
        converted_quantity = final_quantity.to(selected_combination)

        st.markdown("""
        <div class="results-section">
            <h2 class="results-title">✨ Conversion Results</h2>
            <div class="result-cards">
                <div class="result-card">
                    <div class="result-label">Input</div>
                    <div class="result-value">{:.6g}</div>
                    <div class="result-unit">{}</div>
                </div>
                <div class="result-card">
                    <div class="result-label">Output</div>
                    <div class="result-value">{:.6g}</div>
                    <div class="result-unit">{}</div>
                </div>
            </div>
        </div>
        """.format(
            final_quantity.magnitude, str(final_quantity.units),
            converted_quantity.magnitude, str(converted_quantity.units)
        ), unsafe_allow_html=True)

        # Original DataFrame for data integrity
        result_df = pd.DataFrame({
            "Description": ["Initial Quantity", "Converted Quantity"],
            "Value": [final_quantity.magnitude, converted_quantity.magnitude],
            "Unit of Measurement": [str(final_quantity.units), str(converted_quantity.units)]
        })

        with st.expander("📊 Detailed Data Table"):
            st.dataframe(result_df)

        # Conversion factor
        if final_quantity.magnitude != 0:
            conversion_factor = converted_quantity.magnitude / final_quantity.magnitude
            st.markdown(f"""
            <div class="conversion-factor">
                <strong>Conversion Factor:</strong> 1 {str(final_quantity.units)} = {conversion_factor:.6g} {str(converted_quantity.units)}
            </div>
            """, unsafe_allow_html=True)
except Exception as L:
    st.write("An error occurred in finding alternative combinations:")
    st.write(str(L))
