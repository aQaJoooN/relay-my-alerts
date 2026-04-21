

def alert_decorator(old_message):
    
    severity_map = {
        "warning": "🟡 WARNING 🟡",
        "major": "🟠 MAJOR 🟠",
        "critical": "🔴 CRITICAL 🔴",
        "resolved": "✅ RESOLVED ✅"
    }
    out_message = []
    for alert in old_message.get("alerts", []):
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        alert_name = labels.get("alertname", "UnknownAlert")
        severity = labels.get("severity", "").lower()
        instance = labels.get("instance", "N/A")
        service = labels.get("service", "N/A")
        team = labels.get("team", "N/A")

        summary = annotations.get("summary", "No summary")
        description = annotations.get("description", "No description")

        starts_at = alert.get("startsAt", "N/A")

        severity_title = severity_map.get(severity, severity.upper())

        formatted = f"""
    {severity_title} {alert_name}
━━━━━━━━━━━━━━━━━━━━
🚨 **{alert_name}**
💻 Instance: {instance}
⚙️ Service: **{service}**
👥 Team: {team}
📝 **Summary:** {summary}
📋 **Details:** {description}
⏰ Started: {starts_at}
📊 [Dashboard](http://grafana.com/dashboard)
""".strip()
        out_message = formatted
    
    return out_message