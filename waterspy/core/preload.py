"""Here are some variables containing the data that can be preloaded into the database."""

UNITS = ["-", "%", "‰", "°C", "mbar", "Ω*cm", "kΩ*cm", "mg/L", "µg/L", "µg/g", "µS/cm", "mS/cm", "PSU", "mV", "µM",
         "mM", "ng E2 eq./L", "ng BaP eq./L", "n/100 ml", "n/1000 ml", "mmH2O", "cmH2O", "Pa", "bar", "m3/h", "ng/L"]

ANALYTES = [
    {
        "analyte": "XE",
        "detail": "Xenoestrogens"
    },
    {
        "analyte": "PAH",
        "detail": "Polycyclic Aromatic Hydrocarbons"
    },
    {
        "analyte": "POC",
        "detail": "Particulate Organic Carbon"
    },
    {
        "analyte": "PN",
        "detail": "Particulate Nitrogen"
    },
    {
        "analyte": "C:N",
        "detail": "Carbon-to-Nitrogen Ratio"
    },
    {
        "analyte": "δ13C (POC)",
        "detail": "Carbon Isotope Composition of Particulate Organic Carbon"
    },
    {
        "analyte": "δ15N (PN)",
        "detail": "Nitrogen Isotope Composition of Particulate Nitrogen"
    },
    {
        "analyte": "Diss. As",
        "detail": "Dissolved Arsenic"
    },
    {
        "analyte": "Diss. Cd",
        "detail": "Dissolved Cadmium"
    },
    {
        "analyte": "Diss. Pb",
        "detail": "Dissolved Lead"
    },
    {
        "analyte": "Diss. Cr",
        "detail": "Dissolved Chromium"
    },
    {
        "analyte": "Diss. Ni",
        "detail": "Dissolved Nickel"
    },
    {
        "analyte": "Part. Cd",
        "detail": "Particulate Cadmium"
    },
    {
        "analyte": "Part. Pb",
        "detail": "Particulate Lead"
    },
    {
        "analyte": "Part. Cr",
        "detail": "Particulate Chromium"
    },
    {
        "analyte": "Part. Ni",
        "detail": "Particulate Nickel"
    },
    {
        "analyte": "δ18O",
        "detail": "Oxygen Isotope Composition"
    },
    {
        "analyte": "δD",
        "detail": "Deuterium Isotope Composition"
    },
    {
        "analyte": "Cl",
        "detail": "Chloride"
    },
    {
        "analyte": "Br",
        "detail": "Bromide"
    },
    {
        "analyte": "F",
        "detail": "Fluoride"
    },
    {
        "analyte": "SO4",
        "detail": "Sulfate"
    },
    {
        "analyte": "NO3",
        "detail": "Nitrate"
    },
    {
        "analyte": "NO2",
        "detail": "Nitrite"
    },
    {
        "analyte": "PO4",
        "detail": "Phosphate"
    },
    {
        "analyte": "NH4",
        "detail": "Ammonium"
    },
    {
        "analyte": "BOD",
        "detail": "Biochemical Oxygen Demand"
    },
    {
        "analyte": "COD",
        "detail": "Chemical Oxygen Demand"
    },
    {
        "analyte": "TKN",
        "detail": "Total Kjeldahl Nitrogen"
    },
    {
        "analyte": "PTOT",
        "detail": "Total Phosphorus"
    },
    {
        "analyte": "NTOT",
        "detail": "Total Nitrogen"
    },
    {
        "analyte": "Ca",
        "detail": "Calcium"
    },
    {
        "analyte": "Mg",
        "detail": "Magnesium"
    },
    {
        "analyte": "Na",
        "detail": "Sodium"
    },
    {
        "analyte": "K",
        "detail": "Potassium"
    },
    {
        "analyte": "Mn",
        "detail": "Manganese"
    },
    {
        "analyte": "P",
        "detail": "Phosphorus"
    },
    {
        "analyte": "As",
        "detail": "Arsenic"
    },
    {
        "analyte": "Cd",
        "detail": "Cadmium"
    },
    {
        "analyte": "Cr",
        "detail": "Chromium"
    },
    {
        "analyte": "Cu",
        "detail": "Copper"
    },
    {
        "analyte": "Pb",
        "detail": "Lead"
    },
    {
        "analyte": "Ni",
        "detail": "Nickel"
    },
    {
        "analyte": "Zn",
        "detail": "Zinc"
    },
    {
        "analyte": "Hg",
        "detail": "Mercury"
    },
    {
        "analyte": "Ag",
        "detail": "Silver"
    },
    {
        "analyte": "Fe",
        "detail": "Iron"
    },
    {
        "analyte": "Fe3+",
        "detail": "Ferric Iron"
    },
    {
        "analyte": "Fe2+",
        "detail": "Ferrous Iron"
    },
    {
        "analyte": "CO3",
        "detail": "Carbonate"
    },
    {
        "analyte": "OH",
        "detail": "Hydroxide"
    },
    {
        "analyte": "HCO3",
        "detail": "Bicarbonate"
    },
    {
        "analyte": "Alkalinity",
        "detail": "Alkalinity"
    },
    {
        "analyte": "Octylphenol",
        "detail": "Octylphenol"
    },
    {
        "analyte": "Nonylphenol",
        "detail": "Nonylphenol"
    },
    {
        "analyte": "Bisphenol A",
        "detail": "Bisphenol A"
    },
    {
        "analyte": "Benzene",
        "detail": "Benzene"
    },
    {
        "analyte": "Chloroform",
        "detail": "Chloroform"
    },
    {
        "analyte": "Bromoform",
        "detail": "Bromoform"
    },
    {
        "analyte": "Bromodichloromethane",
        "detail": "Bromodichloromethane"
    },
    {
        "analyte": "Dibromochloromethane",
        "detail": "Dibromichloromethane"
    },
    {
        "analyte": "2,6-dichlorobenzamide",
        "detail": "2,6-dichlorobenzamide"
    },
    {
        "analyte": "Atrazine",
        "detail": "Atrazine"
    },
    {
        "analyte": "Bentazon",
        "detail": "Bentazon"
    },
    {
        "analyte": "Bromacil",
        "detail": "Bromacil"
    },
    {
        "analyte": "Clorotoluron",
        "detail": "Clorotoluron"
    },
    {
        "analyte": "Desethylatrazine",
        "detail": "Desethylatrazine"
    },
    {
        "analyte": "Diuron",
        "detail": "Diuron"
    },
    {
        "analyte": "Isoproturon",
        "detail": "Isoproturon"
    },
    {
        "analyte": "Simazine",
        "detail": "Simazine"
    },
    {
        "analyte": "Coliforms",
        "detail": "Coliforms"
    },
    {
        "analyte": "Enterococcus",
        "detail": "Enterococcus"
    },
    {
        "analyte": "E. Coli",
        "detail": "E. Coli"
    },
    {
        "analyte": "Salmonella",
        "detail": "Salmonella"
    },
    {
        "analyte": "TP",
        "detail": "Total Phosphorus"
    },
    {
        "analyte": "TN",
        "detail": "Total Nitrogen"
    },
    {
        "analyte": "Co",
        "detail": "Cobalt"
    },
    {
        "analyte": "δ13C (DIC)",
        "detail": "Carbon isotope 13 on dissolved inorganic carbon"
    }
]


