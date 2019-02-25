"""
Emissions mapping for configuration.
"""

emissions = {
    "simpleNbox": ["ffi_emissions", "luc_emissions"],
    "so2": ["SO2_emissions"],
    "CH4": ["CH4_emissions"],
    "OH": ["NOX_emissions", "CO_emissions", "NMVOC_emissions"],
    "ozone": ["NOX_emissions", "CO_emissions", "NMVOC_emissions"],
    "N2O": ["N2O_emissions"],
    "bc": ["BC_emissions"],
    "oc": ["OC_emissions"],
    "CF4_halocarbon": ["CF4_emissions"],
    "C2F6_halocarbon": ["C2F6_emissions"],
    "C4F10_halocarbon": ["C4F10_emissions"],  # commented out in RCP
    "HFC23_halocarbon": ["HFC23_emissions"],
    "HFC32_halocarbon": ["HFC32_emissions"],
    "HFC4310_halocarbon": ["HFC4310_emissions"],
    "HFC125_halocarbon": ["HFC125_emissions"],
    "HFC134a_halocarbon": ["HFC134a_emissions"],
    "HFC143a_halocarbon": ["HFC143a_emissions"],
    "HFC152a_halocarbon": ["HFC152a_emissions"],  # commented out in RCP
    "HFC227ea_halocarbon": ["HFC227ea_emissions"],
    "HFC245fa_halocarbon": ["HFC245fa_emissions"],
    "HFC236fa_halocarbon": ["HFC236fa_emissions"],  # commented out in RCP
    "SF6_halocarbon": ["SF6_emissions"],
    "CFC11_halocarbon": ["CFC11_emissions"],
    "CFC12_halocarbon": ["CFC12_emissions"],
    "CFC113_halocarbon": ["CFC113_emissions"],
    "CFC114_halocarbon": ["CFC114_emissions"],
    "CFC115_halocarbon": ["CFC115_emissions"],
    "CCl4_halocarbon": ["CCl4_emissions"],
    "CH3CCl3_halocarbon": ["CH3CCl3_emissions"],
    "halon1211_halocarbon": ["halon1211_emissions"],
    "halon1301_halocarbon": ["halon1301_emissions"],
    "halon2402_halocarbon": ["halon2402_emissions"],
    "HCF22_halocarbon": ["HCF22_emissions"],
    "HCF141b_halocarbon": ["HCF141b_emissions"],
    "HCF142b_halocarbon": ["HCF142b_emissions"],
    "HCF143_halocarbon": ["HCF143_emissions"],  # commented out in RCP
    "CH3Cl_halocarbon": ["CH3Cl_emissions"],
    "CH3Br_halocarbon": ["CH3Br_emissions"],
}
