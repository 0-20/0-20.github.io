import csv
from itertools import chain

player = input("Enter the player's name: ")
time = input("Enter the player's time: ")
video = input("Enter the link to the player's run: ")

with open("runs.csv", "r") as run_file:
  reader = csv.reader(run_file)
  matrix = list(reader)

if player in chain(*matrix):
  for record in matrix[1:]:
    if record[0] == player:
      record[1] = time
      record[2] = video
else:
  matrix.append([player, time, video])

matrix = [matrix[0]] + sorted(matrix[1:], key=lambda l:l[1])

# Update CSV
with open("runs.csv", "w") as run_file:
  for row in matrix:
    run_file.write(",".join(row))
    run_file.write("\n")

# Update HTML
with open("all-toads.template", "r") as template:
  template_lines = template.read().split("\n")
  
  tr_tag = " "*10 + "<tr>\n"
  tr_tag += " "*12 + "<th>Place</th>\n"
  tr_tag += " "*12 + "<th>Player</th>\n"
  tr_tag += " "*12 + "<th>Time</th>\n"
  tr_tag += " "*10 + "</tr>\n"
  addition = tr_tag
  
  for idx, record in enumerate(matrix[1:]):
    tr_tag = " "*10 + "<tr>\n"
    tr_tag += " "*12 + "<td>" + str(idx+1) + "</td>\n"
    tr_tag += " "*12 + "<td>" + record[0] + "</td>\n"
    if record[2] == "":
      tr_tag += " "*12 + "<td>" + record[1] + "</td>\n"
    else:
      tr_tag += " "*12 + '<td><a target="_blank" href="' + record[2] + '">' + record[1] + '</td>\n'
    tr_tag += " "*10 + "</tr>\n"
    addition += tr_tag
    
  template_lines[18] = addition[:-1]
  out_file = "\n".join(template_lines)
  
  with open("all-toads.html", "w") as final:
    final.write(out_file)