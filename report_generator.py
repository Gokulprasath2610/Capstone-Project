"""Report generation for loan applications - PDF and CSV export."""

import json
import csv
from typing import List, Dict, Optional
from datetime import datetime
import logging
from io import BytesIO, StringIO

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates various report formats for loan applications."""

    @staticmethod
    def generate_csv_report(applications: List[Dict], filename: Optional[str] = None) -> str:
        """Generate CSV report of applications."""
        try:
            output = StringIO()
            if not applications:
                logger.warning("No applications to export")
                return ""

            fieldnames = [
                "applicant_id", "case_id", "age", "income", "employment_type",
                "credit_score", "loan_amount", "decision", "risk_score",
                "confidence_level", "created_at"
            ]

            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            for app in applications:
                row = {field: app.get(field, "") for field in fieldnames}
                writer.writerow(row)

            csv_content = output.getvalue()
            output.close()

            if filename:
                with open(filename, 'w') as f:
                    f.write(csv_content)
                logger.info(f"CSV report saved to {filename}")

            return csv_content
        except Exception as e:
            logger.error(f"Error generating CSV report: {str(e)}")
            return ""

    @staticmethod
    def generate_json_report(applications: List[Dict], filename: Optional[str] = None) -> str:
        """Generate JSON report of applications."""
        try:
            report = {
                "report_generated_at": datetime.now().isoformat(),
                "total_applications": len(applications),
                "applications": applications
            }

            json_content = json.dumps(report, indent=2)

            if filename:
                with open(filename, 'w') as f:
                    f.write(json_content)
                logger.info(f"JSON report saved to {filename}")

            return json_content
        except Exception as e:
            logger.error(f"Error generating JSON report: {str(e)}")
            return ""

    @staticmethod
    def generate_summary_report(applications: List[Dict], filename: Optional[str] = None) -> str:
        """Generate executive summary report."""
        try:
            total = len(applications)
            approved = sum(1 for app in applications if app.get("decision") == "Approve")
            reviewed = sum(1 for app in applications if app.get("decision") == "Review")
            rejected = sum(1 for app in applications if app.get("decision") == "Reject")

            avg_risk = sum(app.get("risk_score", 0) for app in applications) / total if total > 0 else 0
            avg_confidence = sum(app.get("confidence_level", 0) for app in applications) / total if total > 0 else 0

            report = f"""
════════════════════════════════════════════════════════════════════════════
LOAN APPROVAL SYSTEM - EXECUTIVE SUMMARY REPORT
════════════════════════════════════════════════════════════════════════════

Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

════════════════════════════════════════════════════════════════════════════
STATISTICS
════════════════════════════════════════════════════════════════════════════

Total Applications Processed:    {total}
Approved:                        {approved} ({approved/total*100:.1f}%)
Under Review:                    {reviewed} ({reviewed/total*100:.1f}%)
Rejected:                        {rejected} ({rejected/total*100:.1f}%)

════════════════════════════════════════════════════════════════════════════
METRICS
════════════════════════════════════════════════════════════════════════════

Average Risk Score:              {avg_risk:.2f}/100
Average Confidence Level:        {avg_confidence:.2f}
Approval Rate:                   {approved/total*100:.1f}%

════════════════════════════════════════════════════════════════════════════
DECISION DISTRIBUTION
════════════════════════════════════════════════════════════════════════════

Decision       Count    Percentage    Bar Chart
────────────────────────────────────────────────
Approved       {approved:<6}    {approved/total*100:>6.1f}%      {'█' * int(approved/total*20)}
Review         {reviewed:<6}    {reviewed/total*100:>6.1f}%      {'█' * int(reviewed/total*20)}
Rejected       {rejected:<6}    {rejected/total*100:>6.1f}%      {'█' * int(rejected/total*20)}

════════════════════════════════════════════════════════════════════════════
DETAILED APPLICATION LIST
════════════════════════════════════════════════════════════════════════════

