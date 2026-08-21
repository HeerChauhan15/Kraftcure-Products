import streamlit as st
import math
from logo_b64 import KRAFTCURE_LOGO_B64, POLICYGRACE_LOGO_B64


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Kraftcure Products",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DASHBOARD UI
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   DASHBOARD HEADER
   ============================================================ */

.dashboard-header {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e3a8a,
        #2563eb
    );

    border-radius: 20px;
    padding: 28px 34px;
    margin-bottom: 28px;

    box-shadow:
        0 16px 35px
        rgba(15, 23, 42, 0.20);
}

.dashboard-header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 25px;
}

.dashboard-logo {
    height: 48px;
    max-width: 160px;
    object-fit: contain;
}

.dashboard-title-area {
    text-align: center;
    flex: 1;
}

.dashboard-badge {
    color: #bfdbfe;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.dashboard-title {
    color: white;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 6px;
}

.dashboard-subtitle {
    color: #dbeafe;
    font-size: 14px;
    line-height: 1.5;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-label {
    color: #2563eb;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-top: 15px;
    margin-bottom: 6px;
}

.section-title {
    color: #0f172a;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 18px;
}


/* ============================================================
   DASHBOARD CARD
   ============================================================ */

.dashboard-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 20px;

    box-shadow:
        0 8px 20px
        rgba(15, 23, 42, 0.05);
}


/* ============================================================
   KPI CARDS
   ============================================================ */

.kpi-card {
    min-height: 155px;
    border-radius: 18px;
    padding: 22px;
    color: white;

    box-shadow:
        0 10px 24px
        rgba(15, 23, 42, 0.14);

    position: relative;
    overflow: hidden;
}

.kpi-card::after {
    content: "";
    position: absolute;

    width: 110px;
    height: 110px;

    border-radius: 50%;

    top: -40px;
    right: -40px;

    background:
        rgba(255, 255, 255, 0.10);
}

.kpi-purple {
    background:
        linear-gradient(
            135deg,
            #3730a3,
            #6366f1
        );
}

.kpi-teal {
    background:
        linear-gradient(
            135deg,
            #0f766e,
            #14b8a6
        );
}

.kpi-orange {
    background:
        linear-gradient(
            135deg,
            #c2410c,
            #f97316
        );
}

.kpi-dark {
    background:
        linear-gradient(
            135deg,
            #1e293b,
            #475569
        );
}

.kpi-label {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.3px;
    opacity: 0.85;

    margin-bottom: 22px;

    position: relative;
    z-index: 2;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;

    position: relative;
    z-index: 2;
}

.kpi-note {
    font-size: 11px;
    margin-top: 18px;
    opacity: 0.82;

    position: relative;
    z-index: 2;
}


/* ============================================================
   FINAL PREMIUM CARD
   ============================================================ */

.final-result-card {
    background:
        linear-gradient(
            135deg,
            #1e40af,
            #2563eb,
            #3b82f6
        );

    border-radius: 22px;

    padding: 32px;

    text-align: center;
    color: white;

    margin-top: 24px;

    box-shadow:
        0 18px 40px
        rgba(37, 99, 235, 0.24);
}

.final-result-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    opacity: 0.85;
}

.final-result-value {
    font-size: 48px;
    font-weight: 800;
    margin-top: 8px;
}

.final-result-note {
    font-size: 12px;
    opacity: 0.82;
    margin-top: 7px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 11px;
    margin-top: 32px;
    padding-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTION
# ============================================================

def render_html(html):
    st.markdown(
        html.strip(),
        unsafe_allow_html=True
    )


# ============================================================
# GST
# ============================================================

GST_RATE = 18.0


# ============================================================
# PRODUCT DATA
# CALCULATOR LOGIC UNCHANGED
# ============================================================

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
            "Tata": 169.00,
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
            "3 Lakh": 2287.288135593220,
            "5 Lakh": 3369.00,
        },
    },
}


# ============================================================
# HELPER FUNCTIONS
# CALCULATION LOGIC UNCHANGED
# ============================================================

def round_half_up(amount):

    if amount >= 0:
        return math.floor(amount + 0.5)

    return -math.floor(-amount + 0.5)


