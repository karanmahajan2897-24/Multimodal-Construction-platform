"""
Demo / fallback data for all modules when no API key is provided.
"""

DEMO_SAFETY_AUDIT = {
    "safety_score": 67,
    "overall_status": "NEEDS IMPROVEMENT",
    "analysis_summary": "Site inspection reveals partial PPE compliance. Several workers missing critical head and foot protection. Immediate corrective action required before resuming high-risk operations.",
    "ppe_detection": {
        "helmets": {"status": "PARTIAL", "compliant_count": 4, "total_workers": 6, "notes": "2 workers missing helmets near scaffolding zone"},
        "high_vis_vests": {"status": "COMPLIANT", "compliant_count": 6, "total_workers": 6, "notes": "All workers wearing high-visibility vests"},
        "steel_toe_boots": {"status": "NON-COMPLIANT", "compliant_count": 2, "total_workers": 6, "notes": "4 workers observed in non-safety footwear"},
        "safety_harnesses": {"status": "PARTIAL", "compliant_count": 1, "total_workers": 2, "notes": "1 worker at elevation without harness"}
    },
    "site_hazards": [
        {
            "hazard": "Workers at elevation without fall protection harness",
            "severity": "Critical",
            "osha_standard": "OSHA 1926.502",
            "is_standard": "IS 3696 Part 1",
            "remedy": "Immediately halt work at elevation. Issue and inspect fall arrest harnesses. Conduct toolbox talk on fall protection before resuming."
        },
        {
            "hazard": "Missing hard hats near active scaffolding",
            "severity": "High",
            "osha_standard": "OSHA 1926.100",
            "is_standard": "IS 2925",
            "remedy": "Stop work order for non-compliant workers. Issue Class E helmets. Designate PPE checkpoint at site entry."
        },
        {
            "hazard": "Non-safety footwear in active construction zone",
            "severity": "High",
            "osha_standard": "OSHA 1926.96",
            "is_standard": "IS 15298",
            "remedy": "Enforce no-entry policy without steel-toe boots. Provide temporary footwear from site PPE store."
        },
        {
            "hazard": "Loose materials on scaffolding platform edge",
            "severity": "Medium",
            "osha_standard": "OSHA 1926.502(j)",
            "is_standard": "IS 3696",
            "remedy": "Install toe boards on all scaffold edges. Clear loose materials immediately and secure with netting."
        },
        {
            "hazard": "Inadequate signage around deep excavation zone",
            "severity": "Medium",
            "osha_standard": "OSHA 1926.651",
            "is_standard": "IS 456",
            "remedy": "Install barricades and warning signs at 2m perimeter. Daily inspection of excavation walls required."
        }
    ]
}

DEMO_CRACK_ANALYSIS = {
    "defect_type": "Settlement Crack",
    "confidence": 82,
    "crack_width_mm": 3.2,
    "length_estimate_cm": 45,
    "depth_assessment": "Medium - penetrates plaster into masonry",
    "location_description": "Diagonal crack running from window corner at approximately 45°, consistent with differential foundation settlement",
    "root_causes": [
        "Differential settlement of foundation due to uneven soil bearing capacity",
        "Inadequate foundation depth or poor compaction during construction",
        "Seasonal moisture variation causing soil shrinkage/expansion",
        "Possible overloading of structural bay beyond design capacity"
    ],
    "structural_impact": "Moderate — requires prompt engineering evaluation. Not immediately life-threatening but may progress if left untreated.",
    "urgency": "High",
    "recommended_repairs": [
        {
            "repair": "Epoxy Injection",
            "description": "Low-viscosity epoxy injection (IS 13935) to seal crack and restore tensile strength. Suitable for cracks 0.2–6mm width.",
            "estimated_cost_inr": "₹8,000 – ₹15,000",
            "timeline": "1–2 days"
        },
        {
            "repair": "Foundation Underpinning Investigation",
            "description": "Engage structural engineer for subsurface investigation. Soil borings required to assess differential settlement cause.",
            "estimated_cost_inr": "₹25,000 – ₹60,000",
            "timeline": "1–2 weeks"
        },
        {
            "repair": "Crack Monitoring",
            "description": "Install crack width gauges (tell-tales) at three points along crack length. Monitor weekly for 4 weeks.",
            "estimated_cost_inr": "₹2,000 – ₹5,000",
            "timeline": "Immediate"
        }
    ],
    "applicable_standards": ["IS 456:2000 Clause 8.2", "IS 13935:2009 (Repair of Cracked Structures)", "ACI 224R-01"]
}

