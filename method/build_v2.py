# Build dataset_v2.csv from dataset.csv (first extraction, A) plus the blind round adjudication
# - every A field that adjudication marked wrong gets B's value (origin = corrected)
# - every record only B had and adjudication marked as a real A omission is added (origin = B)
# - the rest stays as A (origin = A). Optional records B added (both_acceptable) stay out
#
# Usage: python build_v2.py   (paths are relative to this file)
import csv
import json
import os
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ADJUDICATION_TO_DATASET_FIELD = {"value": "value", "unit": "unit", "dose_and_unit": "dose_and_unit", "location": "location",
	"season_or_year": "season_or_year", "n_or_reps": "n_or_reps", "significance_letter": "significance_letter"}


def format_cell(value):
	# Same text the first dataset.csv used: null -> empty, bool -> true/false, numbers as str()
	if value is None:
		return ""
	if isinstance(value, bool):
		return "true" if value else "false"
	return str(value)


def load_json(path):
	with open(path, encoding="utf-8") as handle:
		return json.load(handle)


def main():
	with open(os.path.join(ROOT, "dataset.csv"), encoding="utf-8", newline="") as handle:
		reader = csv.DictReader(handle)
		columns = reader.fieldnames
		dataset_rows = list(reader)
	with open(os.path.join(HERE, "adjudication.csv"), encoding="utf-8", newline="") as handle:
		adjudication_rows = list(csv.DictReader(handle))

	# Make sure the formatter rebuilds the A rows exactly, so B rows come out in the same format
	extracted_by_doc = {}
	for row in dataset_rows:
		doc_id = row["doc_id"]
		if doc_id not in extracted_by_doc:
			extracted_by_doc[doc_id] = load_json(os.path.join(ROOT, "extracted", doc_id + ".json"))
		record = extracted_by_doc[doc_id][int(row["record_index"])]
		for key, value in record.items():
			assert format_cell(value) == row[key], (doc_id, row["record_index"], key)

	rows_by_key = {(row["doc_id"], row["record_index"]): row for row in dataset_rows}
	for row in dataset_rows:
		row["origin"] = "A"

	# Field corrections on paired records
	corrected_records = set()
	for adjudicated in adjudication_rows:
		if not adjudicated["a_error_type"] or adjudicated["kind"] == "only_in_B":
			continue
		assert adjudicated["decision"] == "B_right", adjudicated["diff_id"]
		row = rows_by_key[(adjudicated["doc_id"], adjudicated["a_index"])]
		field = ADJUDICATION_TO_DATASET_FIELD[adjudicated["field"]]
		assert row[field] == adjudicated["a_value"], adjudicated["diff_id"]
		row[field] = adjudicated["b_value"]
		row["origin"] = "corrected"
		corrected_records.add((adjudicated["doc_id"], adjudicated["a_index"]))

	# Records A omitted, taken from B
	blind_by_doc = {}
	added_by_doc = collections.defaultdict(list)
	for adjudicated in adjudication_rows:
		if adjudicated["kind"] != "only_in_B" or adjudicated["decision"] != "B_right":
			continue
		doc_id = adjudicated["doc_id"]
		if doc_id not in blind_by_doc:
			blind_by_doc[doc_id] = load_json(os.path.join(HERE, doc_id + ".json"))
		added_by_doc[doc_id].append(blind_by_doc[doc_id][int(adjudicated["b_index"])])

	# Keep each document together: A rows first, then the added B rows with record_index going on from A
	template_by_doc = {}
	output_rows = []
	for row in dataset_rows:
		template_by_doc.setdefault(row["doc_id"], row)
	for doc_id in dict.fromkeys(row["doc_id"] for row in dataset_rows):
		doc_rows = [row for row in dataset_rows if row["doc_id"] == doc_id]
		output_rows.extend(doc_rows)
		next_index = max(int(row["record_index"]) for row in doc_rows) + 1
		for record in added_by_doc.get(doc_id, []):
			new_row = {column: "" for column in columns}
			for key, value in record.items():
				new_row[key] = format_cell(value)
			new_row["record_index"] = str(next_index)
			# Checked against the PDF in the adjudication
			new_row["verified_ok"] = "true"
			new_row["citation"] = template_by_doc[doc_id]["citation"]
			new_row["license"] = template_by_doc[doc_id]["license"]
			new_row["origin"] = "B"
			output_rows.append(new_row)
			next_index += 1

	with open(os.path.join(ROOT, "dataset_v2.csv"), "w", encoding="utf-8", newline="") as handle:
		writer = csv.DictWriter(handle, fieldnames=columns + ["origin"])
		writer.writeheader()
		writer.writerows(output_rows)

	origin_count = collections.Counter(row["origin"] for row in output_rows)
	# Expected from the adjudication: 1955 A records, 88 with a field fixed, 120 omissions added
	assert len(dataset_rows) == 1955 and len(corrected_records) == 88
	assert origin_count == {"A": 1867, "corrected": 88, "B": 120}, origin_count
	assert len({(row["doc_id"], row["record_index"]) for row in output_rows}) == len(output_rows)
	print(len(output_rows), dict(origin_count))


if __name__ == "__main__":
	main()
