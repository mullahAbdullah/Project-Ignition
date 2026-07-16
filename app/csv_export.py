import csv
import io
from datetime import datetime

def profile_to_csv(profile, analysis):
    output = io.StringIO()

    writer = csv.writer(output)
    writer.writerow(["Field", "Value"])

    writer.writerow(["Lead Score", analysis["score"]])
    writer.writerow(["Lead Quality", analysis["quality"]])
    writer.writerow(
        ["Export Date", datetime.now().strftime("%Y-%m-%d %H:%M")]
    )
    writer.writerow([])

    for key, value in profile.items():
        writer.writerow([key, value])

    return output.getvalue()