PARAMETERS = ["pH", "Redox potential", "Salinity", "Conductivity", "Resistivity", "Temperature",
              "Oxygen - partial pressure", "Oxygen - concentration", "Oxygen - saturation", "Turbidity", "TSS", "TDS"]

ANALYTICAL_TECHNIQUES = [
    {
        "technique": "ICP-MS",
        "detail": "Inductively Coupled Plasma Mass Spectrometry. Commonly used for the analysis of trace metals in water.",
        "link": "https://en.wikipedia.org/wiki/Inductively_coupled_plasma_mass_spectrometry"
    },
    {
        "technique": "IRMS",
        "detail": "Isotope Ratio Mass Spectrometry. Commonly used for the analysis of stable isotopes in water.",
        "link": "https://en.wikipedia.org/wiki/Isotope-ratio_mass_spectrometry"
    },
    {
        "technique": "IC",
        "detail": "Ion Chromatography. Commonly used for the analysis of anions and cations in water.",
        "link": "https://en.wikipedia.org/wiki/Ion_chromatography"
    },
    {
        "technique": "Membrane filtration",
        "detail": "Membrane filtration. Commonly used for the analysis of bacteria in water.",
        "link": "https://microbiologyclass.net/membrane-filtration-technique/"
    },
    {
        "technique": "Titration",
        "detail": "Titration. Commonly used for the analysis of carbonates in water.",
        "link": "https://en.wikipedia.org/wiki/Titration"
    },
    {
        "technique": "IGCA",
        "detail": "Isotope and Gas Concentration Analyser (Picarro system). Commonly used for the analysis of stable isotopes in water.",
        "link": "https://www.picarro.com/environmental/products/l2140i_isotope_and_gas_concentration_analyzer"
    },
    {
        "technique": "CALUX",
        "detail": "Chemical Activated LUciferase gene eXpression. Used to detect specific chemicals or classes of chemicals in samples based on response of a cell line genetically modified to produce luciferase in response to the presence of the chemical. Commonly used for the analysis of polycyclic aromatic hydrocarbons and xenoestrogens in water.",
        "link": "https://en.wikipedia.org/wiki/CALUX"
    },
    {
        "technique": "CSFA",
        "detail": "Continuouse Segmented Flow Analyser. Commonly used for the analysis of nutrients in water. Used in e.g. the QuAAtro system. The principle of the CSFA is to mix the sample with reagents in a continuous flow and measure the absorbance of the resulting coloured complex.",
        "link": "https://en.wikipedia.org/wiki/Spectrophotometry"
    },
    {
        "technique": "Discrete analyser",
        "detail": "Discreet analyser. Commonly used for the analysis of nutrients in water. The principle of the discreet analyser is to mix the sample with reagents in a batch and measure the absorbance of the resulting coloured complex.",
        "link": "https://en.wikipedia.org/wiki/Spectrophotometry"
    },
    {
        "technique": "ICP-AES",
        "detail": "Inductively Coupled Plasma Atomic Emission Spectroscopy. Commonly used for the analysis of trace metals in water.",
        "link": "https://en.wikipedia.org/wiki/Inductively_coupled_plasma_atomic_emission_spectroscopy"
    },
    {
        "technique": "GC-MS",
        "detail": "Gas Chromatography Mass Spectrometry. Commonly used for the analysis of organic compounds in water.",
        "link": "https://en.wikipedia.org/wiki/Gas_chromatography%E2%80%93mass_spectrometry"
    },
    {
        "technique": "Headspace GC-MS",
        "detail": "Headspace Gas Chromatography Mass Spectrometry. Commonly used for the analysis of volatile organic compounds in water. Differs from GC-MS in that the sample is not directly injected into the GC but is instead heated to produce a gas phase above the sample which is then injected into the GC.",
        "link": "https://www.innovatechlabs.com/analytical-services-gcms-headspace-analysis/"
    },
    {
        "technique": "FIMS",
        "detail": "Flow Injection Mercury System. Commonly used for the analysis of mercury in water.",
        "link": "https://www.perkinelmer.com/uk/product/fims-100-flow-injection-mercury-system-b0509550"
    },
    {
        "technique": "LC-MS/MS",
        "detail": "Liquid Chromatography Tandem Mass Spectrometry. Commonly used for the analysis of organic compounds in water.",
        "link": "https://www.eag.com/app-note/liquid-chromatography-tandem-mass-spectrometry-lc-ms-ms/"
    },
    {
        "technique": "Incubation",
        "detail": "Five to seven days incubation at 20 degrees Celsius. Commonly used for the analysis of BOD in water.",
        "link": "https://reflabos.vito.be/2023/WAC_III_D_010.pdf"
    },
    {
        "technique": "Small-scale sealed tube",
        "detail": "The principle of the small-scale sealed-tube method for determining Chemical Oxygen Demand (COD) is based on the oxidation of organic and oxidizable inorganic components in water samples. This oxidation occurs in a 50% sulfuric acid medium using a standard potassium dichromate solution. The COD value is then calculated based on the amount of potassium dichromate consumed during the reaction.",
        "link": "https://reflabos.vito.be/2023/WAC_III_D_020.pdf"
    }
]


