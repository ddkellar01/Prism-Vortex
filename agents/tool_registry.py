from typing import Any


def query_threat_database(ip_address: str) -> dict[str, Any]:
    """Queries persistent threat intelligence registry for IP reputation."""
    return {
        "ip": ip_address,
        "reputation_score": 0.89,
        "known_malicious_actor": True,
        "threat_tags": ["botnet_node", "credential_stuffer"],
    }


def verify_iam_policy(role_arn: str) -> dict[str, Any]:
    """Audits cloud IAM policy configurations for over-privileged assumptions."""
    return {
        "role_arn": role_arn,
        "is_overprivileged": True,
        "misconfigurations": ["s3:GetObject on *", "sts:AssumeRole without MFA"],
    }


REGISTERED_TOOLS = [query_threat_database, verify_iam_policy]
