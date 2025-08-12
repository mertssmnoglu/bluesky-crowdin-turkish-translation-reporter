import requests
from type import CheckResult


def notify_discord_webhook(check_result: CheckResult, discord_webhook_url: str | None):
    """Send a notification to Discord webhook based on the check result."""

    if not discord_webhook_url:
        print("❌ Discord webhook URL is not provided.")
        return False

    # Create the message content based on the check result
    if check_result.is_there_a_job:
        title = "⚠️ Translation Needed"
        description = (
            "There are untranslated or unapproved strings that need attention."
        )
        color = 0xFF9900  # Orange color
        emoji = "🔧"
    else:
        title = "🎉 Translation Complete!"
        description = "All strings are translated and approved."
        color = 0x00FF00  # Green color
        emoji = "✅"
        
    # Create Discord embed message
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "fields": [
            {
                "name": "📈 Translated",
                "value": check_result.translated_percent,
                "inline": True,
            },
            {
                "name": "✅ Approved",
                "value": check_result.approved_percent,
                "inline": True,
            },
            {
                "name": "📝 Words to Translate",
                "value": check_result.words_to_translate,
                "inline": False,
            },
        ],
        "footer": {"text": "Bluesky Crowdin Translation Monitor"},
        "timestamp": None,  # Discord will use current timestamp
    }

    # Create the webhook payload
    payload = {
        "content": f"{emoji} **Bluesky Turkish Translation Update**",
        "embeds": [embed],
    }

    try:
        # Send POST request to Discord webhook
        response = requests.post(
            discord_webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        # Check if the request was successful
        if response.status_code == 204:
            print("✅ Discord notification sent successfully!")
            return True
        else:
            print(
                f"❌ Failed to send Discord notification. Status code: {response.status_code}"
            )
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending Discord notification: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
