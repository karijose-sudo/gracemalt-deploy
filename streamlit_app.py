# --- Germination Inputs ---
with st.expander("Germination Measurements", expanded=False):
    col5, col6 = st.columns(2)
    with col5:
        mc_48 = st.number_input('MC 48 hrs (%)', 0.0, 100.0, 43.0)
        mc_72 = st.number_input('MC 72 hrs (%)', 0.0, 100.0, 41.8)
        mc_120 = st.number_input('MC 120 hrs (%)', 0.0, 100.0, 37.8)
    with col6:
        chit_48 = st.number_input('Chit Count 48 hrs (%)', 0.0, 100.0, 95.0)
        chit_72 = st.number_input('Chit Count 72 hrs (%)', 0.0, 100.0, 97.0)
        chit_120_raw = st.number_input('Chit Count 120 hrs (Non-grown)', 0.0, 100.0, 2.0)  # raw non-grown %

# --- Apply same preprocessing as training ---
chit_120 = 100 - chit_120_raw  # Correct 120h chit count
ΔMC_48_72 = mc_72 - mc_48
ΔMC_72_120 = mc_120 - mc_72
ΔChit_48_72 = chit_72 - chit_48
ΔChit_72_120 = chit_120 - chit_72

# Uniformity ratios (match training logic)
Uniformity_MC = ΔMC_72_120 / ΔMC_48_72 if ΔMC_48_72 != 0 else 0
Uniformity_Chit = ΔChit_72_120 / ΔChit_48_72 if ΔChit_48_72 != 0 else 0

# Coefficient of variation
chit_list = [chit_48, chit_72, chit_120]
Chit_CV = (pd.Series(chit_list).std() / pd.Series(chit_list).mean()) * 100

# Efficiency ratios
Efficiency_48_72 = ΔChit_48_72 / ΔMC_48_72 if ΔMC_48_72 != 0 else 0
Efficiency_72_120 = ΔChit_72_120 / ΔMC_72_120 if ΔMC_72_120 != 0 else 0

# Add to user_input dict
user_input.update({
    'ΔMC_48_72': ΔMC_48_72,
    'ΔMC_72_120': ΔMC_72_120,
    'ΔChit_48_72': ΔChit_48_72,
    'ΔChit_72_120': ΔChit_72_120,
    'Uniformity_MC': Uniformity_MC,
    'Uniformity_Chit': Uniformity_Chit,
    'Chit_CV': Chit_CV,
    'Efficiency_48_72': Efficiency_48_72,
    'Efficiency_72_120': Efficiency_72_120
})

# Display for user
st.subheader("Calculated Derived Germination Dynamics")
st.write(user_input)
