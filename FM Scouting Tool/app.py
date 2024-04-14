from bs4 import BeautifulSoup
import numpy as np


def euclidean_distance(row1, row2):
    row1 = np.array(row1[1:], dtype=float)
    row2 = np.array(row2[1:], dtype=float)
    return np.sqrt(np.sum((row1 - row2) ** 2))


# Read the HTML file
with open("ASD.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table")
rows_data = []
rows = table.find_all("tr")

for row in rows:
    row_data = []
    cells = row.find_all(["td", "th"])[2:]
    for cell in cells:
        cell_text = cell.get_text(strip=True)
        if cell_text == "-":
            row_data.append(0.0)
        elif "%" in cell_text and "G" not in cell_text:
            cell_text = float(cell_text.replace("%", "0."))
        else:
            try:
                row_data.append(float(cell_text))
            except ValueError:
                row_data.append(cell_text)
    # Append the row data to the list of rows
    rows_data.append(row_data)

rows_data = rows_data[:-1]
data = rows_data[1:]
target_row = data[0]

for i, row_data in enumerate(data):
    if i > 0 and len(row_data) != len(data[0]):
        data.pop(i)

k = 3
numeric_indices = [i for i, val in enumerate(target_row) if isinstance(val, (int, float))]
top_5_indices = sorted(numeric_indices, key=lambda i: target_row[i], reverse=True)[:5]
# Extract the top 5 numeric attributes for the target
target_top_5 = [target_row[i] for i in top_5_indices]
distances = [euclidean_distance(target_top_5, np.array(t)[top_5_indices]) for t in data]
nearest_indices = np.argsort(distances)[:k]

nearest_neighbors = [rows_data[i+1] for i in nearest_indices]
for neighbor in nearest_neighbors:
    print(neighbor)