METHODS = [
    {
        "target_group": "Dissolved Elements",
        "technique": "ICP-MS",
        "matrix": "groundwater"
    },
    {
        "target_group": "Dissolved Elements",
        "technique": "ICP-MS",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Dissolved Elements",
        "technique": "ICP-MS",
        "matrix": "wastewater"
    },
    {
        "target_group": "Particulate Elements",
        "technique": "ICP-MS",
        "matrix": "groundwater"
    },
    {
        "target_group": "Particulate Elements",
        "technique": "ICP-MS",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Particulate Elements",
        "technique": "ICP-MS",
        "matrix": "wastewater"
    },
    {
        "target_group": "Total Elements",
        "technique": "ICP-MS",
        "matrix": "groundwater"
    },
    {
        "target_group": "Total Elements",
        "technique": "ICP-MS",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Total Elements",
        "technique": "ICP-MS",
        "matrix": "wastewater"
    },
    {
        "target_group": "Total Elements",
        "technique": "ICP-AES",
        "matrix": "groundwater"
    },
    {
        "target_group": "Total Elements",
        "technique": "ICP-AES",
        "matrix": "wastewater"
    },
    {
        "target_group": "Anions",
        "technique": "IC",
        "matrix": "groundwater"
    },
    {
        "target_group": "Anions",
        "technique": "IC",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Anions",
        "technique": "IC",
        "matrix": "wastewater"
    },
    {
        "target_group": "Microorganisms",
        "technique": "Membrane filtration",
        "matrix": "groundwater"
    },
    {
        "target_group": "Microorganisms",
        "technique": "Membrane filtration",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Microorganisms",
        "technique": "Membrane filtration",
        "matrix": "wastewater"
    },
    {
        "target_group": "Alkalinity",
        "technique": "Titration",
        "matrix": "groundwater"
    },
    {
        "target_group": "Alkalinity",
        "technique": "Titration",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Alkalinity",
        "technique": "Titration",
        "matrix": "wastewater"
    },
    {
        "target_group": "Polycyclic Aromatic Hydrocarbons",
        "technique": "CALUX",
        "matrix": "groundwater"
    },
    {
        "target_group": "Polycyclic Aromatic Hydrocarbons",
        "technique": "CALUX",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Polycyclic Aromatic Hydrocarbons",
        "technique": "CALUX",
        "matrix": "wastewater"
    },
    {
        "target_group": "Xenoestrogens",
        "technique": "CALUX",
        "matrix": "groundwater"
    },
    {
        "target_group": "Xenoestrogens",
        "technique": "CALUX",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Xenoestrogens",
        "technique": "CALUX",
        "matrix": "wastewater"
    },
    {
        "target_group": "Stable water isotopes",
        "technique": "IGCA",
        "matrix": "groundwater"
    },
    {
        "target_group": "Stable water isotopes",
        "technique": "IGCA",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Stable water isotopes",
        "technique": "IGCA",
        "matrix": "wastewater"
    },
    {
        "target_group": "Nutrients",
        "technique": "CSFA",
        "matrix": "groundwater"
    },
    {
        "target_group": "Nutrients",
        "technique": "CSFA",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Nutrients",
        "technique": "CSFA",
        "matrix": "wastewater"
    },
    {
        "target_group": "Ions",
        "technique": "Discrete analyser",
        "matrix": "groundwater"
    },
    {
        "target_group": "Ions",
        "technique": "Discrete analyser",
        "matrix": "wastewater"
    },
    {
        "target_group": "Stable isotopes in dissolved phase",
        "technique": "IRMS",
        "matrix": "groundwater"
    },
    {
        "target_group": "Stable isotopes in dissolved phase",
        "technique": "IRMS",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Stable isotopes in dissolved phase",
        "technique": "IRMS",
        "matrix": "wastewater"
    },
    {
        "target_group": "Stable isotopes in particulate phase",
        "technique": "IRMS",
        "matrix": "groundwater"
    },
    {
        "target_group": "Stable isotopes in particulate phase",
        "technique": "IRMS",
        "matrix": "surfacewater"
    },
    {
        "target_group": "Stable isotopes in particulate phase",
        "technique": "IRMS",
        "matrix": "wastewater"
    },
    {
        "target_group": "Pesticides",
        "technique": "LC-MS/MS",
        "matrix": "groundwater"
    },
    {
        "target_group": "Pesticides",
        "technique": "LC-MS/MS",
        "matrix": "wastewater"
    },
    {
        "target_group": "BOD",
        "technique": "Incubation",
        "matrix": "wastewater"
    },
    {
        "target_group": "COD",
        "technique": "Small-scale sealed tube",
        "matrix": "wastewater"
    },
    {
        "target_group": "Kjeldahl Nitrogen",
        "technique": "Titration",
        "matrix": "wastewater"
    },
    {
        "target_group": "Mercury",
        "technique": "FIMS",
        "matrix": "groundwater"
    },
    {
        "target_group": "Mercury",
        "technique": "FIMS",
        "matrix": "wastewater"
    },
    {
        "target_group": "Phenols",
        "technique": "GC-MS",
        "matrix": "groundwater"
    },
    {
        "target_group": "Phenols",
        "technique": "GC-MS",
        "matrix": "wastewater"
    },
    {
        "target_group": "VOC",
        "technique": "Headspace GC-MS",
        "matrix": "groundwater"
    },
    {
        "target_group": "VOC",
        "technique": "Headspace GC-MS",
        "matrix": "wastewater"
    },
    {
        "target_group": "POC",
        "technique": "CSFA",
        "matrix": "groundwater"
    },
    {
        "target_group": "POC",
        "technique": "CSFA",
        "matrix": "surfacewater"
    },
    {
        "target_group": "POC",
        "technique": "CSFA",
        "matrix": "wastewater"
    },
]


DRILLING_TECHNIQUES = [
    "Percussion drilling",
    "Rotary drilling",
    "Hand drilling",
    "Sonic drilling",
    "Direct push",
    "Unknown"
]

PIEZOMETER_MATERIALS = [
    "Steel",
    "PVC",
    "PE",
    "HDPE",
    "Unknown"
]
