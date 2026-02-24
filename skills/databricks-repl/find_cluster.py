"""Look up a Databricks cluster ID by name substring.

Usage: python find_cluster.py --profile <profile> --name <cluster-name-substring>

Returns JSON to stdout:
  {"cluster_id": "...", "cluster_name": "...", "state": "RUNNING"}

If multiple matches, returns a JSON array. If no matches, returns an error.
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Find a Databricks cluster by name")
    parser.add_argument("--profile", required=True, help="Databricks CLI profile from ~/.databrickscfg")
    parser.add_argument("--name", required=True, help="Cluster name or substring to match")
    args = parser.parse_args()

    query = args.name.lower()

    try:
        from databricks.sdk import WorkspaceClient
    except ImportError:
        print(json.dumps({"status": "AuthError", "message": "databricks-sdk not installed. Run: pip install databricks-sdk"}))
        sys.exit(1)

    try:
        client = WorkspaceClient(profile=args.profile)
    except Exception as e:
        print(json.dumps({"status": "AuthError", "message": f"Auth failed for profile '{args.profile}': {e}"}))
        sys.exit(1)

    matches = [
        {
            "cluster_id": c.cluster_id,
            "cluster_name": c.cluster_name,
            "state": str(c.state.value) if c.state else "UNKNOWN",
        }
        for c in client.clusters.list()
        if query in (c.cluster_name or "").lower()
    ]

    if not matches:
        print(json.dumps({"status": "ClusterNotFound", "message": f"No clusters matching '{args.name}'"}))
        sys.exit(1)

    if len(matches) == 1:
        print(json.dumps(matches[0]))
    else:
        print(json.dumps(matches))


if __name__ == "__main__":
    main()
