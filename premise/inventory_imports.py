from . import DATA_DIR
import wurst
from prettytable import PrettyTable
from wurst import searching as ws
from bw2io import ExcelImporter, Migration
import carculator
import carculator_truck
from pathlib import Path
import csv
import uuid
import numpy as np
from .geomap import Geomap

FILEPATH_BIOSPHERE_FLOWS = DATA_DIR / "dict_biosphere.txt"

EI_37_35_MIGRATION_MAP = {
                "fields": ["name", "reference product", "location"],
                "data": [
                    (
                        (
                            "market for water, deionised",
                            ("water, deionised",),
                            "Europe without Switzerland",
                        ),
                        {
                            "name": (
                                "market for water, deionised, from tap water, at user"
                            ),
                            "reference product": (
                                "water, deionised, from tap water, at user"
                            ),
                        },
                    ),
                    (
                        ("market for water, deionised", ("water, deionised",), "RoW"),
                        {
                            "name": (
                                "market for water, deionised, from tap water, at user"
                            ),
                            "reference product": (
                                "water, deionised, from tap water, at user"
                            ),
                        },
                    ),
                    (
                        ("market for water, deionised", ("water, deionised",), "CH"),
                        {
                            "name": (
                                "market for water, deionised, from tap water, at user"
                            ),
                            "reference product": (
                                "water, deionised, from tap water, at user"
                            )
                        },
                    ),
                    (
                        ("market for water, decarbonised", ("water, decarbonised",), "CH"),
                        {
                            "name": (
                                "market for water, decarbonised, at user"
                            ),
                            "reference product": (
                                "water, decarbonised, at user"
                            )
                            ,
                            "location": (
                                "GLO"
                            )
                        },
                    ),
                    (
                        ("water production, deionised", ("water, deionised",), "RoW"),
                        {
                            "name": (
                                "water production, deionised, from tap water, at user"
                            ),
                            "reference product": (
                                "water, deionised, from tap water, at user"
                            )
                            ,
                        },
                    ),
                    (
                        ("water production, deionised", ("water, deionised",), "Europe without Switzerland"),
                        {
                            "name": (
                                "water production, deionised, from tap water, at user"
                            ),
                            "reference product": (
                                "water, deionised, from tap water, at user"
                            )
                            ,
                        },
                    ),
                    (
                        ("market for water, ultrapure", ("water, ultrapure",), "RoW"),
                        {
                            "location": "GLO"
                        },
                    ),
                    (
                        ("market for water, ultrapure", ("water, ultrapure",), "CA-QC"),
                        {
                            "location": "GLO"
                        },
                    ),
                    (
                        (
                            "market for aluminium oxide, metallurgical",
                            ("aluminium oxide, metallurgical",),
                            "IAI Area, EU27 & EFTA",
                        ),
                        {
                            "name": "market for aluminium oxide",
                            "reference product": "aluminium oxide",
                            "location": "GLO",
                        },
                    ),
                    (
                        (
                            "market for flat glass, coated",
                            "flat glass, coated",
                            "RER",
                        ),
                        {"location": "GLO"},
                    ),
                    (
                        (
                            "market for flat glass, uncoated",
                            "flat glass, uncoated",
                            "RER",
                        ),
                        {"location": "GLO"},
                    ),

                    (
                        (
                            "market for steam, in chemical industry",
                            "steam, in chemical industry",
                            "RER",
                        ),
                        {"location": "GLO"},
                    ),
                    (
                        ("market for transport, freight train", ("transport, freight train",), "ZA"),
                        {
                            "location": "RoW",
                        },
                    ),
                    (
                        ("market for transport, freight train", ("transport, freight train",), "IN"),
                        {
                            "location": "RoW",
                        },
                    ),
                    (
                        ("hydrogen production, gaseous, petroleum refinery operation", "hydrogen, gaseous", "Europe without Switzerland"),
                        {
                            "location": "RER",
                            "name": "hydrogen cracking, APME",
                            "reference product": "hydrogen, liquid"
                        },
                    ),
                    (
                        ("hydrogen production, gaseous, petroleum refinery operation", "hydrogen, gaseous", "RoW"),
                        {
                            "location": "RoW",
                            "name": "hydrogen cracking, APME",
                            "reference product": "hydrogen, liquid"
                        },
                    ),
                    (
                        ("hydrogen production, gaseous, petroleum refinery operation", "hydrogen, gaseous", "ZA"),
                        {
                            "location": "RoW",
                            "name": "hydrogen cracking, APME",
                            "reference product": "hydrogen, liquid"
                        },
                    ),
                    (
                        ("hydrogen production, gaseous, petroleum refinery operation", "hydrogen, gaseous", "IN"),
                        {
                            "location": "RoW",
                            "name": "hydrogen cracking, APME",
                            "reference product": "hydrogen, liquid"
                        },
                    ),
                    (
                        ("hydrogen production, gaseous, petroleum refinery operation", "hydrogen, gaseous", "BR"),
                        {
                            "location": "RoW",
                            "name": "hydrogen cracking, APME",
                            "reference product": "hydrogen, liquid"
                        },
                    ),
                    (
                        ("market for tap water", "tap water", "IN"),
                        {
                            "location": "RoW",
                        },
                    ),
                    (
                        ("steel production, electric, low-alloyed",
                         "steel, low-alloyed",
                         "Europe without Switzerland and Austria"),
                        {
                            "location": "RER",
                        },
                    ),
                    (
                        ("reinforcing steel production",
                         "reinforcing steel",
                         "Europe without Austria"),
                        {
                            "location": "RER",
                        },
                    ),
                    (
                        ("smelting of copper concentrate, sulfide ore",
                         "copper, anode",
                         "RoW"),
                        {
                            "name": "smelting and refining of nickel ore",
                            "reference product": "copper concentrate, sulfide ore",
                            "location": "GLO",
                        },
                    )

                ],
            }

EI_37_36_MIGRATION_MAP = {
                "fields": ["name", "reference product", "location"],
                "data": [
                    (
                        (
                            "market for transport, freight, sea, transoceanic tanker",
                            ("transport, freight, sea, transoceanic tanker",),
                            "GLO",
                        ),
                        {
                            "name": (
                                "market for transport, freight, sea, tanker for liquid goods other than petroleum and liquefied natural gas"
                            ),
                            "reference product": (
                                "transport, freight, sea, tanker for liquid goods other than petroleum and liquefied natural gas"
                            ),
                        },
                    ),
                    (
                        (
                            "market for water, decarbonised, at user",
                            "water, decarbonised, at user",
                            "GLO",
                        ),
                        {
                            "name": "market for water, decarbonised",
                            "reference product": "water, decarbonised",
                            "location": "DE",
                        },
                    ),
                    (
                        (
                            "market for water, completely softened, from decarbonised water, at user",
                            (
                                "water, completely softened, from decarbonised water, at user",
                            ),
                            "GLO",
                        ),
                        {
                            "name": "market for water, completely softened",
                            "reference product": "water, completely softened",
                            "location": "RER",
                        },
                    ),
                    (
                        ("market for concrete block", "concrete block", "GLO"),
                        {"location": "DE"},
                    ),
                    (
                        ("steel production, electric, low-alloyed",
                         "steel, low-alloyed",
                         "Europe without Switzerland and Austria"),
                        {
                            "location": "RER",
                        },
                    ),
                    (
                        ("reinforcing steel production",
                         "reinforcing steel",
                         "Europe without Austria"),
                        {
                            "location": "RER",
                        },
                    ),
                    (
                        ("smelting of copper concentrate, sulfide ore",
                         "copper, anode",
                         "RoW"),
                        {
                            "name": "smelting and refining of nickel ore",
                            "reference product": "copper concentrate, sulfide ore",
                            "location": "GLO",
                        },
                    )
                ],
            }