DEMO_WEATHER_ALERTS = {
    "High Wind": {
        "alert_level": "DANGER",
        "color": "#EF4444",
        "icon": "🌪️",
        "headline": "High Wind Advisory — Suspend Elevated Operations",
        "alerts": [
            {"category": "Crane Operations", "action": "SUSPEND ALL CRANE LIFTS immediately. Wind speeds exceeding 12 m/s (OSHA limit). Secure boom and counterweight.", "severity": "Critical"},
            {"category": "Scaffolding Safety", "action": "Inspect all scaffold clamps and ties. Remove or secure all loose materials. Do not allow workers above 10m elevation.", "severity": "High"},
            {"category": "Hoarding & Signage", "action": "Inspect and reinforce all temporary site hoardings. Remove unsecured banners and sheeting.", "severity": "High"},
            {"category": "Concrete Operations", "action": "Halt open concrete pours. Wind causes rapid drying leading to plastic shrinkage cracks (IS 456 Clause 13.5).", "severity": "Medium"},
            {"category": "Personnel Safety", "action": "Issue wind warning to all site personnel. Restrict roof/top-floor work. Maintain communication via site radio.", "severity": "Medium"}
        ]
    },
    "Heavy Rain": {
        "alert_level": "WARNING",
        "color": "#3B82F6",
        "icon": "🌧️",
        "headline": "Heavy Rain Warning — Electrical & Excavation Hazards Active",
        "alerts": [
            {"category": "Electrical Safety", "action": "De-energize all temporary electrical panels on ground level. Use GFCI protected outlets only. No electrical work in wet conditions.", "severity": "Critical"},
            {"category": "Excavation & Trenches", "action": "Inspect all excavation walls for signs of collapse. Pump out water accumulation. Halt deep excavation work (IS 3764).", "severity": "High"},
            {"category": "Concrete Curing", "action": "Cover fresh concrete pours with polythene sheeting immediately. Rain dilutes surface concrete causing dusting and reduced strength.", "severity": "High"},
            {"category": "Foundation Work", "action": "Halt all foundation concrete pours. Rainwater contamination can reduce design strength by 15-25%.", "severity": "High"},
            {"category": "Site Access", "action": "Deploy anti-slip mats at all ladder and staircase access points. Issue rain gear to all site personnel.", "severity": "Medium"}
        ]
    },
    "Extreme Heat": {
        "alert_level": "WARNING",
        "color": "#F97316",
        "icon": "☀️",
        "headline": "Extreme Heat Protocol — Worker Welfare & Concrete Care",
        "alerts": [
            {"category": "Worker Heat Stress", "action": "Mandatory 15-min rest breaks every hour for workers in direct sunlight. Provide ORS (Oral Rehydration Salts) and shaded rest areas.", "severity": "High"},
            {"category": "Concrete Temperature Control", "action": "Mix concrete with chilled water (IS 456 Clause 9.2). Target fresh concrete temperature below 30°C. Use ice if necessary.", "severity": "High"},
            {"category": "Curing Protocol", "action": "Increase curing frequency — wet hessian curing every 2 hours. Cover all exposed concrete surfaces from direct sun.", "severity": "High"},
            {"category": "Bituminous Work", "action": "Avoid bitumen laying in peak hours (12PM–3PM). Temperature of laid bitumen must be monitored per IRC:111.", "severity": "Medium"},
            {"category": "Equipment", "action": "Check engine coolant levels in all heavy equipment. Monitor hydraulic oil temperatures. Schedule heavy ops for early morning.", "severity": "Medium"}
        ]
    },
    "Normal": {
        "alert_level": "ALL CLEAR",
        "color": "#10B981",
        "icon": "✅",
        "headline": "Normal Conditions — Full Site Operations Approved",
        "alerts": [
            {"category": "Daily Startup Checks", "action": "Conduct toolbox talk with all crew leaders. Verify PPE compliance at site entry gate.", "severity": "Low"},
            {"category": "Equipment Inspection", "action": "Pre-operational check on all cranes, hoists, and excavators per manufacturer schedule.", "severity": "Low"},
            {"category": "Concrete Quality", "action": "Conduct slump test on first batch of the day. Verify water-cement ratio per mix design.", "severity": "Low"},
            {"category": "Progress Monitoring", "action": "Update daily progress report. Photograph completed work for client and regulatory records.", "severity": "Low"},
            {"category": "Housekeeping", "action": "Clear all gangways and emergency exits. Conduct end-of-day site cleanup and tool accounting.", "severity": "Low"}
        ]
    }
}

DEMO_CHAT_RESPONSES = {
    "concrete": "For M25 concrete mix design (IS 10262:2019), the typical proportions are 1:1:2 (Cement:FA:CA) with a w/c ratio of 0.44. Target mean strength = fck + 1.65σ = 25 + 1.65×4 = 31.6 N/mm². Ensure slump of 75–100mm for RCC work. Use OPC 53 grade cement and test cubes at 7 and 28 days.",
    "rebar": "For Fe500D TMT bars per IS 1786, the minimum bend diameter is 4× bar dia for ≤25mm and 6× for >25mm. Cover requirements: Foundation=50mm, Column=40mm, Beam=25mm, Slab=20mm (IS 456 Clause 26.4). Use chair spacers to maintain bottom cover in slabs.",
    "foundation": "For raft foundation design per IS 2950, the gross safe bearing capacity must consider net pressure = gross load/area – soil overburden. Typical SBC for Bangalore hard rock: 300–500 kN/m². For expansive soils, provide 1.5m minimum depth below GL to avoid zone of desiccation.",
    "default": "I'm your AI Construction Engineering Assistant. I can help with: mix design calculations, structural member sizing, IS code compliance, quality control protocols, schedule optimization, and safety management. Please ask your specific construction engineering question and I'll provide detailed technical guidance."
}
