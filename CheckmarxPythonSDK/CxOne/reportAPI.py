import json
import requests
import time
import os
from CheckmarxPythonSDK.CxOne.httpRequests import get_request, post_request
from CheckmarxPythonSDK.CxOne import authHeaders
from CheckmarxPythonSDK.CxOne.config import config

base_url = config.get("server")


def create_scan_report(file_format, scan_id, project_id):
    report_url = f"{base_url}/api/reports"

    post_data = json.dumps({
        "fileFormat": file_format,
        "reportType": "ui",
        "reportName": "scan-report",
        "data": {
            "scanId": scan_id,
            "projectId": project_id,
            "branchName": ".unknown",
            "sections": [
                "ScanSummary",
                "ExecutiveSummary",
                "ScanResults"
            ],
            "scanners": [
                "SAST",
                "SCA",
                "KICS"
            ],
            "host": ""
        }
    })

    headers = authHeaders.auth_headers.copy()

    response = requests.post(report_url, headers=headers, data=post_data, verify=False)
    report_json = response.json()
    report_id = report_json.get("reportId")

    report_status_url = f"{base_url}/api/reports/{report_id}?returnUrl=true"

    while True:
        response = requests.get(report_status_url, headers=headers, verify=False)
        status_json = response.json()
        status = status_json.get("status")

        if status == "completed":
            print("Report has been generated successfully!")
            break
        else:
            print("Generating report, please wait...")
            time.sleep(2)
    return report_id


def get_scan_report(report_id):
    relative_url = f"/api/reports/{report_id}/download"

    response = get_request(relative_url=relative_url)
    return response.content