EI_37_MIGRATION_MAP = {
                "fields": ["name", "location", "reference product"],
                "data": [
                    (("aluminium, ingot, primary, import from Rest of Europe", "IAI Area, EU27 & EFTA", ()),
                     {"name": "aluminium, ingot, primary, import from Rest of Europe",
                      "location": "IAI Area, EU27 & EFTA", "reference product": "aluminium, primary, ingot"}),
                    (("copper production, blister-copper", "RER", "copper, blister-copper"),
                     {"name": "nickel mine operation and benefication to nickel concentrate, 7% Ni", "location": "CN",
                      "reference product": "nickel concentrate, 7% Ni"}),
                    (("diesel, burned in diesel-electric generating set, 18.5kW", "GLO",
                      "Diesel, burned in diesel-electric generating set/GLO U"),
                     {"name": "diesel, burned in diesel-electric generating set, 18.5kW", "location": "GLO",
                      "reference product": "diesel, burned in diesel-electric generating set, 18.5kW"}),
                    (("excavation, hydraulic digger", "RER", ()),
                     {"name": "excavation, hydraulic digger", "location": "RER",
                      "reference product": "excavation, hydraulic digger"}),
                    (("heat production, heavy fuel oil, at industrial furnace 1MW", "Europe without Switzerland", ()),
                     {"name": "heat production, heavy fuel oil, at industrial furnace 1MW",
                      "location": "Europe without Switzerland",
                      "reference product": "heat, district or industrial, other than natural gas"}),
                    (("heat production, natural gas, at industrial furnace >100kW", "Europe without Switzerland", ()),
                     {"name": "heat production, natural gas, at industrial furnace >100kW",
                      "location": "Europe without Switzerland",
                      "reference product": "heat, district or industrial, other than natural gas"}),
                    (("heat pump production, for heat and power co-generation unit, 160kW electrical", "RER", ()),
                     {"name": "heat pump production, for heat and power co-generation unit, 160kW electrical",
                      "location": "RER",
                      "reference product": "heat pump, for heat and power co-generation unit, 160kW electrical"}),
                    (("heavy fuel oil, burned in refinery furnace", "RoW", ()),
                     {"name": "heavy fuel oil, burned in refinery furnace", "location": "RoW",
                      "reference product": "heavy fuel oil, burned in refinery furnace"}),
                    (("market for absorption chiller, 100kW", "GLO", ()),
                     {"name": "market for absorption chiller, 100kW", "location": "GLO",
                      "reference product": "absorption chiller, 100kW"}),
                    (("market for aluminium oxide", "GLO", "aluminium oxide"),
                     {"name": "market for aluminium oxide, metallurgical", "location": "IAI Area, EU27 & EFTA",
                      "reference product": "aluminium oxide, metallurgical"}),
                    (("market for aluminium, cast alloy", "GLO", ()),
                     {"name": "market for aluminium, cast alloy", "location": "GLO",
                      "reference product": "aluminium, cast alloy"}),
                    (("market for ammonia, liquid", "RER", "ammonia, liquid"),
                     {"name": "market for ammonia, anhydrous, liquid", "location": "RER",
                      "reference product": "ammonia, anhydrous, liquid"}),
                    (("market for ammonia, liquid", "RER", ()),
                     {"name": "market for ammonia, anhydrous, liquid", "location": "RER",
                      "reference product": "ammonia, anhydrous, liquid"}),
                    (("market for ammonium sulfate, as N", "GLO", "ammonium sulfate, as N"),
                     {"name": "market for ammonium sulfate", "location": "RER",
                      "reference product": "ammonium sulfate"}),
                    (("market for calcium chloride", "RER", ()),
                     {"name": "market for calcium chloride", "location": "RER",
                      "reference product": "calcium chloride"}),
                    (("market for cast iron", "GLO", ()),
                     {"name": "market for cast iron", "location": "GLO", "reference product": "cast iron"}),
                    (("market for cellulose fibre, inclusive blowing in", "GLO",
                      "cellulose fibre, inclusive blowing in"),
                     {"name": "market for cellulose fibre", "location": "RoW", "reference product": "cellulose fibre"}),
                    (("market for cement, unspecified", "CH", ()),
                     {"name": "market for cement, unspecified", "location": "CH",
                      "reference product": "cement, unspecified"}),
                    (("market for charcoal", "GLO", ()),
                     {"name": "market for charcoal", "location": "GLO", "reference product": "charcoal"}),
                    (("market for chemical factory, organics", "GLO", ()),
                     {"name": "market for chemical factory, organics", "location": "GLO",
                      "reference product": "chemical factory, organics"}),
                    (("market for chemical, organic", "GLO", ()),
                     {"name": "market for chemical, organic", "location": "GLO",
                      "reference product": "chemical, organic"}),
                    (("market for chemical, organic", "GLO", "Chemicals organic, at plant/GLO U"),
                     {"name": "market for chemical, organic", "location": "GLO",
                      "reference product": "chemical, organic"}),
                    (("market for chemicals, inorganic", "GLO", "Chemicals inorganic, at plant/GLO U"),
                     {"name": "market for chemicals, inorganic", "location": "GLO",
                      "reference product": "chemical, inorganic"}),
                    (("market for chemicals, inorganic", "GLO", ()),
                     {"name": "market for chemicals, inorganic", "location": "GLO",
                      "reference product": "chemical, inorganic"}),
                    (("market for chlorine, liquid", "RER", ()),
                     {"name": "market for chlorine, liquid", "location": "RER",
                      "reference product": "chlorine, liquid"}),
                    (("market for chromium", "GLO", ()),
                     {"name": "market for chromium", "location": "GLO", "reference product": "chromium"}),
                    (("market for concrete block", "GLO", "concrete block"),
                     {"name": "market for concrete block", "location": "DE", "reference product": "concrete block"}),
                    (("market for concrete, normal", "CH", ()),
                     {"name": "market for concrete, normal", "location": "CH",
                      "reference product": "concrete, normal"}),
                    (("market for copper", "GLO", ()),
                     {"name": "market for copper, anode", "location": "GLO", "reference product": "copper, anode"}),
                    (("market for copper", "GLO", "copper"),
                     {"name": "market for copper, anode", "location": "GLO", "reference product": "copper, anode"}),
                    (("market for diesel, burned in building machine", "GLO", ()),
                     {"name": "market for diesel, burned in building machine", "location": "GLO",
                      "reference product": "diesel, burned in building machine"}),
                    (("market for dimethyl sulfate", "RER", ()),
                     {"name": "market for dimethyl sulfate", "location": "RER",
                      "reference product": "dimethyl sulfate"}),
                    (("market for gas power plant, combined cycle, 400MW electrical", "GLO", ()),
                     {"name": "market for gas power plant, combined cycle, 400MW electrical", "location": "GLO",
                      "reference product": "gas power plant, combined cycle, 400MW electrical"}),
                    (("market for gas turbine, 10MW electrical", "GLO", ()),
                     {"name": "market for gas turbine, 10MW electrical", "location": "GLO",
                      "reference product": "gas turbine, 10MW electrical"}),
                    (("market for gas turbine, 10MW electrical", "GLO", "gas turbine, 10MWe, at production plant"),
                     {"name": "market for gas turbine, 10MW electrical", "location": "GLO",
                      "reference product": "gas turbine, 10MW electrical"}),
                    (("market for hard coal", "Europe, without Russia and Turkey", ()),
                     {"name": "market for hard coal", "location": "Europe, without Russia and Turkey",
                      "reference product": "hard coal"}),
                    (("market for hydrochloric acid, without water, in 30% solution state", "RER", ()),
                     {"name": "market for hydrochloric acid, without water, in 30% solution state", "location": "RER",
                      "reference product": "hydrochloric acid, without water, in 30% solution state"}),
                    (("market for lead", "GLO", ()),
                     {"name": "market for lead", "location": "GLO", "reference product": "lead"}),
                    (("market for lignite power plant", "GLO", ()),
                     {"name": "market for lignite power plant", "location": "GLO",
                      "reference product": "lignite power plant"}),
                    (("market for liquid storage tank, chemicals, organics", "GLO", ()),
                     {"name": "market for liquid storage tank, chemicals, organics", "location": "GLO",
                      "reference product": "liquid storage tank, chemicals, organics"}),
                    (("market for lubricating oil", "RER", "Lubricating oil, at plant/RER U"),
                     {"name": "market for lubricating oil", "location": "RER", "reference product": "lubricating oil"}),
                    (("market for lubricating oil", "RER", ()),
                     {"name": "market for lubricating oil", "location": "RER", "reference product": "lubricating oil"}),
                    (("market for magnesium", "GLO", ()),
                     {"name": "market for magnesium", "location": "GLO", "reference product": "magnesium"}),
                    (("market for methanol", "GLO", ()),
                     {"name": "market for methanol", "location": "GLO", "reference product": "methanol"}),
                    (("market for monoethanolamine", "GLO", ()),
                     {"name": "market for monoethanolamine", "location": "GLO",
                      "reference product": "monoethanolamine"}),
                    (("market for natural gas, from medium pressure network (0.1-1 bar), at service station", "GLO",
                      "natural gas, from medium pressure network (0.1-1 bar), at service station"),
                     {"name": "market for natural gas, medium pressure, vehicle grade", "location": "GLO",
                      "reference product": "natural gas, medium pressure, vehicle grade"}),
                    (("market for nickel, 99.5%", "GLO", "nickel, 99.5%"),
                     {"name": "market for nickel, class 1", "location": "GLO", "reference product": "nickel, class 1"}),
                    (("market for nitrogen fertiliser, as N", "GLO", "nitrogen fertiliser, as N"),
                     {"name": "market group for inorganic nitrogen fertiliser, as N", "location": "RER",
                      "reference product": "inorganic nitrogen fertiliser, as N"}),
                    (("market for NOx retained, by selective catalytic reduction", "GLO", ()),
                     {"name": "market for NOx retained, by selective catalytic reduction", "location": "GLO",
                      "reference product": "NOx retained, by selective catalytic reduction"}),
                    (("market for phosphate fertiliser, as P2O5", "GLO", "phosphate fertiliser, as P2O5"),
                     {"name": "market group for inorganic phosphorus fertiliser, as P2O5", "location": "RER",
                      "reference product": "inorganic phosphorus fertiliser, as P2O5"}),
                    (("market for polyvinylfluoride", "GLO", ()),
                     {"name": "market for polyvinylfluoride", "location": "GLO",
                      "reference product": "polyvinylfluoride"}),
                    (("market for potassium fertiliser, as K2O", "GLO", "potassium fertiliser, as K2O"),
                     {"name": "market group for inorganic potassium fertiliser, as K2O", "location": "RER",
                      "reference product": "inorganic potassium fertiliser, as K2O"}),
                    (("market for potassium sulfate, as K2O", "GLO", "potassium sulfate, as K2O"),
                     {"name": "market for potassium sulfate", "location": "RER",
                      "reference product": "potassium sulfate"}),
                    (("market for pump, 40W", "GLO", ()),
                     {"name": "market for pump, 40W", "location": "GLO", "reference product": "pump, 40W"}),
                    (("market for reinforcing steel", "GLO", ()),
                     {"name": "market for reinforcing steel", "location": "GLO",
                      "reference product": "reinforcing steel"}),
                    (("market for sodium hydroxide, without water, in 50% solution state", "GLO", ()),
                     {"name": "market for sodium hydroxide, without water, in 50% solution state", "location": "GLO",
                      "reference product": "sodium hydroxide, without water, in 50% solution state"}),
                    (("market for sodium hypochlorite, without water, in 15% solution state", "RER", ()),
                     {"name": "market for sodium hypochlorite, without water, in 15% solution state", "location": "RER",
                      "reference product": "sodium hypochlorite, without water, in 15% solution state"}),
                    (("market for SOx retained, in hard coal flue gas desulfurisation", "RER", ()),
                     {"name": "market for SOx retained, in hard coal flue gas desulfurisation", "location": "RER",
                      "reference product": "SOx retained, in hard coal flue gas desulfurisation"}),
                    (("market for steam, in chemical industry", "GLO", ()),
                     {"name": "market for steam, in chemical industry", "location": "RER",
                      "reference product": "steam, in chemical industry"}),
                    (("market for steam, in chemical industry", "GLO", "steam, in chemical industry"),
                     {"name": "market for steam, in chemical industry", "location": "RER",
                      "reference product": "steam, in chemical industry"}),
                    (("market for steel, low-alloyed", "GLO", ()),
                     {"name": "market for steel, low-alloyed", "location": "GLO",
                      "reference product": "steel, low-alloyed"}),
                    (("market for steel, low-alloyed", "GLO", "Steel, low-alloyed, at plant"),
                     {"name": "market for steel, low-alloyed", "location": "GLO",
                      "reference product": "steel, low-alloyed"}),
                    (("market for steel, low-alloyed", "GLO", "Steel, low-alloyed, at plant/RER U"),
                     {"name": "market for steel, low-alloyed", "location": "GLO",
                      "reference product": "steel, low-alloyed"}),
                    (("market for sulfuric acid", "RER", ()),
                     {"name": "market for sulfuric acid", "location": "RER", "reference product": "sulfuric acid"}),
                    (("market for tap water", "Europe without Switzerland", ()),
                     {"name": "market for tap water", "location": "Europe without Switzerland",
                      "reference product": "tap water"}),
                    (("market for transport, freight train", "Europe without Switzerland", ()),
                     {"name": "market for transport, freight train", "location": "Europe without Switzerland",
                      "reference product": "transport, freight train"}),
                    (("market for transport, freight train", "Europe without Switzerland", "Transport, freight, rail"),
                     {"name": "market for transport, freight train", "location": "Europe without Switzerland",
                      "reference product": "transport, freight train"}),
                    (("market for transport, freight train", "Europe without Switzerland",
                      "Transport, freight, rail/RER U"),
                     {"name": "market for transport, freight train", "location": "Europe without Switzerland",
                      "reference product": "transport, freight train"}),
                    (("market for transport, freight, lorry, unspecified", "RER",
                      "Transport, lorry >16t, fleet average"),
                     {"name": "market for transport, freight, lorry, unspecified", "location": "RER",
                      "reference product": "transport, freight, lorry, unspecified"}),
                    (("market for transport, freight, lorry, unspecified", "RER",
                      "Transport, lorry >16t, fleet average/RER U"),
                     {"name": "market for transport, freight, lorry, unspecified", "location": "RER",
                      "reference product": "transport, freight, lorry, unspecified"}),
                    (("market for transport, freight, lorry, unspecified", "RER", ()),
                     {"name": "market for transport, freight, lorry, unspecified", "location": "RER",
                      "reference product": "transport, freight, lorry, unspecified"}),
                    (("market for transport, freight, sea, transoceanic tanker", "GLO",
                      "transport, freight, sea, transoceanic tanker"),
                     {"name": "market for transport, freight, sea, tanker for petroleum", "location": "GLO",
                      "reference product": "transport, freight, sea, tanker for petroleum"}),
                    (("market for triethylene glycol", "RER", ()),
                     {"name": "market for triethylene glycol", "location": "RER",
                      "reference product": "triethylene glycol"}),
                    (("market for urea, as N", "GLO", "urea, as N"),
                     {"name": "market for urea", "location": "RER", "reference product": "urea"}),
                    (("market for water, completely softened, from decarbonised water, at user", "GLO",
                      "water, completely softened, from decarbonised water, at user"),
                     {"name": "market for water, completely softened", "location": "RER",
                      "reference product": "water, completely softened"}),
                    (("market for water, completely softened, from decarbonised water, at user", "GLO", ()),
                     {"name": "market for water, completely softened", "location": "RER",
                      "reference product": "water, completely softened"}),
                    (("market for water, decarbonised", "CH", ()),
                     {"name": "market for water, decarbonised", "location": "CH",
                      "reference product": "water, decarbonised"}),
                    (("market for water, decarbonised, at user", "GLO", "water, decarbonised, at user"),
                     {"name": "market for water, decarbonised", "location": "RoW",
                      "reference product": "water, decarbonised"}),
                    (("market for water, decarbonised, at user", "GLO", ()),
                     {"name": "market for water, decarbonised", "location": "RoW",
                      "reference product": "water, decarbonised"}),
                    (("market for wood chips, wet, measured as dry mass", "Europe without Switzerland", ()),
                     {"name": "market for wood chips, wet, measured as dry mass",
                      "location": "Europe without Switzerland",
                      "reference product": "wood chips, wet, measured as dry mass"}),
                    (("market group for electricity, high voltage", "ENTSO-E", ()),
                     {"name": "market group for electricity, high voltage", "location": "ENTSO-E",
                      "reference product": "electricity, high voltage"}),
                    (("market group for electricity, high voltage", "RER", ()),
                     {"name": "market group for electricity, high voltage", "location": "RER",
                      "reference product": "electricity, high voltage"}),
                    (("market group for electricity, low voltage", "ENTSO-E", ()),
                     {"name": "market group for electricity, low voltage", "location": "ENTSO-E",
                      "reference product": "electricity, low voltage"}),
                    (("market group for electricity, medium voltage", "ENTSO-E", ()),
                     {"name": "market group for electricity, medium voltage", "location": "ENTSO-E",
                      "reference product": "electricity, medium voltage"}),
                    (("market group for light fuel oil", "RER", ()),
                     {"name": "market group for light fuel oil", "location": "RER",
                      "reference product": "light fuel oil"}),
                    (("market group for natural gas, high pressure", "Europe without Switzerland", ()),
                     {"name": "market group for natural gas, high pressure", "location": "Europe without Switzerland",
                      "reference product": "natural gas, high pressure"}),
                    (("nickel mine operation, sulfidic ore", "GLO", "nickel, 99.5%"),
                     {"name": "nickel mine operation and benefication to nickel concentrate, 7% Ni", "location": "CN",
                      "reference product": "nickel concentrate, 7% Ni"}),
                    (("platinum group metal mine operation, ore with high rhodium content", "ZA", "nickel, 99.5%"),
                     {"name": "platinum group metal, extraction and refinery operations", "location": "ZA",
                      "reference product": "nickel, class 1"}),
                    (("plywood production, for outdoor use", "RER", "plywood, for outdoor use"),
                     {"name": "plywood production", "location": "RER", "reference product": "plywood"}),
                    (("reinforcing steel production", "RER", "reinforcing steel"),
                     {"name": "reinforcing steel production", "location": "Europe without Austria",
                      "reference product": "reinforcing steel"}),
                    (("steel production, electric, chromium steel 18/8", "RER", ()),
                     {"name": "steel production, electric, chromium steel 18/8", "location": "RER",
                      "reference product": "steel, chromium steel 18/8"}),
                    (("steel production, electric, low-alloyed", "RER", "steel, low-alloyed"),
                     {"name": "steel production, electric, low-alloyed",
                      "location": "Europe without Switzerland and Austria", "reference product": "steel, low-alloyed"}),
                    (("transport, freight, lorry >32 metric ton, EURO4", "RER", ()),
                     {"name": "transport, freight, lorry >32 metric ton, EURO4", "location": "RER",
                      "reference product": "transport, freight, lorry >32 metric ton, EURO4"}),
                    (("transport, freight, lorry 16-32 metric ton, EURO4", "RER", ()),
                     {"name": "transport, freight, lorry 16-32 metric ton, EURO4", "location": "RER",
                      "reference product": "transport, freight, lorry 16-32 metric ton, EURO4"}),
                    (("treatment of average incineration residue, residual material landfill", "RoW", ()),
                     {"name": "treatment of average incineration residue, residual material landfill",
                      "location": "RoW", "reference product": "average incineration residue"}),
                    (("treatment of hard coal ash, residual material landfill", "RoW", ()),
                     {"name": "treatment of hard coal ash, residual material landfill", "location": "RoW",
                      "reference product": "average incineration residue"}),
                    (("treatment of hazardous waste, hazardous waste incineration", "CH",
                      "Disposal, hazardous waste, 25% water, to hazardous waste incineration/CH U"),
                     {"name": "treatment of hazardous waste, hazardous waste incineration", "location": "CH",
                      "reference product": "hazardous waste, for incineration"}),
                    (("treatment of hazardous waste, hazardous waste incineration", "CH", ()),
                     {"name": "treatment of hazardous waste, hazardous waste incineration", "location": "CH",
                      "reference product": "hazardous waste, for incineration"}),
                    (("treatment of inert waste, inert material landfill", "CH",
                      "Disposal, inert waste, 5% water, to inert material landfill"),
                     {"name": "treatment of inert waste, inert material landfill", "location": "CH",
                      "reference product": "inert waste, for final disposal"}),
                    (("treatment of inert waste, inert material landfill", "CH", ()),
                     {"name": "treatment of inert waste, inert material landfill", "location": "CH",
                      "reference product": "inert waste, for final disposal"}),
                    (("treatment of lignite ash, opencast refill", "RoW", ()),
                     {"name": "treatment of lignite ash, opencast refill", "location": "RoW",
                      "reference product": "lignite ash"}),
                    (("treatment of municipal solid waste, incineration", "CH", ()),
                     {"name": "treatment of municipal solid waste, incineration", "location": "CH",
                      "reference product": "municipal solid waste"}),
                    (("treatment of residue from cooling tower, sanitary landfill", "CH", ()),
                     {"name": "treatment of residue from cooling tower, sanitary landfill", "location": "CH",
                      "reference product": "residue from cooling tower"}),
                    (("treatment of spent solvent mixture, hazardous waste incineration", "CH", ()),
                     {"name": "treatment of spent solvent mixture, hazardous waste incineration", "location": "CH",
                      "reference product": "spent solvent mixture"}),
                    (("treatment of waste mineral oil, hazardous waste incineration", "CH", ()),
                     {"name": "treatment of waste mineral oil, hazardous waste incineration", "location": "CH",
                      "reference product": "waste mineral oil"}),
                    (("treatment of waste wood, untreated, sanitary landfill", "CH", ()),
                     {"name": "treatment of waste wood, untreated, sanitary landfill", "location": "CH",
                      "reference product": "waste wood, untreated"}),
                    (("zinc-lead mine operation", "GLO", "zinc concentrate"),
                     {"name": "treatment of sulfidic tailings, from zinc-lead mine operation, tailings impoundment",
                      "location": "CN", "reference product": "sulfidic tailings, from zinc-lead mine operation"}),
                ],
            }

