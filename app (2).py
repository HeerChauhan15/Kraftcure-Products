import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Insurance Premium Calculator",
    page_icon="💰",
    layout="centered"
)

GST_RATE = 18.0

# ---------------------------------------------------------
# PRODUCT DATA
# All rates are FLAT, PRE-GST premium per member (₹).
# GST (18%) is added on top at calculation time.
# ---------------------------------------------------------
# Structure:
#   "type": "insurer"  -> user picks Low / Medium / High (based on insurer rate)
#   "type": "tier"     -> user picks a Sum Insured tier (single insurer)
#   "type": "fixed"    -> only one insurer/rate, nothing to pick

PRODUCTS = {
    "PA": {
        "type": "insurer",
        "rates": {
            "Care": 9.32,
            "Aditya Birla": 21.186440677966104,
            "Cigna Manipal": 24.00,
        },
    },
    "PA Hospicash": {
        "type": "fixed",
        "rates": {
            "Magma": 424.00,
        },
    },
    "PA + Cancer Specific": {
        "type": "fixed",
        "rates": {
            "Cigna Manipal": 180.00,
        },
    },
    "Cancer Specific": {
        "type": "fixed",
        "rates": {
            "Cigna Manipal": 156.00,
        },
    },
    "PA + CI": {
        "type": "insurer",
        "rates": {
            "Magma": 270.00,
            "Cigna Manipal": 368.00,
        },
    },
    "CI": {
        "type": "fixed",
        "rates": {
            "Cigna Manipal": 344.00,
        },
    },
    "Health": {
        "type": "tier",
        "insurer": "Aditya Birla",
        "rates": {
            "1 Lakh": 1879.00,
            "3 Lakh": 2287.288135593220,
            "5 Lakh": 3369.00,
        },
    },
}


# ---------------------------------------------------------
# HELPER FUNCTION - INDIAN CURRENCY FORMAT
# ---------------------------------------------------------

def format_currency(amount):
    """
    Format number using Indian numbering system.
    Example:
    1000000 -> ₹10,00,000
    """
    amount = round(amount, 2)

    if amount == int(amount):
        amount = int(amount)

    number = str(amount)

    if "." in number:
        integer_part, decimal_part = number.split(".")
    else:
        integer_part = number
        decimal_part = ""

    negative = integer_part.startswith("-")
    if negative:
        integer_part = integer_part[1:]

    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]

        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        if remaining:
            groups.insert(0, remaining)

        formatted = ",".join(groups) + "," + last_three

    if negative:
        formatted = "-" + formatted

    if decimal_part:
        formatted += "." + decimal_part

    return f"₹{formatted}"


def get_low_medium_high(rates_dict):
    """
    Given a dict of {insurer: rate}, return an ordered list of
    (label, insurer, rate) tuples.
    - 1 insurer  -> [("Standard", insurer, rate)]
    - 2 insurers -> [("Low", ...), ("High", ...)]
    - 3+ insurers -> [("Low", ...), ("Medium", ...), ("High", ...)]
      (Medium = the middle-ranked insurer by rate; if more than 3
      insurers exist, Low/High are min/max and Medium is the median)
    """
    sorted_items = sorted(rates_dict.items(), key=lambda x: x[1])

    if len(sorted_items) == 1:
        insurer, rate = sorted_items[0]
        return [("Standard", insurer, rate)]

    if len(sorted_items) == 2:
        (low_ins, low_rate), (high_ins, high_rate) = sorted_items
        return [("Low", low_ins, low_rate), ("High", high_ins, high_rate)]

    low_ins, low_rate = sorted_items[0]
    high_ins, high_rate = sorted_items[-1]
    mid_index = len(sorted_items) // 2
    med_ins, med_rate = sorted_items[mid_index]
    return [
        ("Low", low_ins, low_rate),
        ("Medium", med_ins, med_rate),
        ("High", high_ins, high_rate),
    ]


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("💰 Insurance Premium Calculator")
st.caption("Select one or more products, pick an option for each, and get a combined premium.")
st.divider()

# ---------------------------------------------------------
# PRODUCT SELECTION
# ---------------------------------------------------------

st.subheader("1. Select Products")

selected_products = st.multiselect(
    "Which product(s) do you want to quote?",
    list(PRODUCTS.keys()),
)

# ---------------------------------------------------------
# PER-PRODUCT OPTIONS
# ---------------------------------------------------------

product_choices = {}  # product_name -> (label, insurer, rate)

if selected_products:
    st.divider()
    st.subheader("2. Choose Option per Product")

    for product_name in selected_products:
        product = PRODUCTS[product_name]
        st.markdown(f"**{product_name}**")

        if product["type"] == "insurer":
            options = get_low_medium_high(product["rates"])
            option_labels = [
                f"{label} — {insurer}"
                for label, insurer, rate in options
            ]
            choice = st.radio(
                f"Choose option for {product_name}",
                option_labels,
                key=f"radio_{product_name}",
                label_visibility="collapsed",
            )
            chosen = options[option_labels.index(choice)]
            product_choices[product_name] = chosen

        elif product["type"] == "tier":
            tier_labels = list(product["rates"].keys())
            tier = st.selectbox(
                f"Sum Insured tier for {product_name}",
                tier_labels,
                key=f"tier_{product_name}",
                label_visibility="collapsed",
            )
            rate = product["rates"][tier]
            product_choices[product_name] = (tier, product["insurer"], rate)

        else:  # fixed - single insurer, nothing to choose
            insurer, rate = list(product["rates"].items())[0]
            st.caption(f"{insurer} (only option available)")
            product_choices[product_name] = ("Standard", insurer, rate)

        st.write("")

# ---------------------------------------------------------
# OPTIONAL LOADING
# ---------------------------------------------------------

loading = 0.0
if selected_products:
    st.divider()
    st.subheader("3. Loading (optional)")
    loading = st.number_input(
        "Loading on combined premium (%)",
        min_value=0.0,
        value=0.0,
        step=0.5,
    )

# ---------------------------------------------------------
# CALCULATE
# ---------------------------------------------------------

if selected_products:
    calculate = st.button("Calculate Premium", type="primary", use_container_width=True)
else:
    calculate = False
    st.info("Select at least one product above to calculate a premium.")

if calculate:
    st.divider()
    st.subheader("Premium Quotation")

    total_base_premium = 0.0

    for product_name in selected_products:
        label, insurer, rate = product_choices[product_name]
        total_base_premium += rate

        col1, col2 = st.columns([3, 2])
        with col1:
            st.write(f"**{product_name}** — {insurer} ({label})")
        with col2:
            st.write(format_currency(rate))

    st.divider()

    loading_amount = total_base_premium * loading / 100
    premium_before_gst = total_base_premium + loading_amount
    gst_amount = premium_before_gst * GST_RATE / 100
    premium_with_gst = premium_before_gst + gst_amount

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Base Premium (sum of products)", format_currency(total_base_premium))
    with col2:
        st.metric("Loading Amount", format_currency(loading_amount))

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Premium Before GST", format_currency(premium_before_gst))
    with col2:
        st.metric("GST @ 18%", format_currency(gst_amount))
    with col3:
        st.metric("Premium Including GST", format_currency(premium_with_gst))