ID            | Decision | Risk Score | Confidence | Created At
──────────────┼──────────┼────────────┼────────────┼──────────────────────
"""

            for app in applications[:20]:  # Show first 20 apps
                app_id = app.get("applicant_id", "N/A")[:12]
                decision = app.get("decision", "N/A")[:8]
                risk = f"{app.get('risk_score', 0):.1f}"
                conf = f"{app.get('confidence_level', 0):.2f}"
                created = app.get("created_at", "N/A")[:19]

                report += f"{app_id:<13} | {decision:<8} | {risk:>10} | {conf:>10} | {created}\n"

            report += f"\n... and {max(0, total - 20)} more applications\n"

            report += """
════════════════════════════════════════════════════════════════════════════
END OF REPORT
════════════════════════════════════════════════════════════════════════════
"""

            if filename:
                with open(filename, 'w') as f:
                    f.write(report)
                logger.info(f"Summary report saved to {filename}")

            return report
        except Exception as e:
            logger.error(f"Error generating summary report: {str(e)}")
            return ""

    @staticmethod
    def generate_compliance_report(applications: List[Dict], filename: Optional[str] = None) -> str:
        """Generate compliance and audit report."""
        try:
            report = f"""
════════════════════════════════════════════════════════════════════════════
COMPLIANCE & AUDIT REPORT
════════════════════════════════════════════════════════════════════════════

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Records Audited: {len(applications)}

════════════════════════════════════════════════════════════════════════════
COMPLIANCE STATUS
════════════════════════════════════════════════════════════════════════════

"""

            kyc_compliant = 0
            aml_clear = 0
            regulatory_compliant = 0

            for app in applications:
                compliance = app.get("compliance_action", {}).get("compliance_checks", {})
                if compliance.get("kyc_verified"):
                    kyc_compliant += 1
                if compliance.get("aml_clear"):
                    aml_clear += 1
                if compliance.get("regulatory_compliant"):
                    regulatory_compliant += 1

            total = len(applications)
            report += f"""
KYC Compliance:                  {kyc_compliant}/{total} ({kyc_compliant/total*100:.1f}%)
AML Compliance:                  {aml_clear}/{total} ({aml_clear/total*100:.1f}%)
Regulatory Compliance:           {regulatory_compliant}/{total} ({regulatory_compliant/total*100:.1f}%)

════════════════════════════════════════════════════════════════════════════
AUDIT TRAIL
════════════════════════════════════════════════════════════════════════════

Case ID             | Applicant ID    | Decision   | Risk Score | Status
────────────────────┼─────────────────┼────────────┼────────────┼──────────
"""

            for app in applications[:30]:
                case_id = app.get("case_id", "N/A")[:19]
                app_id = app.get("applicant_id", "N/A")[:15]
                decision = app.get("decision", "N/A")[:10]
                risk = f"{app.get('risk_score', 0):.1f}"
                status = "PROCESSED"

                report += f"{case_id:<19} | {app_id:<15} | {decision:<10} | {risk:>10} | {status}\n"

            report += """
════════════════════════════════════════════════════════════════════════════
COMPLIANCE SIGN-OFF
════════════════════════════════════════════════════════════════════════════

This report certifies that all applications have been processed according
to established compliance procedures and regulatory requirements.

Report Authority: Automated Compliance System
Audit Status: COMPLETE
"""

            if filename:
                with open(filename, 'w') as f:
                    f.write(report)
                logger.info(f"Compliance report saved to {filename}")

            return report
        except Exception as e:
            logger.error(f"Error generating compliance report: {str(e)}")
            return ""


# Factory function
def create_report(report_type: str, applications: List[Dict], filename: Optional[str] = None) -> str:
    """Factory function to generate reports of different types."""
    reports = {
        "csv": ReportGenerator.generate_csv_report,
        "json": ReportGenerator.generate_json_report,
        "summary": ReportGenerator.generate_summary_report,
        "compliance": ReportGenerator.generate_compliance_report
    }

    generator = reports.get(report_type.lower())
    if generator:
        return generator(applications, filename)
    else:
        logger.error(f"Unknown report type: {report_type}")
        return ""