class BaseInventoryImport:
    """
    Base class for inventories that are to be merged with the ecoinvent database.

    :ivar db: the target database for the import (the Ecoinvent database),
              unpacked to a list of dicts
    :vartype db: list
    :ivar version: the target Ecoinvent database version
    :vartype version: str
    """

    def __init__(self, database, version, path):
        """Create a :class:`BaseInventoryImport` instance.

        :param list database: the target database for the import (the Ecoinvent database),
                              unpacked to a list of dicts
        :param version: the version of the target database ("3.5", "3.6", "3.7", "3.7.1")
        :type version: str
        :param path: Path to the imported inventory.
        :type path: str or Path

        """
        self.db = database
        self.db_code = [x["code"] for x in self.db]
        self.db_names = [
            (x["name"], x["reference product"], x["location"]) for x in self.db
        ]
        self.version = version
        self.biosphere_dict = self.get_biosphere_code()

        path = Path(path)

        if path != Path("."):
            if not path.is_file():
                raise FileNotFoundError(
                    "The inventory file {} could not be found.".format(path)
                )

        self.path = path
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        """Load an inventory from a specified path.

        Sets the :attr:`import_db` attribute.

        :param str path: Path to the inventory file
        :returns: Nothing.

        """
        pass

    def prepare_inventory(self):
        """Prepare the inventory for the merger with Ecoinvent.

        Modifies :attr:`import_db` in-place.

        :returns: Nothing

        """
        pass

    def check_for_duplicates(self):
        """
        Check whether the inventories to be imported are not
        already in the source database.
        """

        # print if we find datasets that already exist
        already_exist = [
            (x["name"], x["reference product"], x["location"])
            for x in self.import_db.data
            if x["code"] in self.db_code
        ]

        already_exist.extend(
            [
                (x["name"], x["reference product"], x["location"])
                for x in self.import_db.data
                if (x["name"], x["reference product"], x["location"]) in self.db_names
            ]
        )

        if len(already_exist) > 0:
            print(
                "The following datasets to import already exist in the source database. They will not be imported"
            )
            t = PrettyTable(["Name", "Reference product", "Location", "File"])
            for ds in already_exist:
                t.add_row([ds[0][:50], ds[1][:30], ds[2], self.path.name])

            print(t)

        self.import_db.data = [
            x for x in self.import_db.data if x["code"] not in self.db_code
        ]
        self.import_db.data = [
            x
            for x in self.import_db.data
            if (x["name"], x["reference product"], x["location"]) not in self.db_names
        ]

    def merge_inventory(self):
        """Prepare :attr:`import_db` and merge the inventory to the ecoinvent :attr:`db`.

        Calls :meth:`prepare_inventory`. Changes the :attr:`db` attribute.

        :returns: Nothing

        """
        self.prepare_inventory()
        self.db.extend(self.import_db)

    def search_exchanges(self, srchdict):
        """Search :attr:`import_db` by field values.

        :param dict srchdict: dict with the name of the fields and the values.
        :returns: the activities with the exchanges that match the search.
        :rtype: dict

        """
        results = []
        for act in self.import_db.data:
            for ex in act["exchanges"]:
                if len(srchdict.items() - ex.items()) == 0:
                    results.append(act)
        return results

    def search_missing_field(self, field):
        """Find exchanges and activities that do not contain a specific field
        in :attr:`imort_db`

        :param str field: label of the field to search for.
        :returns: a list of dictionaries, activities and exchanges
        :rtype: list

        """
        results = []
        for act in self.import_db.data:
            if field not in act:
                results.append(act)
            for ex in act["exchanges"]:
                if ex["type"] == "technosphere" and field not in ex:
                    results.append(ex)
        return results

    @staticmethod
    def get_biosphere_code():
        """
        Retrieve a dictionary with biosphere flow names and uuid codes.

        :returns: dictionary with biosphere flow names as keys and uuid code as values
        :rtype: dict
        """

        if not FILEPATH_BIOSPHERE_FLOWS.is_file():
            raise FileNotFoundError(
                "The dictionary of biosphere flows could not be found."
            )

        csv_dict = {}

        with open(FILEPATH_BIOSPHERE_FLOWS) as f:
            input_dict = csv.reader(f, delimiter=";")
            for row in input_dict:
                csv_dict[(row[0], row[1], row[2], row[3])] = row[4]

        return csv_dict

    def add_product_field_to_exchanges(self):
        """Add the `product` key to the production and
        technosphere exchanges in :attr:`import_db`.
        Also add `code` field if missing.

        For production exchanges, use the value of the `reference_product` field.
        For technosphere exchanges, search the activities in :attr:`import_db` and
        use the reference product. If none is found, search the Ecoinvent :attr:`db`.
        Modifies the :attr:`import_db` attribute in place.

        :raises IndexError: if no corresponding activity (and reference product) can be found.

        """
        # Add a `product` field to the production exchange
        for x in self.import_db.data:
            for y in x["exchanges"]:
                if y["type"] == "production":
                    if "product" not in y:
                        y["product"] = x["reference product"]

                    if y["name"] != x["name"]:
                        y["name"] = x["name"]

        # Add a `product` field to technosphere exchanges
        for x in self.import_db.data:
            for y in x["exchanges"]:
                if y["type"] == "technosphere":
                    # Check if the field 'product' is present
                    if not "product" in y:
                        y["product"] = self.correct_product_field(y)

                    # If a 'reference product' field is present, we make sure
                    # it matches with the new 'product' field
                    if "reference product" in y:
                        try:
                            assert y["product"] == y["reference product"]
                        except AssertionError:
                            y["product"] = self.correct_product_field(y)

        # Add a `code` field if missing
        for x in self.import_db.data:
            if "code" not in x:
                x["code"] = str(uuid.uuid4().hex)

    def correct_product_field(self, exc):
        """
        Find the correct name for the `product` field of the exchange
        :param exc: a dataset exchange
        :return: name of the product field of the exchange
        :rtype: str
        """
        # Look first in the imported inventories
        candidate = next(ws.get_many(
            self.import_db.data,
            ws.equals("name", exc["name"]),
            ws.equals("location", exc["location"]),
            ws.equals("unit", exc["unit"])
        ), None)
        # possibles = [
        #     a["reference product"]
        #     for a in self.import_db.data
        #     if a["name"] == exc["name"]
        #     and a["location"] == exc["location"]
        #     and a["unit"] == exc["unit"]
        # ]

        # If not, look in the ecoinvent inventories
        if candidate is None:
            candidate = next(ws.get_many(
                self.db,
                ws.equals("name", exc["name"]),
                ws.equals("location", exc["location"]),
                ws.equals("unit", exc["unit"])
            ), None)

        if candidate is not None:
            return candidate["reference product"]
        else:
            raise IndexError(
                "An inventory exchange in {} cannot be linked to the biosphere or the ecoinvent database: {}".format(
                    self.import_db.db_name, exc
                )
            )

    def add_biosphere_links(self, delete_missing=False):
        """Add links for biosphere exchanges to :attr:`import_db`

        Modifies the :attr:`import_db` attribute in place.
        """
        for x in self.import_db.data:
            for y in x["exchanges"]:
                if y["type"] == "biosphere":
                    if isinstance(y["categories"], str):
                        y["categories"] = tuple(y["categories"].split("::"))
                    if len(y["categories"]) > 1:
                        try:
                            y["input"] = (
                                "biosphere3",
                                self.biosphere_dict[
                                    (
                                        y["name"],
                                        y["categories"][0],
                                        y["categories"][1],
                                        y["unit"],
                                    )
                                ],
                            )
                        except KeyError:
                            if delete_missing:
                                y["flag_deletion"] = True
                            else:
                                raise
                    else:
                        try:
                            y["input"] = (
                                "biosphere3",
                                self.biosphere_dict[
                                    (
                                        y["name"],
                                        y["categories"][0],
                                        "unspecified",
                                        y["unit"],
                                    )
                                ],
                            )
                        except KeyError:
                            if delete_missing:
                                y["flag_deletion"] = True
                            else:
                                raise
            x["exchanges"] = [ex for ex in x["exchanges"] if "flag_deletion" not in ex]

    def remove_ds_and_modifiy_exchanges(self, name, ex_data):
        """
        Remove an activity dataset from :attr:`import_db` and replace the corresponding
        technosphere exchanges by what is given as second argument.

        :param str name: name of activity to be removed
        :param dict ex_data: data to replace the corresponding exchanges

        :returns: Nothing
        """

        self.import_db.data = [
            act for act in self.import_db.data if not act["name"] == name
        ]

        for act in self.import_db.data:
            for ex in act["exchanges"]:
                if ex["type"] == "technosphere" and ex["name"] == name:
                    ex.update(ex_data)
                    # make sure there is no existing link
                    if "input" in ex:
                        del ex["input"]

            # Delete any field that does not have information
            for key in act:
                if act[key] is None:
                    act.pop(key)

