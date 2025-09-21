import subprocess
import tempfile
import os
from bs4 import BeautifulSoup

# URLs and their associated output file names and table IDs
targets = [
    # {
    #     "url": "https://fhusagrapevine.sportspilot.com/Scheduler/Public/report.aspx?contest=1705&header=off&team=20480",
    #     "grade": "6th"
    # },
    # {
    #     "url": "https://fhusagrapevine.sportspilot.com/Scheduler/Public/report.aspx?contest=1709&header=off&team=20481",
    #     "grade": "9th"
    # },
    {
        "url": "https://fhusagrapevine.sportspilot.com/Scheduler/public/report.aspx?contest=1724&header=off&team=20681",
        "grade": "7th-Black"  
    },
    {
        "url": "https://fhusagrapevine.sportspilot.com/Scheduler/public/report.aspx?contest=1724&header=off&team=20682",
        "grade": "7th-Silver"  
    },
    {
        "url": "https://fhusagrapevine.sportspilot.com/Scheduler/public/report.aspx?contest=1723&header=off&team=20604",
        "grade": "HS"  
    }
]

# Table IDs and output file name templates
table_info = [
    {
        "id": "ctl00_MainColumn_ctl01_ctl00_StandingsGrid_ctl00",
        "suffix": "standings"
    },
    {
        "id": "ctl00_MainColumn_RegularGamesGridPanel_ctl00",
        "suffix": "schedule"
    }
]

def save_table_as_html(table, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write('<html><head><meta charset="utf-8"></head><body>\n')
        f.write(str(table))
        f.write('\n</body></html>')
    print(f"Saved {filename}")

def main():
    for target in targets:
        # Download HTML to a temp file using curl
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            tmp_filename = tmpfile.name

        # Use curl to download the HTML
        subprocess.run([
            "curl", "-s", "-A", "Mozilla/5.0", "-o", tmp_filename, target["url"]
        ], check=True)

        # Parse the HTML and extract tables
        with open(tmp_filename, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        for info in table_info:
            table = soup.find("table", id=info["id"])
            if table:
                outname = f"fall-2025-{target['grade']}-{info['suffix']}.html"
                save_table_as_html(table, outname)
            else:
                print(f"Table with id {info['id']} not found for {target['grade']} grade.")

        # Remove the temporary file
        os.remove(tmp_filename)

if __name__ == "__main__":
    main()

