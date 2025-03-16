import os


repo_structure = {
    "ad_optimization_platform": {
        "services": {
            "api_gateway": {
                "app": {
                    "api": {
                        "__init__.py": "",
                        "dependencies.py": "",
                        "errors.py": "",
                        "v1": {
                            "__init__.py": "",
                            "endpoints": {
                                "__init__.py": "",
                                "auth.py": "",
                                "ads.py": "",
                                "analytics.py": "",
                                "optimization.py": "",
                                "ai.py": "",
                                "health.py": "",
                            },
                            "router.py": "",
                        },
                    },
                    "core": {
                        "__init__.py": "",
                        "config.py": "",
                        "exceptions.py": "",
                        "logging.py": "",
                        "security.py": "",
                    },
                    "db": {
                        "__init__.py": "",
                        "base.py": "",
                        "session.py": "",
                        "repositories": {
                            "__init__.py": "",
                            "ad_repository.py": "",
                            "analytics_repository.py": "",
                            "user_repository.py": "",
                        },
                    },
                    "models": {
                        "__init__.py": "",
                        "base.py": "",
                        "ad.py": "",
                        "user.py": "",
                        "analytics.py": "",
                    },
                    "schemas": {
                        "__init__.py": "",
                        "base.py": "",
                        "ad.py": "",
                        "user.py": "",
                        "analytics.py": "",
                    },
                    "services": {
                        "__init__.py": "",
                        "ad_service.py": "",
                        "analytics_service.py": "",
                        "auth_service.py": "",
                        "ai_service.py": "",
                    },
                    "__init__.py": "",
                },
                "tests": {
                    "__init__.py": "",
                    "conftest.py": "",
                    "api": {
                        "__init__.py": "",
                        "v1": {
                            "__init__.py": "",
                            "test_auth.py": "",
                            "test_ads.py": "",
                            "test_analytics.py": "",
                            "test_optimization.py": "",
                            "test_ai.py": "",
                        },
                    },
                    "db": {"__init__.py": ""},
                    "services": {"__init__.py": ""},
                    "utils.py": "",
                },
                ".env.example": "",
                ".gitignore": "",
                "Dockerfile": "",
                "main.py": "",
                "mypy.ini": "",
                "pyproject.toml": "",
                "README.md": "",
                "requirements.txt": "",
            },
            "data_ingestion": {
                "app": {
                    "ingestion": {
                        "__init__.py": "",
                        "google_ads.py": "",
                        "meta_ads.py": "",
                        "linkedin_ads.py": "",
                    },
                    "core": {
                        "__init__.py": "",
                        "config.py": "",
                        "logging.py": "",
                    },
                    "tasks": {
                        "__init__.py": "",
                        "fetch_data.py": "",
                    },
                    "__init__.py": "",
                },
                "Dockerfile": "",
                "main.py": "",
                "requirements.txt": "",
            },
            "ml_engine": {
                "app": {
                    "models": {
                        "__init__.py": "",
                        "bid_optimizer.py": "",
                        "budget_allocator.py": "",
                    },
                    "core": {
                        "__init__.py": "",
                        "config.py": "",
                    },
                    "__init__.py": "",
                },
                "Dockerfile": "",
                "main.py": "",
                "requirements.txt": "",
            },
            "dashboard": {
                "src": {
                    "components": {
                        "CampaignAnalytics.tsx": "",
                        "BudgetOptimizer.tsx": "",
                        "AIInsights.tsx": "",
                    },
                    "pages": {
                        "Home.tsx": "",
                        "Campaigns.tsx": "",
                        "Insights.tsx": "",
                    },
                    "utils": {"api.ts": ""},
                },
                "public": {},
                "Dockerfile": "",
                "package.json": "",
                "README.md": "",
                "vite.config.ts": "",
            },
        },
        "infra": {
            "k8s": {
                "api_gateway.yaml": "",
                "data_ingestion.yaml": "",
                "ml_engine.yaml": "",
                "dashboard.yaml": "",
                "postgres.yaml": "",
                "clickhouse.yaml": "",
            },
            "docker-compose.yml": "",
            "terraform": {
                "main.tf": "",
                "variables.tf": "",
            },
        },
        ".gitignore": "",
        "README.md": "",
    }
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)


if __name__ == "__main__":
    create_structure(".", repo_structure)
    print("Project structure generated successfully!")