class CarmaCCSInventory(BaseInventoryImport):
    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        if self.version == "3.6":
            # apply some updates to comply with ei 3.6
            new_technosphere_data = EI_37_36_MIGRATION_MAP

            Migration("migration_36").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5 to 3.6",
            )
            self.import_db.migrate("migration_36")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()

        # Check for duplicates
        self.check_for_duplicates()

class DACInventory(BaseInventoryImport):
    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        if self.version == "3.6":
            # apply some updates to go from ei3.7 to ei3.6
            new_technosphere_data = EI_37_36_MIGRATION_MAP

            Migration("migration_36").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.7 to 3.5",
            )
            self.import_db.migrate("migration_36")

        if self.version == "3.5":
            # apply some updates to go from ei3.7 to ei3.5
            new_technosphere_data = EI_37_35_MIGRATION_MAP

            Migration("migration_35").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.7 to 3.6",
            )
            self.import_db.migrate("migration_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()

        # Add carbon storage for CCS technologies
        print("Add fossil carbon dioxide storage for CCS technologies.")
        self.add_negative_CO2_flows_for_biomass_CCS()

        # Check for duplicates
        self.check_for_duplicates()

    def add_negative_CO2_flows_for_biomass_CCS(self):
        """
        Rescale the amount of all exchanges of carbon dioxide, non-fossil by a factor -9 (.9/-.1),
        to account for sequestered CO2.

        All CO2 capture and storage in the Carma datasets is assumed to be 90% efficient.
        Thus, we can simply find out what the new CO2 emission is and then we know how much gets stored in the ground.
        It's very important that we ONLY do this for biomass CCS plants, as only they will have negative emissions!

        We also rename the emission to 'Carbon dioxide, from soil or biomass stock' so that it is properly
        characterized by IPCC's GWP100a method.

        Modifies in place (does not return anything).

        """
        for ds in ws.get_many(
            self.db, ws.contains("name", "storage"), ws.equals("database", "Carma CCS")
        ):
            for exc in ws.biosphere(
                ds, ws.equals("name", "Carbon dioxide, non-fossil")
            ):
                wurst.rescale_exchange(exc, (0.9 / -0.1), remove_uncertainty=True)

class BiofuelInventory(BaseInventoryImport):
    """
    Biofuel datasets from the master thesis of Francesco Cozzolino (2018).
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):

        # migration for ei 3.7
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        # Migrations for 3.6
        if self.version == "3.6":
            migrations = EI_37_36_MIGRATION_MAP

            Migration("biofuels_ecoinvent_36").write(
                migrations,
                description="Change technosphere names due to change from 3.5 to 3.6",
            )
            self.import_db.migrate("biofuels_ecoinvent_36")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()

        # Check for duplicates
        self.check_for_duplicates()

class HydrogenInventory(BaseInventoryImport):
    """
    Hydrogen datasets from the ELEGANCY project (2019).
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        # migration for ei 3.7
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        # Migrations for 3.5
        if self.version == "3.5":
            migrations = EI_37_35_MIGRATION_MAP

            Migration("hydrogen_ecoinvent_35").write(
                migrations,
                description="Change technosphere names due to change from 3.5 to 3.6",
            )
            self.import_db.migrate("hydrogen_ecoinvent_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()

        # Check for duplicates
        self.check_for_duplicates()

class HydrogenBiogasInventory(BaseInventoryImport):
    """
    Hydrogen datasets from the ELEGANCY project (2019).
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        # migration for ei 3.7
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        # Migrations for 3.5
        if self.version == "3.5":
            migrations = EI_37_35_MIGRATION_MAP

            Migration("hydrogen_ecoinvent_35").write(
                migrations,
                description="Change technosphere names due to change from 3.5 to 3.6",
            )
            self.import_db.migrate("hydrogen_ecoinvent_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()

        # Check for duplicates
        self.check_for_duplicates()

class BiogasInventory(BaseInventoryImport):
    """
    Biogas datasets from the SCCER project (2019).
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        # migration for ei 3.7
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        # Migrations for 3.5
        if self.version == "3.5":
            migrations = EI_37_35_MIGRATION_MAP

            Migration("biogas_ecoinvent_35").write(
                migrations,
                description="Change technosphere names due to change from 3.5 to 3.6",
            )
            self.import_db.migrate("biogas_ecoinvent_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()

        # Check for duplicates
        self.check_for_duplicates()

class SyngasInventory(BaseInventoryImport):
    """
    Synthetic fuel datasets from the PSI project (2019).
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        # migration for ei 3.7
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        # migration for ei 3.5
        if self.version == "3.5":
            migrations = EI_37_35_MIGRATION_MAP

            Migration("syngas_ecoinvent_35").write(
                migrations,
                description="Change technosphere names due to change from 3.6 to 3.5",
            )
            self.import_db.migrate("syngas_ecoinvent_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()

class SynfuelInventory(BaseInventoryImport):
    """
    Synthetic fuel datasets from the PSI project (2019).
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        # migration for ei 3.7
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        if self.version == "3.5":
            migrations = EI_37_35_MIGRATION_MAP

            Migration("syngas_ecoinvent_35").write(
                migrations,
                description="Change technosphere names due to change from 3.6 to 3.5",
            )
            self.import_db.migrate("syngas_ecoinvent_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()
        # Check for duplicates
        self.check_for_duplicates()

class GeothermalInventory(BaseInventoryImport):
    """
    Geothermal heat production, adapted from geothermal power production dataset from ecoinvent 3.6.
.
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        # migration for ei 3.7
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")
        self.add_biosphere_links()
        self.add_product_field_to_exchanges()
        # Check for duplicates
        self.check_for_duplicates()

class LPGInventory(BaseInventoryImport):
    """
    Liquified Petroleum Gas (LPG) from methanol distillation, the PSI project (2020), with hydrogen from electrolysis.
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):
        # migration for ei 3.7
        if self.version in ["3.7", "3.7.1"]:
            # apply some updates to comply with ei 3.7
            new_technosphere_data = EI_37_MIGRATION_MAP

            Migration("migration_37").write(
                new_technosphere_data,
                description="Change technosphere names due to change from 3.5/3.6 to 3.7",
            )
            self.import_db.migrate("migration_37")

        # Migrations for 3.5
        if self.version == "3.5":
            migrations = EI_37_35_MIGRATION_MAP

            Migration("LPG_ecoinvent_35").write(
                migrations,
                description="Change technosphere names due to change from 3.5 to 3.6",
            )
            self.import_db.migrate("LPG_ecoinvent_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()
        # Check for duplicates
        self.check_for_duplicates()

class VariousVehicles(BaseInventoryImport):
    """
    Imports various future vehicles' inventories (two-wheelers, buses, trams, etc.).
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):

        # Migrations for 3.6
        if self.version == "3.6":
            migrations = EI_37_36_MIGRATION_MAP

            Migration("ecoinvent_36").write(
                migrations,
                description="Change technosphere names due to change from 3.7 to 3.6",
            )
            self.import_db.migrate("ecoinvent_36")


        # Migrations for 3.5
        if self.version == "3.5":
            migrations = EI_37_35_MIGRATION_MAP

            Migration("ecoinvent_35").write(
                migrations,
                description="Change technosphere names due to change from 3.5 to 3.6",
            )
            self.import_db.migrate("ecoinvent_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()
        # Check for duplicates
        self.check_for_duplicates()

class AdditionalInventory(BaseInventoryImport):
    """
    Import additional inventories, if any.
    """

    def __init__(self, database, version, path):
        super().__init__(database, version, path)
        self.import_db = self.load_inventory(path)

    def load_inventory(self, path):
        return ExcelImporter(path)

    def prepare_inventory(self):

        # Migrations for 3.6
        if self.version == "3.6":
            migrations = EI_37_36_MIGRATION_MAP

            Migration("ecoinvent_36").write(
                migrations,
                description="Change technosphere names due to change from 3.7 to 3.6",
            )
            self.import_db.migrate("ecoinvent_36")

        # Migrations for 3.5
        if self.version == "3.5":
            migrations = EI_37_35_MIGRATION_MAP

            Migration("migration_35").write(
                migrations,
                description="Change technosphere names due to change from 3.7 to 3.5",
            )
            self.import_db.migrate("migration_35")

        self.add_biosphere_links()
        self.add_product_field_to_exchanges()
        # Check for duplicates
        self.check_for_duplicates()

class CarculatorInventory(BaseInventoryImport):
    """
    Car models from the carculator project, https://github.com/romainsacchi/carculator
    """

    def __init__(self, database, version, path, fleet_file, model, pathway, year, regions, filters=None):
        self.db_year = year
        self.model = model
        self.geomap = Geomap(model=self.model)
        self.regions = regions
        self.fleet_file = fleet_file
        self.filter = ["fleet average"]

        if filters:
            self.filter.extend(filters)

        # IAM output file extension differs between REMIND and IMAGE
        ext = ".mif" if model == "remind" else ".xls"

        self.source_file = path / (model + "_" + pathway + ext)

        if not self.source_file.is_file():
            raise FileNotFoundError("For some reason, the file {} is not accessible.".format(
                self.source_file
            ))

        super().__init__(database, version, Path("."))

    def load_inventory(self, path):
        """Create `carculator` fleet average inventories for a given range of years.
        """

        cip = carculator.CarInputParameters()
        cip.static()
        _, array = carculator.fill_xarray_from_input_parameters(cip)

        array = array.interp(
            year=np.arange(1996, self.db_year + 1), kwargs={"fill_value": "extrapolate"}
        )
        cm = carculator.CarModel(array, cycle="WLTC 3.4")
        cm.set_all()

        fleet_array = carculator.create_fleet_composition_from_IAM_file(
            self.fleet_file
        )

        for r, region in enumerate(self.regions):

            if region == "World":
                region = [r for r in self.regions if r != "World"]

            # The fleet file has REMIND region
            # Hence, if we use IMAGE, we need to convert
            # the region names
            # which is something `iam_to_GAINS_region()` does.
            if self.model == "remind":
                reg_fleet = region
            if self.model == "image":
                reg_fleet = self.geomap.iam_to_GAINS_region(region)

            fleet = fleet_array.sel(IAM_region=reg_fleet,
                                    vintage_year=np.arange(1996, self.db_year + 1)
                                    ).interp(variable=np.arange(1996, self.db_year + 1))


            years = []
            for y in np.arange(1996, self.db_year):
                if y in fleet.vintage_year:
                    if fleet.sel(vintage_year=y,
                                 variable=self.db_year).sum(dim=["size", "powertrain"]) != 0:
                        years.append(y)
            years.append(self.db_year)

            scope = {
                "powertrain": fleet.sel(vintage_year=years).powertrain.values,
                "size": fleet.sel(vintage_year=years).coords["size"].values,
                "year": years,
                "fu": {"fleet": fleet.sel(vintage_year=years), "unit": "vkm"},
            }

            mix = carculator.extract_electricity_mix_from_IAM_file(
                model=self.model, fp=self.source_file, IAM_region=region, years=scope["year"]
            )


            fuel_shares = carculator.extract_biofuel_shares_from_IAM(
                model=self.model, fp=self.source_file, IAM_region=region, years=scope["year"],
                allocate_all_synfuel=True
            )

            bc = {
                "custom electricity mix": mix,
                "country": region,
                "fuel blend": {
                    "petrol": {
                        "primary fuel": {
                            "type": "petrol",
                            "share": fuel_shares.sel(fuel_type="liquid - fossil").values
                            if "liquid - fossil" in fuel_shares.fuel_type.values
                            else np.ones_like(years),
                        },
                        "secondary fuel": {
                            "type": "bioethanol - wheat straw",
                            "share": fuel_shares.sel(
                                fuel_type="liquid - biomass"
                            ).values
                            if "liquid - biomass" in fuel_shares.fuel_type.values
                            else np.zeros_like(years),
                        },
                        "tertiary fuel": {
                            "type": "synthetic gasoline",
                            "share": fuel_shares.sel(
                                fuel_type="liquid - synfuel"
                            ).values
                            if "liquid - synfuel" in fuel_shares.fuel_type.values
                            else np.zeros_like(years),
                        },
                    },
                    "diesel": {
                        "primary fuel": {
                            "type": "diesel",
                            "share": fuel_shares.sel(fuel_type="liquid - fossil").values
                            if "liquid - fossil" in fuel_shares.fuel_type.values
                            else np.ones_like(years),
                        },
                        "secondary fuel": {
                            "type": "biodiesel - cooking oil",
                            "share": fuel_shares.sel(
                                fuel_type="liquid - biomass"
                            ).values
                            if "liquid - biomass" in fuel_shares.fuel_type.values
                            else np.zeros_like(years),
                        },
                        "tertiary fuel": {
                            "type": "synthetic diesel",
                            "share": fuel_shares.sel(
                                fuel_type="liquid - synfuel"
                            ).values
                            if "liquid - synfuel" in fuel_shares.fuel_type.values
                            else np.zeros_like(years),
                        }
                    },
                    "cng": {
                        "primary fuel": {
                            "type": "cng",
                            "share": fuel_shares.sel(fuel_type="gas - fossil").values
                            if "gas - fossil" in fuel_shares.fuel_type.values
                            else np.ones_like(years),
                        },
                        "secondary fuel": {
                            "type": "biogas - biowaste",
                            "share": fuel_shares.sel(fuel_type="gas - biomass").values
                            if "gas - biomass" in fuel_shares.fuel_type.values
                            else np.zeros_like(years),
                        },
                    },
                    "hydrogen": {
                        "primary fuel": {
                            "type": "electrolysis",
                            "share": np.ones_like(years),
                        }
                    },
                },
            }

            ic = carculator.InventoryCalculation(
                cm.array, scope=scope, background_configuration=bc
            )

            # if self.fleet_file:
            #
            #     i = ic.export_lci_to_bw(presamples=False,
            #                             ecoinvent_version=str(self.version),
            #                             create_vehicle_datasets=False)
            #
            # else:
            i = ic.export_lci_to_bw(presamples=False,
                                    ecoinvent_version=str(self.version),
                                    create_vehicle_datasets=False)


            # filter out cars if anything given in `self.filter`
            i.data = [x for x in i.data if "transport, passenger car" not in x["name"]
                      or (any(y.lower() in x["name"].lower() for y in self.filter) and str(self.db_year) in x["name"])]

            # we need to remove the electricity inputs in the fuel markets
            # that are typically added when synfuels are part of the blend
            for x in i.data:
                if "fuel supply for " in x["name"]:
                    for e in x["exchanges"]:
                        if "electricity market for " in e["name"]:
                            x["exchanges"].remove(e)

            if r == 0:
                import_db = i
            else:
                # remove duplicate items if iterating over several regions
                i.data = [
                    x
                    for x in i.data
                    if (x["name"], x["location"])
                       not in [(z["name"], z["location"]) for z in import_db.data]
                ]
                import_db.data.extend(i.data)

        return import_db


    def prepare_inventory(self):
        self.add_biosphere_links(delete_missing=True)
        self.add_product_field_to_exchanges()
        # Check for duplicates
        self.check_for_duplicates()

    def merge_inventory(self):
        self.prepare_inventory()

        activities_to_remove = [
            "transport, passenger car",
            "market for passenger car",
            "market for transport, passenger car"
        ]

        self.db = [x for x in self.db if not any(y for y in activities_to_remove if y in x["name"])]
        self.db.extend(self.import_db)

        exchanges_to_modify = [
            'market for transport, passenger car, large size, petol, EURO 4',
            'market for transport, passenger car',
            'market for transport, passenger car, large size, petrol, EURO 3',
            'market for transport, passenger car, large size, diesel, EURO 4',
            'market for transport, passenger car, large size, diesel, EURO 5'
        ]
        for ds in self.db:
            excs = (exc for exc in ds["exchanges"]
                    if exc["name"] in exchanges_to_modify
                    and exc["type"] == "technosphere")

            for exc in excs:

                try:

                    new_supplier = ws.get_one(
                        self.db,
                        *[
                            ws.contains("name", "transport, passenger car, fleet average, all powertrains"),
                            ws.equals("location", self.geomap.ecoinvent_to_iam_location(ds["location"])),
                            ws.contains("reference product", "transport")
                        ]
                    )

                    exc["name"] = new_supplier["name"]
                    exc["location"] = new_supplier["location"]
                    exc["product"] = new_supplier["reference product"]
                    exc["unit"] = new_supplier["unit"]

                except ws.NoResults:

                    new_supplier = ws.get_one(
                        self.db,
                        *[
                            ws.contains("name", "transport, passenger car, fleet average, all powertrains"),
                            ws.equals("location", self.regions[0]),
                            ws.contains("reference product", "transport")
                        ]
                    )

                    exc["name"] = new_supplier["name"]
                    exc["location"] = new_supplier["location"]
                    exc["product"] = new_supplier["reference product"]
                    exc["unit"] = new_supplier["unit"]

        return self.db


class TruckInventory(BaseInventoryImport):
    """
    Car models from the carculator project, https://github.com/romainsacchi/carculator
    """

    def __init__(self, database, version, path, fleet_file, model, pathway, year, regions, filters=None):

        self.db_year = year
        self.model = model
        self.geomap = Geomap(model=self.model)
        self.regions = regions
        self.fleet_file = fleet_file
        self.filter = ["fleet average"]

        if filters:
            self.filter.extend(filters)

        # IAM output file extension differs between REMIND and IMAGE
        ext = ".mif" if model == "remind" else ".xls"

        self.source_file = path / (model + "_" + pathway + ext)

        if not self.source_file.is_file():
            raise FileNotFoundError("For some reason, the file {} is not accessible.".format(
                self.source_file
            ))

        super().__init__(database, version, Path("."))

    def load_inventory(self, path):
        """Create `carculator_truck` fleet average inventories for a given range of years.
        """

        fleet_array = carculator_truck.create_fleet_composition_from_IAM_file(
            self.fleet_file
        )

        fleet = fleet_array.sel(IAM_region="EUR").interp(variable=np.arange(1996, self.db_year + 1))



        years = []
        for y in np.arange(2010, self.db_year):
            if y in fleet.vintage_year:
                if fleet.sel(vintage_year=y,
                             variable=self.db_year).sum(dim=["size", "powertrain"]) != 0:
                    years.append(y)
        years.append(self.db_year)

        scope = {
            "powertrain": fleet.sel(vintage_year=years).powertrain.values,
            "size": fleet.sel(vintage_year=years).coords["size"].values,
            "fu": {"fleet": fleet.sel(vintage_year=years), "unit": "tkm"},
        }


        tip = carculator_truck.TruckInputParameters()
        tip.static()
        _, array = carculator_truck.fill_xarray_from_input_parameters(tip,
                                                                      scope=scope
                                                                      )

        array = array.interp(
            year=years, kwargs={"fill_value": "extrapolate"}
        )
        tm = carculator_truck.TruckModel(array, cycle="Regional delivery", country="CH")
        tm.set_all()



        for r, region in enumerate(self.regions):

            if region == "World":
                region = [r for r in self.regions if r != "World"]

            # The fleet file has REMIND region
            # Hence, if we use IMAGE, we need to convert
            # the region names
            # which is something `iam_to_GAINS_region()` does.
            if self.model == "remind":
                reg_fleet = region
            if self.model == "image":
                reg_fleet = self.geomap.iam_to_GAINS_region(region)

            fleet = fleet_array.sel(IAM_region=reg_fleet).interp(variable=np.arange(1996, self.db_year + 1))

            years = []
            for y in np.arange(2010, self.db_year):
                if y in fleet.vintage_year:
                    if fleet.sel(vintage_year=y,
                                 variable=self.db_year).sum(dim=["size", "powertrain"]) != 0:
                        years.append(y)
            years.append(self.db_year)

            scope = {
                "powertrain": fleet.sel(vintage_year=years).powertrain.values,
                "size": fleet.sel(vintage_year=years).coords["size"].values,
                "year": years,
                "fu": {"fleet": fleet.sel(vintage_year=years), "unit": "tkm"},
            }

            mix = carculator_truck.extract_electricity_mix_from_IAM_file(
                model=self.model, fp=self.source_file, IAM_region=region, years=scope["year"]
            )

            fuel_shares = carculator_truck.extract_biofuel_shares_from_IAM(
                model=self.model, fp=self.source_file, IAM_region=region, years=scope["year"],
                allocate_all_synfuel=True
            )

            bc = {
                "custom electricity mix": mix,
                "country": region,
                "fuel blend": {
                    "diesel": {
                        "primary fuel": {
                            "type": "diesel",
                            "share": fuel_shares.sel(fuel_type="liquid - fossil").values
                            if "liquid - fossil" in fuel_shares.fuel_type.values
                            else np.ones_like(years),
                        },
                        "secondary fuel": {
                            "type": "biodiesel - cooking oil",
                            "share": fuel_shares.sel(
                                fuel_type="liquid - biomass"
                            ).values
                            if "liquid - biomass" in fuel_shares.fuel_type.values
                            else np.zeros_like(years),
                        },
                        "tertiary fuel": {
                            "type": "synthetic diesel",
                            "share": fuel_shares.sel(
                                fuel_type="liquid - synfuel"
                            ).values
                            if "liquid - synfuel" in fuel_shares.fuel_type.values
                            else np.zeros_like(years),
                        }
                    },
                    "cng": {
                        "primary fuel": {
                            "type": "cng",
                            "share": fuel_shares.sel(fuel_type="gas - fossil").values
                            if "gas - fossil" in fuel_shares.fuel_type.values
                            else np.ones_like(years),
                        },
                        "secondary fuel": {
                            "type": "biogas - biowaste",
                            "share": fuel_shares.sel(fuel_type="gas - biomass").values
                            if "gas - biomass" in fuel_shares.fuel_type.values
                            else np.zeros_like(years),
                        },
                    },
                    "hydrogen": {
                        "primary fuel": {
                            "type": "electrolysis",
                            "share": np.ones_like(years),
                        }
                    },
                },
            }

            ic = carculator_truck.InventoryCalculation(tm,
                                                      scope=scope,
                                                      background_configuration=bc,
                                                       )

            i = ic.export_lci_to_bw(presamples=False,
                                    ecoinvent_version=str(self.version),
                                    create_vehicle_datasets=False
                                    )


            # filter out trucks if anything given in `self.filter`
            i.data = [x for x in i.data if "transport, " not in x["name"]
                      or (any(y.lower() in x["name"].lower() for y in self.filter) and str(self.db_year) in x["name"])]


            # we need to remove the electricity inputs in the fuel markets
            # that are typically added when synfuels are part of the blend
            for x in i.data:
                if "fuel supply for " in x["name"]:
                    for e in x["exchanges"]:
                        if "electricity market for " in e["name"]:
                            x["exchanges"].remove(e)

            if r == 0:
                import_db = i
            else:
                # remove duplicate items if iterating over several regions
                i.data = [
                    x
                    for x in i.data
                    if (x["name"], x["location"])
                       not in [(z["name"], z["location"]) for z in import_db.data]
                ]
                import_db.data.extend(i.data)

        return import_db

    def prepare_inventory(self):
        self.add_biosphere_links(delete_missing=True)
        self.add_product_field_to_exchanges()
        # Check for duplicates
        self.check_for_duplicates()

    def merge_inventory(self):
        self.prepare_inventory()

        activities_to_remove = [
            "transport, freight, lorry",
        ]

        self.db = [x for x in self.db if not any(y for y in activities_to_remove if y in x["name"])]
        self.db.extend(self.import_db)


        for ds in self.db:
            excs = (exc for exc in ds["exchanges"]
                    if "transport, freight, lorry" in exc["name"]
                    and exc["type"] == "technosphere")

            for exc in excs:

                try:

                    new_supplier = ws.get_one(
                        self.db,
                        *[
                            ws.contains("name", "transport, medium and heavy duty truck, fleet average, all powertrains"),
                            ws.equals("location", self.geomap.ecoinvent_to_iam_location(ds["location"])),
                            ws.contains("reference product", "transport")
                        ]
                    )

                    exc["name"] = new_supplier["name"]
                    exc["location"] = new_supplier["location"]
                    exc["product"] = new_supplier["reference product"]
                    exc["unit"] = new_supplier["unit"]

                except ws.NoResults:

                    new_supplier = ws.get_one(
                        self.db,
                        *[
                            ws.contains("name", "transport, medium and heavy duty truck, fleet average, all powertrains"),
                            ws.equals("location", self.regions[0]),
                            ws.contains("reference product", "transport")
                        ]
                    )

                    exc["name"] = new_supplier["name"]
                    exc["location"] = new_supplier["location"]
                    exc["product"] = new_supplier["reference product"]
                    exc["unit"] = new_supplier["unit"]

        return self.db
