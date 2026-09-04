import streamlit as st
from logo_b64 import KRAFTCURE_LOGO_B64, POLICYGRACE_LOGO_B64

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Kraftcure Products",
    page_icon="💰",
    layout="centered"
)

# ---------------------------------------------------------
# LIGHT STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #eef2f7 0%, #f7f4ee 100%);
    }
    .kc-header-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 60px 18px 60px;
    }
    .kc-header-bar img { height: 52px; object-fit: contain; }
    .kc-title-block { text-align: center; flex: 1; padding: 0 40px; }
    .kc-title-block h1 {
        margin: 0;
        font-size: 1.9rem;
        background: linear-gradient(90deg, #10b981, #f97316);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kc-title-block .kc-tagline {
        margin: 2px 0 0 0;
        color: #374151;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .kc-title-block .kc-subtext { margin: 4px 0 0 0; color: #6b7280; font-size: 0.9rem; }
    .kc-section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px 20px 8px 20px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetricValue"] { font-size: 1.4rem; }
    </style>
    """,
    unsafe_allow_html=True,
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
            "Care": 12.00,
            "Aditya Birla": 21.186440677966104,
            "Cigna Manipal": 24.00,
        },
    },
    "PA Hospicash": {
        "type": "insurer",
        "rates": {
            "Magma": 471.00,
            "Tata": 250.00,
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
            "Magma": 300.00,
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
            "3 Lakh": 2699,
            "5 Lakh": 3369.00,
        },
    },
    "GTL": {
        "type": "insurer",
        "rates": {
            "Aviva": 800.00,
            "IPRU": 800.00,
        },
    },
}


# ---------------------------------------------------------
# HELPER FUNCTION - INDIAN CURRENCY FORMAT
# ---------------------------------------------------------

import math

def round_half_up(amount):
    """
    Round to the nearest whole number, rounding .5 and above UP
    (not Python's default banker's rounding, which rounds .5 to
    the nearest even number).
    """
    if amount >= 0:
        return math.floor(amount + 0.5)
    return -math.floor(-amount + 0.5)


def format_currency(amount):
    """
    Format number using Indian numbering system, rounded to the
    nearest whole rupee (0.5 and above rounds up).
    Example:
    1000000 -> ₹10,00,000
    """
    amount = round_half_up(amount)

    number = str(amount)
    integer_part = number

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

    return f"₹{formatted}"


def get_insurer_options(rates_dict):
    """
    Given a dict of {insurer: rate}, return an ordered list of
    (insurer, rate) tuples sorted by rate ascending — one entry
    per insurer available for that product, so the user can pick
    whichever insurer they want directly.
    """
    return sorted(rates_dict.items(), key=lambda x: x[1])


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    f"""
    <div class="kc-header-bar">
        <img src="data:image/png;base64,{KRAFTCURE_LOGO_B64}" alt="Kraftcure logo">
        <div class="kc-title-block">
            <h1>Kraftcure Products</h1>
            <p class="kc-tagline">You Choose. We Deliver.</p>
        </div>
        <img src="data:image/png;base64,{POLICYGRACE_LOGO_B64}" alt="Policygrace logo">
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# ---------------------------------------------------------
# PRODUCT SELECTION
# ---------------------------------------------------------

st.markdown('<div class="kc-section-card">', unsafe_allow_html=True)
st.subheader("1. Select Products")

selected_products = st.multiselect(
    "Which product(s) do you want to quote?",
    list(PRODUCTS.keys()),
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PER-PRODUCT OPTIONS
# ---------------------------------------------------------

product_choices = {}  # product_name -> (label, insurer, rate)

if selected_products:
    st.divider()
    st.markdown('<div class="kc-section-card">', unsafe_allow_html=True)
    st.subheader("2. Choose Option per Product")

    for product_name in selected_products:
        product = PRODUCTS[product_name]
        col_label, col_input = st.columns([1, 2])

        if product["type"] == "insurer":
            options = get_insurer_options(product["rates"])
            insurer_names = [insurer for insurer, rate in options]
            with col_label:
                st.markdown(f"**{product_name}**")
            with col_input:
                chosen_insurer = st.selectbox(
                    f"Insurer for {product_name}",
                    insurer_names,
                    key=f"insurer_{product_name}",
                    label_visibility="collapsed",
                )
            chosen_rate = product["rates"][chosen_insurer]
            product_choices[product_name] = ("Standard", chosen_insurer, chosen_rate)

        elif product["type"] == "tier":
            tier_labels = list(product["rates"].keys())
            with col_label:
                st.markdown(f"**{product_name}**")
            with col_input:
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
            with col_label:
                st.markdown(f"**{product_name}**")
            with col_input:
                st.caption(f"{insurer} (only option available)")
            product_choices[product_name] = ("Standard", insurer, rate)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# OPTIONAL LOADING
# ---------------------------------------------------------

loading = 0.0
if selected_products:
    st.divider()
    st.markdown('<div class="kc-section-card">', unsafe_allow_html=True)
    st.subheader("3. Loading / Partner Commission (optional)")
    loading = st.number_input(
        "Loading (partner commission) on combined premium (%)",
        min_value=0.0,
        max_value=99.0,
        value=0.0,
        step=0.5,
        help="Premium is grossed up so this % of the final premium (before GST) equals the partner payout.",
    )
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="kc-section-card">', unsafe_allow_html=True)
    st.subheader("Premium Quotation")

    total_base_premium = 0.0

    for product_name in selected_products:
        label, insurer, rate = product_choices[product_name]
        total_base_premium += rate

        col1, col2 = st.columns([3, 2])
        with col1:
            if label == "Standard":
                st.write(f"**{product_name}** — {insurer}")
            else:
                st.write(f"**{product_name}** — {insurer} ({label})")
        with col2:
            st.write(format_currency(rate))

    st.divider()

    # Loading is treated as embedded partner commission: the base
    # premium is grossed up so that `loading`% of the FINAL premium
    # (before GST) equals the loading/partner-payout amount.
    #   premium_before_gst = base / (1 - loading%)
    #   loading_amount      = premium_before_gst - base
    #                        = loading% of premium_before_gst (same value)
    premium_before_gst = total_base_premium / (1 - loading / 100)
    loading_amount = premium_before_gst - total_base_premium
    partner_payout = loading_amount  # identical value, shown for the partner's clarity

    gst_amount = premium_before_gst * GST_RATE / 100
    premium_with_gst = premium_before_gst + gst_amount

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Base Premium (sum of products)", format_currency(total_base_premium))
    with col2:
        st.metric("Loading Amount", format_currency(loading_amount))

    st.metric("Partner Payout", format_currency(partner_payout))

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Premium Before GST", format_currency(premium_before_gst))
    with col2:
        st.metric("GST @ 18%", format_currency(gst_amount))
    with col3:
        st.metric("Premium Including GST", format_currency(premium_with_gst))

    st.markdown('</div>', unsafe_allow_html=True)
