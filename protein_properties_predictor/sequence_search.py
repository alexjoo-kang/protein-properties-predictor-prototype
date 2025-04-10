"""
Sequence Search (BLASTp)

This module performs BLASTp similarity searches using the NCBI BLAST API.
It sends a protein sequence to the NCBI server and retrieves similar sequences.

Dependencies:
- requests (install with `pip install requests` or `conda install requests`)
"""

import requests
from time import sleep

# NCBI BLAST API endpoint
BLAST_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"

def blastp_search(sequence, database="nr", hit_count=5):
    """
    Performs a BLASTp search against the NCBI database.

    :param sequence: (str) Protein sequence.
    :param database: (str) NCBI protein database (default: "nr").
    :param hit_count: (int) Number of top hits to return.
    :return: (list) List of BLASTp hits with sequence IDs and alignment scores.
    """
    # Step 1: Submit BLAST query
    blast_params = {
        "CMD": "Put",
        "PROGRAM": "blastp",
        "DATABASE": database,
        "QUERY": sequence,
        "FORMAT_TYPE": "XML",
    }

    response = requests.post(BLAST_URL, data=blast_params)
    if response.status_code != 200:
        raise Exception(f"Error submitting BLAST query: {response.status_code}")

    # Extract BLAST Request ID (RID) for retrieving results later
    rid = None
    for line in response.text.split("\n"):
        if "RID =" in line:
            rid = line.split("=")[1].strip()
            break

    if not rid:
        raise Exception("Failed to retrieve BLAST Request ID (RID).")

    print(f"✅ BLAST request submitted. RID: {rid}")

    # Step 2: Wait for BLAST results to be ready
    while True:
        sleep(5)  # Wait 5 seconds before checking status
        check_params = {"CMD": "Get", "RID": rid, "FORMAT_OBJECT": "SearchInfo"}
        status_response = requests.get(BLAST_URL, params=check_params)

        if "Status=READY" in status_response.text:
            print("✅ BLAST search completed.")
            break
        elif "Status=WAITING" in status_response.text:
            print("⏳ Waiting for BLAST results...")
        else:
            raise Exception("Unexpected error while checking BLAST status.")

    # Step 3: Retrieve BLAST results
    result_params = {
        "CMD": "Get",
        "RID": rid,
        "FORMAT_TYPE": "XML",
    }

    result_response = requests.get(BLAST_URL, params=result_params)
    if result_response.status_code != 200:
        raise Exception(f"Error retrieving BLAST results: {result_response.status_code}")

    # Step 4: Parse the BLAST results (simplified parsing)
    hits = []
    lines = result_response.text.split("\n")
    for line in lines:
        if "<Hit_id>" in line:
            hit_id = line.split(">")[1].split("<")[0]
        if "<Hsp_score>" in line:
            score = line.split(">")[1].split("<")[0]
            hits.append((hit_id, score))
        if len(hits) >= hit_count:
            break

    return hits

if __name__ == "__main__":
    # Test case: Perform BLASTp search on a sample protein sequence
    test_sequence = "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQ"

    try:
        print("🔍 Running BLASTp search...")
        blast_hits = blastp_search(test_sequence)
        print(f"✅ Top {len(blast_hits)} BLAST Hits: {blast_hits}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
