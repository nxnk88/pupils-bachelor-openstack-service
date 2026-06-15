from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query


app = FastAPI(
    title="pupils-bachelor-openstack-service",
    description=(
        "Учебный FastAPI-сервис для определения студентов, которые могут стать "
        "бакалаврами в области защищенных автоматизированных систем."
    ),
    version="1.0.0",
)


students_data = [
    {
        "name": "Ivan Petrov",
        "specialization": "Protected Automated Systems",
        "grade": 5,
        "course": 4,
    },
    {
        "name": "Anna Smirnova",
        "specialization": "Information Security",
        "grade": 4,
        "course": 3,
    },
    {
        "name": "Dmitry Sokolov",
        "specialization": "Network Security",
        "grade": 3,
        "course": 3,
    },
    {
        "name": "Maria Kuznetsova",
        "specialization": "Protected Automated Systems",
        "grade": 4,
        "course": 2,
    },
    {
        "name": "Sergey Ivanov",
        "specialization": "Secure Software Development",
        "grade": 5,
        "course": 3,
    },
    {
        "name": "Elena Morozova",
        "specialization": "Information Security",
        "grade": 5,
        "course": 4,
    },
]

students_df = pd.DataFrame(students_data)


def dataframe_to_records(dataframe: pd.DataFrame) -> list[dict]:
    return dataframe.to_dict(orient="records")


@app.get("/")
def read_root() -> dict:
    return {
        "service": "pupils-bachelor-openstack-service",
        "message": (
            "Сервис определяет студентов, которые могут стать бакалаврами "
            "в области защищенных автоматизированных систем."
        ),
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/students")
def get_students(
    specialization: Optional[str] = Query(
        default=None,
        description="Фильтр по специализации студента",
    )
) -> dict:
    if specialization is None:
        filtered_students = students_df
    else:
        filtered_students = students_df[
            students_df["specialization"].str.casefold() == specialization.casefold()
        ]

    return {
        "count": len(filtered_students),
        "students": dataframe_to_records(filtered_students),
    }


@app.get("/student/{name}")
def get_student(name: str) -> dict:
    student = students_df[students_df["name"].str.casefold() == name.casefold()]

    if student.empty:
        raise HTTPException(status_code=404, detail="Student not found")

    return dataframe_to_records(student)[0]


@app.get("/bachelor")
def get_bachelor_candidates() -> dict:
    candidates = students_df[(students_df["grade"] >= 4) & (students_df["course"] >= 3)]
    specialization_distribution = (
        candidates["specialization"].value_counts().sort_index().to_dict()
    )

    return {
        "message": "Я стану бакалавром в области защищенных автоматизированных систем",
        "total_candidates": len(candidates),
        "specialization_distribution": specialization_distribution,
        "candidates": dataframe_to_records(candidates),
    }
