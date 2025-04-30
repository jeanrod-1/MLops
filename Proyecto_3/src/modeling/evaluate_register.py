"""
Selecciona el run con mejor F1 y lo move a 'Production'.
"""
import mlflow
from mlflow.tracking import MlflowClient
from config import MLFLOW_TRACKING_URI

def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    experiment = client.get_experiment_by_name("diabetes-readmit")
    runs = client.search_runs(experiment.experiment_id, order_by=["metrics.f1 DESC"])

    best_run = runs[0]
    best_model = client.get_registered_model("diabetes_rf")

    # archiva versiones anteriores
    for mv in client.search_model_versions("name='diabetes_rf'"):
        if mv.current_stage == "Production":
            client.transition_model_version_stage("diabetes_rf", mv.version, "Archived")

    client.transition_model_version_stage(
        name="diabetes_rf",
        version=best_run.data.tags["mlflow.version"],
        stage="Production",
        archive_existing_versions=False,
    )
    print("Modelo promovido")

if __name__ == "__main__":
    main()