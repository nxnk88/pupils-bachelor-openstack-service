from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query


app = FastAPI(
    title="protected-workstation-audit-service",
    description=(
        "Учебный FastAPI-сервис для аудита рабочих станций, готовых к вводу "
        "в защищенный контур."
    ),
    version="1.0.0",
)


workstations_data = [
    {
        "hostname": "ws-fin-01",
        "department": "Finance",
        "hardening_score": 92,
        "antivirus_enabled": True,
        "disk_encryption": True,
    },
    {
        "hostname": "ws-hr-02",
        "department": "HR",
        "hardening_score": 88,
        "antivirus_enabled": True,
        "disk_encryption": True,
    },
    {
        "hostname": "ws-dev-03",
        "department": "Engineering",
        "hardening_score": 79,
        "antivirus_enabled": True,
        "disk_encryption": False,
    },
    {
        "hostname": "ws-soc-04",
        "department": "Security Operations",
        "hardening_score": 95,
        "antivirus_enabled": True,
        "disk_encryption": True,
    },
    {
        "hostname": "ws-ops-05",
        "department": "Operations",
        "hardening_score": 83,
        "antivirus_enabled": False,
        "disk_encryption": True,
    },
    {
        "hostname": "ws-legal-06",
        "department": "Legal",
        "hardening_score": 87,
        "antivirus_enabled": True,
        "disk_encryption": True,
    },
]

workstations_df = pd.DataFrame(workstations_data)


def dataframe_to_records(dataframe: pd.DataFrame) -> list[dict]:
    return dataframe.to_dict(orient="records")


@app.get("/")
def read_root() -> dict:
    return {
        "service": "protected-workstation-audit-service",
        "message": (
            "Сервис выполняет аудит рабочих станций и определяет системы, "
            "готовые к вводу в защищенный контур."
        ),
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/workstations")
def get_workstations(
    department: Optional[str] = Query(
        default=None,
        description="Фильтр по подразделению рабочей станции",
    )
) -> dict:
    if department is None:
        filtered_workstations = workstations_df
    else:
        filtered_workstations = workstations_df[
            workstations_df["department"].str.casefold() == department.casefold()
        ]

    return {
        "count": len(filtered_workstations),
        "workstations": dataframe_to_records(filtered_workstations),
    }


@app.get("/workstation/{hostname}")
def get_workstation(hostname: str) -> dict:
    workstation = workstations_df[
        workstations_df["hostname"].str.casefold() == hostname.casefold()
    ]

    if workstation.empty:
        raise HTTPException(status_code=404, detail="Workstation not found")

    return dataframe_to_records(workstation)[0]


@app.get("/audit-ready")
def get_audit_ready_workstations() -> dict:
    ready_workstations = workstations_df[
        (workstations_df["hardening_score"] >= 85)
        & (workstations_df["antivirus_enabled"])
        & (workstations_df["disk_encryption"])
    ]
    department_distribution = (
        ready_workstations["department"].value_counts().sort_index().to_dict()
    )

    return {
        "message": "Рабочая станция готова к вводу в защищенный контур",
        "total_ready_workstations": len(ready_workstations),
        "department_distribution": department_distribution,
        "ready_workstations": dataframe_to_records(ready_workstations),
    }