def format_currency(amount):

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

            groups.insert(
                0,
                remaining[-2:]
            )

            remaining = remaining[:-2]

        if remaining:

            groups.insert(
                0,
                remaining
            )

        formatted = (
            ",".join(groups)
            + ","
            + last_three
        )

    if negative:

        formatted = "-" + formatted

    return f"₹{formatted}"


def get_insurer_options(rates_dict):

    return sorted(
        rates_dict.items(),
        key=lambda x: x[1]
    )


# ============================================================
# DASHBOARD HEADER
# ============================================================

render_html(
    f"""
<div class="dashboard-header">

<div class="dashboard-header-content">

<img
class="dashboard-logo"
src="data:image/png;base64,{KRAFTCURE_LOGO_B64}"
alt="Kraftcure logo"
>

<div class="dashboard-title-area">

<div class="dashboard-badge">
KRAFTCURE • POLICYGRACE
</div>

<div class="dashboard-title">
Kraftcure Products Calculator
</div>

<div class="dashboard-subtitle">
Select your insurance products, choose the right coverage options
and calculate the final premium instantly.
</div>

</div>

<img
class="dashboard-logo"
src="data:image/png;base64,{POLICYGRACE_LOGO_B64}"
alt="Policygrace logo"
>

</div>

</div>
"""
)


# ============================================================
# PRODUCT SELECTION
# ============================================================

render_html("""
<div class="section-label">
STEP 01
</div>

<div class="section-title">
Select Products
</div>

<div class="section-subtitle">
Choose one or more products to include in the quotation.
</div>
""")


st.markdown(
    '<div class="dashboard-card">',
    unsafe_allow_html=True
)

