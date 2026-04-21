schema = {
    "type": "object",
    "description": "Structured output for website audit analysis",
    "properties": {
        "report_summary": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "enum": ["Lighthouse", "GTMetrix", "PageSpeed", "Unknown"],
                    "description": "Source of the audit report"
                },
                "overall_performance": {
                    "type": "string",
                    "enum": ["Good", "Needs Improvement", "Poor"],
                    "description": "Overall performance rating"
                },
                "core_web_vitals": {
                    "type": "object",
                    "properties": {
                        "lcp": {"type": "string"},
                        "cls": {"type": "string"},
                        "inp": {"type": "string"}
                    },
                    "required": ["lcp", "cls", "inp"]
                }
            },
            "required": ["source", "overall_performance", "core_web_vitals"]
        },

        "recommendations": {
            "type": "array",
            "description": "List of optimization recommendations",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Unique identifier for the recommendation"
                    },
                    "title": {
                        "type": "string",
                        "description": "Short technical title"
                    },
                    "why": {
                        "type": "string",
                        "description": "Explanation of why this optimization is needed"
                    },
                    "impact": {
                        "type": "string",
                        "enum": ["High", "Medium", "Low"]
                    },
                    "complexity": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"]
                    },
                    "estimated_effort": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"]
                    },
                    "category": {
                        "type": "string",
                        "enum": [
                            "Rendering",
                            "Images",
                            "JavaScript",
                            "CSS",
                            "Network",
                            "Caching",
                            "Core Web Vitals",
                            "Other"
                        ]
                    },
                    "priority_score": {
                        "type": "number",
                        "description": "Numeric score representing priority (higher = more important)"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Developer-focused implementation notes"
                    }
                },
                "required": [
                    "id",
                    "title",
                    "why",
                    "impact",
                    "complexity",
                    "estimated_effort",
                    "category",
                    "priority_score"
                ]
            }
        }
    },
    "required": ["report_summary", "recommendations"]
}