selected_products = st.multiselect(
    "Which product(s) do you want to quote?",
    list(PRODUCTS.keys())
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PER PRODUCT OPTIONS
# ============================================================

product_choices = {}


if selected_products:

    st.divider()

    render_html("""
<div class="section-label">
STEP 02
</div>

<div class="section-title">
Choose Product Options
</div>

<div class="section-subtitle">
Select the insurer or coverage option for each product.
</div>
""")

    st.markdown(
        '<div class="dashboard-card">',
        unsafe_allow_html=True
    )

    for product_name in selected_products:

        product = PRODUCTS[product_name]

        col_label, col_input = st.columns(
            [1, 2]
        )

        if product["type"] == "insurer":

            options = get_insurer_options(
                product["rates"]
            )

            insurer_names = [
                insurer
                for insurer, rate in options
            ]

            with col_label:

                st.markdown(
                    f"**{product_name}**"
                )

            with col_input:

                chosen_insurer = st.selectbox(
                    f"Insurer for {product_name}",
                    insurer_names,
                    key=f"insurer_{product_name}",
                    label_visibility="collapsed"
                )

            chosen_rate = (
                product["rates"]
                [chosen_insurer]
            )

            product_choices[product_name] = (
                "Standard",
                chosen_insurer,
                chosen_rate
            )


        elif product["type"] == "tier":

            tier_labels = list(
                product["rates"].keys()
            )

            with col_label:

                st.markdown(
                    f"**{product_name}**"
                )

            with col_input:

                tier = st.selectbox(
                    f"Sum Insured tier for {product_name}",
                    tier_labels,
                    key=f"tier_{product_name}",
                    label_visibility="collapsed"
                )

            rate = (
                product["rates"][tier]
            )

            product_choices[product_name] = (
                tier,
                product["insurer"],
                rate
            )


        else:

            insurer, rate = list(
                product["rates"].items()
            )[0]

            with col_label:

                st.markdown(
                    f"**{product_name}**"
                )

            with col_input:

                st.caption(
                    f"{insurer} "
                    "(only option available)"
                )

            product_choices[product_name] = (
                "Standard",
                insurer,
                rate
            )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# OPTIONAL LOADING
# ============================================================

loading = 0.0


if selected_products:

    st.divider()

    render_html("""
<div class="section-label">
STEP 03
</div>

<div class="section-title">
Loading / Partner Commission
</div>

<div class="section-subtitle">
Optionally add partner commission to the combined premium.
</div>
""")

    st.markdown(
        '<div class="dashboard-card">',
        unsafe_allow_html=True
    )

    loading = st.number_input(
        "Loading (partner commission) on combined premium (%)",
        min_value=0.0,
        max_value=99.0,
        value=0.0,
        step=0.5,
        help=(
            "Premium is grossed up so this percentage "
            "of the final premium before GST equals "
            "the partner payout."
        )
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# CALCULATE BUTTON
# ============================================================

if selected_products:

    calculate = st.button(
        "Calculate Premium",
        type="primary",
        use_container_width=True
    )

else:

    calculate = False

    st.info(
        "Select at least one product above "
        "to calculate a premium."
    )


# ============================================================
# CALCULATION RESULTS
# CALCULATOR LOGIC UNCHANGED
# ============================================================

if calculate:

    st.divider()

    render_html("""
<div class="section-label">
CALCULATION RESULTS
</div>

<div class="section-title">
Premium Quotation
</div>

<div class="section-subtitle">
Live premium calculation based on your selected products.
</div>
""")


    # --------------------------------------------------------
    # PRODUCT PREMIUM CALCULATION
    # --------------------------------------------------------

    total_base_premium = 0.0

    for product_name in selected_products:

        label, insurer, rate = (
            product_choices[product_name]
        )

        total_base_premium += rate


    # --------------------------------------------------------
    # LOADING CALCULATION
    # UNCHANGED
    # --------------------------------------------------------

    premium_before_gst = (
        total_base_premium /
        (1 - loading / 100)
    )

    loading_amount = (
        premium_before_gst -
        total_base_premium
    )

    partner_payout = loading_amount

    gst_amount = (
        premium_before_gst *
        GST_RATE / 100
    )

    premium_with_gst = (
        premium_before_gst +
        gst_amount
    )


    # ========================================================
    # SELECTED PRODUCTS
    # ========================================================

    st.subheader("Selected Products")

    for product_name in selected_products:

        label, insurer, rate = (
            product_choices[product_name]
        )

        product_col, insurer_col, premium_col = (
            st.columns([2, 2, 1])
        )

        with product_col:

            st.write(
                f"**{product_name}**"
            )

        with insurer_col:

            if label == "Standard":

                st.caption(insurer)

            else:

                st.caption(
                    f"{insurer} • {label}"
                )

        with premium_col:

            st.write(
                format_currency(rate)
            )


    # ========================================================
    # KPI DASHBOARD
    # ========================================================

    st.divider()

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        render_html(f"""
<div class="kpi-card kpi-purple">
<div class="kpi-label">
BASE PREMIUM
</div>

<div class="kpi-value">
{format_currency(total_base_premium)}
</div>

<div class="kpi-note">
Combined product premium
</div>
</div>
""")


    with c2:

        render_html(f"""
<div class="kpi-card kpi-teal">
<div class="kpi-label">
LOADING AMOUNT
</div>

<div class="kpi-value">
{format_currency(loading_amount)}
</div>

<div class="kpi-note">
Partner commission amount
</div>
</div>
""")


    with c3:

        render_html(f"""
<div class="kpi-card kpi-orange">
<div class="kpi-label">
PARTNER PAYOUT
</div>

<div class="kpi-value">
{format_currency(partner_payout)}
</div>

<div class="kpi-note">
Calculated partner payout
</div>
</div>
""")


    with c4:

        render_html(f"""
<div class="kpi-card kpi-dark">
<div class="kpi-label">
GST AMOUNT
</div>

<div class="kpi-value">
{format_currency(gst_amount)}
</div>

<div class="kpi-note">
GST at 18 percent
</div>
</div>
""")


    # ========================================================
    # FINAL PREMIUM
    # ========================================================

    render_html(f"""
<div class="final-result-card">

<div class="final-result-label">
FINAL PREMIUM INCLUDING GST
</div>

<div class="final-result-value">
{format_currency(premium_with_gst)}
</div>

<div class="final-result-note">
Premium before GST: {format_currency(premium_before_gst)}
</div>

</div>
""")


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">
KRAFTCURE PRODUCTS • POWERED BY POLICYGRACE
</div>
""")
